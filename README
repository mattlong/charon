##Introduction##
Charon is a set a tools to manage an instance of the load balancer HAProxy. You can do so either locally or remotely using either the command-line directly or via a Fabric wrapper.

##Command Line##
charon all
charon show <frontend_name>
charon add <frontend_name> <host> <enabled|disabled>(optional)
charon remove <frontend_name> <host>
charon enable <frontend_name> <host>
charon disable <frontend_name> <host>

##Fabric API##
get_frontends()
  => { '<frontend_name>': <get_backends('<frontend_name>')>, ... }

get_backends(frontend_name)
  => { '<1.1.1.1:80>': { 'status': 'enabled' }, ... }

add_backend(frontend_name, host, status=enabled)
  => same as get_backends(frontend_name) as if it were called after the operation

remove_backend(frontend_name, host)
  => same as get_backends(frontend_name) as if it were called after the operation

disable_backend(frontend_name, host)
  => same as get_backends(frontend_name) as if it were called after the operation

enable_backend(frontend_name, host)
  => same as get_backends(frontend_name) as if it were called after the operation
