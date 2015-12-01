# simple-bottle-api

0. cd to the directory you want to install the project in
If first time do these, otherwise jump to '4'
1. ` git clone git@github.com:survivor956/simple-bottle-api.git`
2. `sudo apt-get install python-pip`
3. `pip install fabric fabtools`
4. cd bottle-mongo-api
4.1. If you want to reset:
    `vagrant box remove workshop` 
    `rm -rf .vagrant`
5. `vagrant up`
6. run `fab bootstrap_vagrant`
