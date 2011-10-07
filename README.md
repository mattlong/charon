## Introduction
Charon is a set a tools to manage an instance of the load balancer HAProxy. You can do so either locally or remotely using either the command-line directly or via a Fabric wrapper.

## Command Line
    show [<frontend_name> [<host>]]
    add <frontend_name> <host> [<enabled|disabled>]
    remove <frontend_name> <host>
    enable <frontend_name> <host>
    disable <frontend_name> <host>

## Python Configuration
Charon can (and should) be configured via a Python module named 'charonconfig' that is available on the system path. The following settings are available:

CHARON_HAPROXY_HOST
The hostname your HAProxy instance is running on. It must be accessible via SSH on port 22.

CHARON_KEY_FILENAME (optional)
Path to the local private SSL key to use to connect to your HAProxy instance. If not specified, the ususal default keys will be used. 

## Python API
    show(frontend=None, host=None)
      => { '<frontend>': <backend>: { 'status': 'enabled'}, ... }

    add(frontend, backend, state='enabled')
      => same as show(frontend) after ther add operation

    remove(frontend, backend)
      => same as show(frontend) after ther remove operation

    enable(frontend, backend)
      => same as show(frontend) after ther enable operation

    disable(frontend, backend)
      => same as show(frontend) after ther disable operation
