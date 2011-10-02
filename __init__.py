#!/usr/bin/env python

import sys, os, shutil, json, re

BASE_PATH = '/etc/charon'
GLOBAL_CONFIG_FILE = 'global'
FRONTEND_DIR = 'frontends'
HAPROXY_CFG_PATH = '/etc/haproxy/haproxy.cfg'
CFG_HEADER = '# WARNING: This HAProxy configuration was generated with Charon and should not be edited directly!\n\n'

def mkdir(path, empty=False, parents=False):
    if os.path.isdir(path):
        if empty: shutil.rmtree(path)
        else: return
    if parents: os.makedirs(path)
    else: os.mkdir(path)

def info(string):
    print string

def error(string):
    print 'ERROR: ' + string

def abs_path(rel_path):
    return os.path.join(BASE_PATH, rel_path)

class Frontend(object):
    def __init__(self, name, backend_params=''):
        self.name = name
        self.backend_params = backend_params

    def get_backends(self, serialize=False):
        fp, backends = None, {}
        try:
            fp = open(os.path.join(abs_path(FRONTEND_DIR), self.name), 'r')
            backends = json.loads(fp.read())
            fp.close()
        except:
            pass
        finally:
            fp and fp.close()

        return json.dumps(backends, indent=4) if serialize else backends

    def _update_backends(self, backends):
        fp = open(os.path.join(abs_path(FRONTEND_DIR), self.name), 'w')
        fp.write(json.dumps(backends, indent=4)+'\n')
        fp.close()

    def add_backend(self, host, state='enabled'):
        backends = self.get_backends()
        backends[host] = { 'state': state }
        self._update_backends(backends)

    def remove_backend(self, host):
        backends = self.get_backends()
        if host in backends:
            del backends[host]
        self._update_backends(backends)

    def enable_backend(self, host):
        backends = self.get_backends()
        backends[host]['state'] = 'enabled'
        self._update_backends(backends)

    def disable_backend(self, host):
        backends = self.get_backends()
        backends[host]['state'] = 'disabled'
        self._update_backends(backends)

fe_reg = re.compile(r'\s*listen\s+([^\s]+)\s+([^\s]+)[\s$]+')
be_reg = re.compile(r'\s*{{BACKEND}}(.*)$')

def parse_global():
    name, frontends = None, {}
    fp = open(abs_path(GLOBAL_CONFIG_FILE), 'r')
    for line in fp.readlines():
        m = fe_reg.match(line)
        if m:
            name = m.group(1)
            frontends[name] = Frontend(name)
            continue
        m = be_reg.match(line)
        if name is not None and m:
            frontends[name].backend_params = m.group(1)
            name = None
    fp.close()

    return frontends

def generate_config():
    global_fp = open(abs_path(GLOBAL_CONFIG_FILE), 'r')
    fp = open(os.path.join(BASE_PATH, 'haproxy.cfg.temp'), 'w')
    fp.write(CFG_HEADER)

    frontend, frontends = None, parse_global()

    def do_basic(fp, frontend):
        for host, backend in frontend.get_backends().items():
            count += 1
            state = backend['state'] if backend['state'] == 'disabled' else ''
            be_text = '\tserver %s_%d %s %s\n' % (name, count, host, state,)
            fp.write(be_text)
        fp.write('\n')

    for line in global_fp.readlines():
        m = fe_reg.match(line)
        if m:
            if frontend is not None:
                do_basic(fp, frontend)
                frontend = None

            name, count = m.group(1), 0
            frontend = frontends[name]
            fp.write(line)
            continue

        m = be_reg.match(line)
        if frontend is not None and m:
            for host, backend in frontend.get_backends().items():
                count += 1
                state = backend['state'] if backend['state'] == 'disabled' else ''
                be_text = 'server %s_%d %s %s' % (name, count, host, state,)
                fp.write(re.sub('{{BACKEND}}', be_text, line))
            frontend = None
            continue
        
        if frontend is not None and line.strip() == '':
            do_basic(fp, frontend)
            frontend = None
            continue

        fp.write(line)

    global_fp and global_fp.close()
    fp and fp.close()

def validate_args(*args):
    frontend_name, host = None, None

    if len(args) > 0:
        frontend_name = args[0]
    
    if len(args) > 1:
        host = args[1]

    frontends = parse_global()
    if frontend_name is not None and frontend_name not in frontends:
        error('Frontend %s not found' % frontend_name)
        sys.exit(1)

    return (frontend_name, host, frontends, args[2:],) 

def do_show(*args, **kwargs):
    results = {}
    (frontend_name, host, frontends, args_tail,) = validate_args(*args)
    for fe_name in parse_global().keys(): 
        results[fe_name] = frontends[fe_name].get_backends()

    if frontend_name:
        results = results[frontend_name]

    if host:
        results = results[host]

    return json.dumps(results, indent=4) if kwargs.get('serialize') else results 

def do_add(*args, **kwargs):
    (frontend_name, host, frontends, args_tail,) = validate_args(*args)

    if len(args_tail) > 1: do_help()

    state = args_tail[0] if len(args) == 1 else 'enabled'
    if state not in ('enabled', 'disabled',): do_help()

    frontends[frontend_name].add_backend(host, state=state)
    generate_config()

    results = do_show(*(frontend_name,))
    return json.dumps(results, indent=4) if kwargs.get('serialize') else results 

def do_remove(*args, **kwargs):
    (frontend_name, host, frontends, args_tail,) = validate_args(*args)
    frontends[frontend_name].remove_backend(host)
    generate_config()
    results = do_show(*(frontend_name,))
    return json.dumps(results, indent=4) if kwargs.get('serialize') else results 

def do_enable(*args, **kwargs):
    (frontend_name, host, frontends, args_tail,) = validate_args(*args)
    frontends[frontend_name].enable_backend(host)
    generate_config()
    results = do_show(*(frontend_name,))
    return json.dumps(results, indent=4) if kwargs.get('serialize') else results 

def do_disable(*args, **kwargs):
    (frontend_name, host, frontends, args_tail,) = validate_args(*args)
    frontends[frontend_name].disable_backend(host)
    generate_config()
    results = do_show(*(frontend_name,))
    return json.dumps(results, indent=4) if kwargs.get('serialize') else results 

def do_help(args=None):
        info('''Usage: charon <command> [<args>]

Available commands are:
show [<frontend_name> [<host>]]
add <frontend_name> <host> [<enabled|disabled>]
remove <frontend_name> <host>
enable <frontend_name> <host>
disable <frontend_name> <host>''')
        sys.exit(2) 

def main(*args, **kwargs):
    args = args[1:]
    if len(args) < 1: do_help()

    commands = {
        'help': do_help,
        'show': do_show,
        'add': do_add,
        'remove': do_remove,
        'enable': do_enable,
        'disable': do_disable,
    }

    command, args = args[0].lower().replace('-', '_'), args[1:]
    if command not in commands.keys():
        info("charon: '%s' is not a charon command. See 'charon help'." % (command,))
        sys.exit(2)

    info(commands[command](*args, serialize=True))

if __name__ == '__main__':
    main(*sys.argv[1:])
