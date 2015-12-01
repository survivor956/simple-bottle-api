from fabric.api import local, cd, run, env, roles, sudo, put
from fabric.context_managers import prefix
from fabtools import require
import fabtools


env.project_name = "simple-bottle-api"
env.repo = "survivor956/simple-bottle-api"

INSTALL_PACKAGES_CENTOS = [
     'python-devel',
     'python-setuptools.noarch',
     'python-pip',
     "gcc",
     
]

env.forward_agent = True
env.roledefs.update({
    "vagrant": ["127.0.0.1:2222"]
})

# 
# Environments setup
# 

def vagrant():
    env.user = "vagrant"
    # use vagrant ssh key
    result = local("vagrant ssh-config | grep IdentityFile", capture=True)
    env.key_filename = result.split()[1]

# 
# Installation functions
# 

def create_virtualenv(environment):
    if environment == "local":
        run("virtualenv /home/vagrant/envs/{0}/".format(env.project_name))
        run('sudo echo "source /home/vagrant/envs/{0}/bin/activate" >> /home/vagrant/.bashrc'.format(
        env.project_name))
    else:
        run("virtualenv ~/projects/envs/{0}".format(env.project_name))

def install_requirements(environment):
    if environment == "local":
        with cd("/vagrant/"):
            with prefix("source /home/vagrant/envs/{0}/bin/activate".format(env.project_name)):
                run("pip install -r requirements.txt")

def install_mongodb():
    sudo("""cat >/etc/yum.repos.d/mongodb.repo <<EOL
[mongodb]
name=MongoDB Repository
baseurl=http://downloads-distro.mongodb.org/repo/redhat/os/i686/
gpgcheck=0
enabled=1
EOL""")
    sudo("yum install -y mongodb mongodb-server")
    sudo("service mongod start")
    sudo("chkconfig mongod on")
    
# 
#  Bootstrapping scripts
# 

def bootstrap(environment):
    #Install Redhat requirements
    sudo("yum update -y")
    sudo("/etc/init.d/vboxadd setup")
    package_str = " ".join(INSTALL_PACKAGES_CENTOS)
    sudo("rpm -ivh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm")#extra package required
    sudo("yum -y install "+package_str)
    sudo("pip install fabric fabtools virtualenv")

@roles('vagrant')
def bootstrap_vagrant():
    env.warn_only = True
    vagrant()
    install_mongodb()
    """bootstrap(environment="local")
    create_virtualenv(environment="local")
    install_requirements(environment="local")"""

def restart_supervisor():
    #TODO# Restart supervisor
    pass

def run_tests():
    pass

def prepare_deploy():
    run_tests()
    local('git checkout master')

@roles('production')
def deploy():
    pass
