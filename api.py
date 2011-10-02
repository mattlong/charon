import json

from fabric.api import settings, env, sudo, run
from fabric.network import disconnect_all

#env.key_filename = ['/home/ubuntu/.ssh/dev_key_pair.pem']
PROXY_HOST = '10.112.91.114'

def set_key_filename(obj):
    env.key_filename = obj

def _do_command(command):
    with settings(host_string=PROXY_HOST):
        result = sudo(command)
    disconnect_all()
    return json.loads(result.stdout)

def show(frontend=None, host=None):
    parts = ['charon show']
    if frontend:
        parts.append(frontend)
        if host:
            parts.append(host)

    return _do_command(' '.join(parts))

def add(frontend, host, state='enabled'):
    return _do_command('charon add %s %s %s' % (frontend, host, state,))

def remove(frontend, host):
    return _do_command('charon remove %s %s' % (frontend, host,))

def enable(frontend, host):
    return _do_command('charon enable %s %s' % (frontend, host,))

def disable(frontend, host):
    return _do_command('charon disable %s %s' % (frontend, host,))
