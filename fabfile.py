from fabric.api import env, local, cd, run

env.hosts = ['redcoat']
server_repo = "/home/alexm/repos/civic-site"

def _push_code():
    local("git push 'redcoat:%s' HEAD:incoming" % server_repo)

def install_server():
    run("mkdir -p '%s'" % server_repo)
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
