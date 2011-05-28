import os.path
from fabric.api import env, local, cd, run, put

env.hosts = ['redcoat']
server_repo = "/home/alexm/repos/civic-site"
server_rdfs = "/home/alexm/repos/civic-rdf"
prefix_4s = "/home/alexm/.local/bin"

def _push_code():
    local("git push 'redcoat:%s' HEAD:incoming" % server_repo)

def install_server():
    run("mkdir -p '%s'" % server_repo)
    run("mkdir -p '%s'" % server_rdfs)
    with cd(server_repo):
        run("git init")
    _push_code()
    with cd(server_repo):
        run("git checkout incoming -b deploy")

def cleanup_server():
    run("rm -rf '%s'" % server_repo)

def deploy():
    _push_code()
    with cd(server_repo):
        run("git reset incoming --hard")

def rdfupload(local_path):
    base_name = os.path.basename(local_path)
    rdf_name = 'http://civic.grep.ro/model/%s' % base_name
    remote_path = "%s/%s" % (server_rdfs, base_name)
    put(local_path, remote_path)
    run("%s/4s-import civic <(bzcat '%s') -m '%s'" % (
            prefix_4s, remote_path, rdf_name))
