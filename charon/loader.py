import sys, os, importlib
import imp as _imp
from contextlib import contextmanager

import charon

def read_configuration():
    configname = os.environ.get("CHARON_CONFIG_MODULE", charon.CONFIG_MODULE)

    try:
        find_module(configname)
    except ImportError:
        print 'Could not find configuration module "%s". Be sure to call api.set_host before making API calls.' % (configname,)
        return {}
    else:
        charonconfig = import_from_cwd(configname)
        usercfg = dict((key, getattr(charonconfig, key))
                        for key in dir(charonconfig)
                        if key.startswith('CHARON_'))
        return usercfg

@contextmanager
def cwd_in_path():
    cwd = os.getcwd()
    if cwd in sys.path:
        yield
    else:
        sys.path.insert(0, cwd)
        try:
            yield cwd 
        finally:
            try:
                sys.path.remove(cwd)
            except ValueError:
                pass

def find_module(module, path=None, imp=None):
    if imp is None:
        imp = importlib.import_module
    with cwd_in_path():
        if "." in module:
            last = None
            parts = module.split(".")
            for i, part in enumerate(parts[:-1]):
                path = imp(".".join(parts[:i + 1])).__path__
                last = _imp.find_module(parts[i + 1], path)
            return last
        return _imp.find_module(module)

def import_from_cwd(module, imp=None):
    if imp is None:
        imp = importlib.import_module
    with cwd_in_path():
        return imp(module)
