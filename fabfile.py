import os.path
from fabric.api import env, local, cd, run, put

env.hosts = ['redcoat']
server_prefix = "/home/alexm/sites/civic.grep.ro"
server_repo = "%s/src/civic-site" % server_prefix
server_rdfs = "%s/rdf" % server_prefix
fourstore_bin_prefix = "/home/alexm/.local/bin"
bin_prefix = "%s/bin" % server_prefix

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

def install_server():
    run("mkdir -p '%s'" % server_prefix)
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

def rdfupload(local_path):
    base_name = os.path.basename(local_path)
    rdf_name = 'http://civic.grep.ro/model/%s' % base_name
    remote_path = "%s/%s" % (server_rdfs, base_name)
    put(local_path, remote_path)
    run("%s/4s-import civic <(bzcat '%s') -m '%s'" % (
            bin_prefix, remote_path, rdf_name))
