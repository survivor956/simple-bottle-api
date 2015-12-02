# simple-bottle-api


## Installation:
===================

Please make sure that you have Vagrant and VirtualBox (Version earlier tha v5) installed before you run the following commands.

### For Debian based hosts
0. cd to the directory you want to install the project in
If first time do these, otherwise jump to '4'
1. install git and add your ssh key (https://help.github.com/articles/generating-ssh-keys/)
2. ` git clone git@github.com:survivor956/simple-bottle-api.git`
3. `sudo apt-get install python-pip`
4. `pip install fabric fabtools`
5. `cd bottle-mongo-api`
6. If you want to reset:
    `vagrant box remove workshop` 
    `rm -rf .vagrant`
7. `vagrant up`
8. run `fab bootstrap_vagrant`

### For Red Hat based hosts
0. cd to the directory you want to install the project in
If first time do these, otherwise jump to '4'
1. install git and add your ssh key (https://help.github.com/articles/generating-ssh-keys/)
2. ` git clone git@github.com:survivor956/simple-bottle-api.git`
3. `sudo yum install python-pip`
4. `pip install fabric fabtools`
5. `cd bottle-mongo-api`
6. If you want to reset:
    `vagrant box remove workshop` 
    `rm -rf .vagrant`
7. `vagrant up`
8. run `fab bootstrap_vagrant`

### For Windows hosts
VirtualBox: download.virtualbox.org/virtualbox/4.3.34/VirtualBox-4.3.34-104062-Win.exe

Vagrant: https://releases.hashicorp.com/vagrant/1.7.4/vagrant_1.7.4.msi

0. cd to the directory you want to install the project in
If first time do these, otherwise jump to '4'
1. Install git http://git-scm.com/download/win (by default shipped with Git Bash; Strongly recommended)
2. Install Python https://www.python.org/ftp/python/2.7.6/python-2.7.6.msi
3. Add C:\Python27 path to environment variable
4. Install visual c++ for python2.7: https://download.microsoft.com/download/7/9/6/796EF2E4-801B-4FC4-AB28-B59FBF6D907B/VCForPython27.msi
5. Install Python-pip: in cmd do python -c "exec('try: from urllib2 import urlopen \nexcept: from urllib.request import urlopen');f=urlopen('https://bootstrap.pypa.io/get-pip.py').read();exec(f)"
6. Add C:\Python27\Scripts path to environment variable
7. ` git clone git@github.com:survivor956/simple-bottle-api.git`
8. `sudo yum install python-pip`
9. In cmd `pip install fabric fabtools`
10. Open Git Bash and `cd bottle-mongo-api`
11. If you want to reset:

    `vagrant box remove workshop`
    `rm -rf .vagrant`
    
12. `vagrant up`
13. run `fab bootstrap_vagrant`
