from fabric.api import local, cd, run, env, roles, sudo, put
from fabric.context_managers import prefix
from fabtools import require
import fabtools
import platform

DEBIANBASED = ["debian", "ubuntu"]
REDHATBASED = ["centos", "fedora", "redhat"]

env.project_name = "cm2_bm_net"
env.repo = "git@dev.fadatec.com:cm2_bm_net"

HOST = "127.0.0.1:2322"
USER = ""
PASSWORD = ""

MIRRORHOST = "178.18.31.125"
MIRRORUSER = "rosafi"
MIRRORPASSWORD = "rsf123"

INSTALL_PACKAGES_DEBIAN = [
     'software-properties-common',
     'python-software-properties',
     'build-essential',
     'python-dev',
     'python-setuptools',
     'python-pip',
     'unzip',
     'wget'
]

INSTALL_PACKAGES_CENTOS = [
     'python-devel.x86_64',
     'python-setuptools.noarch',
     'python-pip',
     "gcc.x86_64",
     'unzip',
     'wget'
     
]

env.forward_agent = True
env.roledefs.update({
    "vagrant": ["127.0.0.1:2222"],
    "baremetal": [HOST],
    "mirror": [MIRRORHOST]
})

# 
# Environments setup
# 

def vagrant():
    env.user = "vagrant"
    # use vagrant ssh key
    result = local("vagrant ssh-config | grep IdentityFile", capture=True)
    env.key_filename = result.split()[1]

def baremetal():
    env.base = "~/projects/{0}/".format(env.project_name)
    print "Enter credentials for host '%s'" %(HOST)
    if(USER == ""):
        user = raw_input("Enter username: ")
        env.user = user
    else:
        env.user = USER
    password = raw_input("Enter password: ")
    env.password = password

def mirror():
    if(MIRRORHOST == ""):
        host = raw_input("Enter Mirror Address: ")
        env.hosts = [host]
    #else:
        #env.hosts = [MIRRORHOST]
        
    if(MIRRORUSER == ""):
        user = raw_input("Enter Mirror username: ")
        env.user = user
    else:
        env.user = MIRRORUSER
        
    if(MIRRORPASSWORD == ""):
        password = raw_input("Enter Mirror password: ")
        env.password = password
    else:
        env.password = MIRRORPASSWORD
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
            with prefix("source /home/vagrant/envs/cm2_bm_net/bin/activate"):
                run("pip install -r requirements.txt")
    else:
        if(environment == "baremetal"):
            with cd(env.base):
                with prefix("source ~/projects/envs/cm2_bm_net/bin/activate"):
                    run("pip install -r requirements.txt")

# 
#  Bootstrapping scripts
# 

def bootstrap_debian(environment):
    #Install Debian requirements
    sudo("apt-get update")
    package_str = " ".join(INSTALL_PACKAGES_DEBIAN)
    sudo("apt-get -y install "+package_str)
    sudo("apt-get install -y git")
    sudo("apt-get install -y bridge-utils")
    sudo("pip install fabric fabtools virtualenv")

def bootstrap_redhat(environment):
    #Install Redhat requirements
    sudo("yum update -y")
    package_str = " ".join(INSTALL_PACKAGES_CENTOS)
    sudo("rpm -ivh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm")#extra package required
    sudo("yum -y install "+package_str)
    sudo("yum install -y git")
    sudo("yum install -y bridge-utils")
    sudo("pip install fabric fabtools virtualenv")

def bootstrap(environment):
    distribution = run("tr -s ' \011' '\012' < /etc/issue | head -n 1").lower()
    print distribution
    if(distribution in DEBIANBASED):
        bootstrap_debian(environment)
    else:
        if(distribution in REDHATBASED):
            bootstrap_redhat(environment)
    if (environment == "baremetal"):
        run("mkdir ~/projects/")
        fabtools.git.clone(remote_url=env.repo,
                           path='~/projects/{0}'.format(env.project_name))

@roles('vagrant')
def bootstrap_vagrant():
    env.warn_only = True
    vagrant()
    bootstrap(environment="local")
    create_virtualenv(environment="local")
    install_requirements(environment="local")
    install_pyinstaller()

@roles('baremetal')
def bootstrap_baremetal():
    env.warn_only = True
    baremetal()
    bootstrap(environment="baremetal")
    create_virtualenv(environment="baremetal")
    install_requirements(environment="baremetal")
    #TODO#
    #Install supervisor

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

@roles('baremetal')
def deploy():
    baremetal()
    prepare_deploy()
    local('git push origin master')
    with cd(env.base):
        with prefix("source ~/projects/envs/{0}/bin/activate".format(env.project_name)):
            run("git pull origin master")
            restart_supervisor()

def install_pyinstaller():
    with cd("/tmp"):
        run("wget https://github.com/pyinstaller/pyinstaller/archive/develop.zip")
        run("unzip develop.zip")
        with cd("pyinstaller-develop"):
            run("python setup.py install")

@roles('vagrant')
def distribute():
    vagrant()
    with cd("/vagrant"):
        run("pyinstaller -y cloudmatic_bm_net/networking_api.py")
        with cd("dist"):
            run("tar -zcvf networking_api.tar.gz networking_api/")
            #TODO
            #upload networking_api.tar.gz to ftp server

@roles('mirror')
def upload_package():
    mirror()
    put('dist/networking_api.tar.gz', '/srv/rosafi/packages/networking-api/', use_sudo=True)
    put('/home/yahya/rosafi/cm2_bm_net/cloudmatic_bm_net/external/centos/networking_api', '/srv/rosafi/packages/networking-api/centos/', use_sudo=True)
    put('/home/yahya/rosafi/cm2_bm_net/cloudmatic_bm_net/external/centos/networking_api.conf', '/srv/rosafi/packages/networking-api/centos/', use_sudo=True)
    put('/home/yahya/rosafi/cm2_bm_net/cloudmatic_bm_net/external/ubuntu/networking_api', '/srv/rosafi/packages/networking-api/ubuntu', use_sudo=True)
    put('/home/yahya/rosafi/cm2_bm_net/cloudmatic_bm_net/external/ubuntu/networking_api.conf', '/srv/rosafi/packages/networking-api/ubuntu/', use_sudo=True)
