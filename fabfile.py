import os.path
from StringIO import StringIO
from fabric.api import env, local, cd, run, put, open_shell

from local_fabfile import *

server_repo = "%s/src/civic-site" % server_prefix
server_rdfs = "%s/rdf" % server_prefix
fourstore_bin_prefix = "/home/alexm/.local/bin"
bin_prefix = "%s/bin" % server_prefix

FCGI_RUNNER_SCRIPT = """\
#!/bin/bash
CIVIC_SITE='%(prefix)s/bin/civic-site'
FCGI_SOCK='%(prefix)s/var/civic-site.fcgi'
PIDFILE='%(prefix)s/var/civic-site.pid'

$CIVIC_SITE --fastcgi $FCGI_SOCK --pidfile $PIDFILE
"""

RC_SITE_SCRIPT = """\
#! /bin/bash

DAEMON='%(prefix)s/bin/civic-site-fcgi.sh'
PIDFILE='%(prefix)s/var/civic-site.pid'

case "$1" in
  start)
    echo "Starting civic-site FCGI daemon"
    /sbin/start-stop-daemon --start --pidfile $PIDFILE --exec $DAEMON
    ;;
  stop)
    echo "Stopping civic-site FCGI daemon"
    /sbin/start-stop-daemon --stop --pidfile $PIDFILE --verbose
    ;;
  *)
    echo "Usage: $0 {start|stop}"
    exit 1
    ;;
esac

exit 0
"""

RC_SPARQL_SCRIPT = """\
#! /bin/bash

case "$1" in
  start)
    echo "Starting 4store http server"
    %(prefix)s/bin/4s-httpd -H 127.0.0.1 -p 11746 civic
    ;;
  stop)
    echo "Stopping 4store http server"
    killall 4s-httpd
    ;;
  *)
    echo "Usage: $0 {start|stop}"
    exit 1
    ;;
esac

exit 0
"""


def push_dep(local_path):
    base_name = os.path.basename(local_path)
    server_tmp = "%s/tmp" % server_prefix
    server_path = "%s/%s" % (server_tmp, base_name)
    run("mkdir -p '%s'" % server_tmp)
    put(local_path, server_path)
    with cd(server_prefix):
        run("bin/pip install '%s'" % server_path)
    run("rm '%s'" % server_path)

def _push_code():
    local("git push -f 'redcoat:%s' HEAD:incoming" % server_repo)

def _create_server_repo():
    run("mkdir -p '%s'" % server_repo)
    with cd(server_repo):
        run("git init")
    _push_code()
    with cd(server_repo):
        run("git checkout incoming -b deploy")

def _setup_virtualenv():
    with cd(server_prefix):
        run("virtualenv --distribute .")
        for name in ['4s-backend', '4s-httpd', '4s-import']:
            run("ln -s '%s/%s' bin/" % (fourstore_bin_prefix, name))

def _upload_fcgi_runner_scripts():
    with cd('%s/bin' % server_prefix):
        put(StringIO(FCGI_RUNNER_SCRIPT % {'prefix': server_prefix}),
            "civic-site-fcgi.sh")
        put(StringIO(RC_SITE_SCRIPT % {'prefix': server_prefix}),
            "rc-site.sh")
        put(StringIO(RC_SPARQL_SCRIPT % {'prefix': server_prefix}),
            "rc-sparql.sh")
        run("chmod +x civic-site-fcgi.sh rc-site.sh rc-sparql.sh")

def uprc():
    _upload_fcgi_runner_scripts()

def start(name):
    run("%s/bin/rc-%s.sh start" % (server_prefix, name))

def stop(name):
    run("%s/bin/rc-%s.sh stop" % (server_prefix, name))

def install_server():
    run("mkdir -p '%s'" % server_prefix)
    run("mkdir -p '%s'/var" % server_prefix)
    _create_server_repo()
    _setup_virtualenv()
    run("mkdir -p '%s'" % server_rdfs)

def cleanup_server():
    run("rm -rf '%s'" % server_repo)

def deploy():
    _push_code()
    with cd(server_repo):
        run("git reset incoming --hard")
    with cd(server_prefix):
        run("bin/pip install -e '%s'" % server_repo)
    _upload_fcgi_runner_scripts()
    stop('site')
    start('site')

def rdfupload(local_path):
    base_name = os.path.basename(local_path)
    rdf_name = 'http://civic.grep.ro/model/%s' % base_name
    remote_path = "%s/%s" % (server_rdfs, base_name)
    put(local_path, remote_path)
    stop('sparql')
    run("%s/4s-import civic <(bzcat '%s') -m '%s'" % (
            bin_prefix, remote_path, rdf_name))
    start('sparql')

def shell():
    open_shell(". .profile && cd '%s' && . bin/activate" % server_prefix)

def static():
    local("rsync -rtv static/_build/html/ 'redcoat:%s/www'" % server_prefix)

def build_static():
    local("cd static && make html")
