from fabric.api import run, sudo, hosts, settings, abort, warn, cd, local, put, get
from fabric.contrib.console import confirm
from fabric.contrib.files import exists, sed

from library import services

def put_files():
    sudo('rm -rf /tmp/deploy/')
    sudo('mkdir -p /tmp/deploy/')
    sudo('chown kcunning /tmp/deploy')
    local('rm -rf The-Real-Katie')
    local('rm deploy-files.tar')
    local('git clone git@github.com:kcunning/The-Real-Katie.git')
    local('tar cvf deploy-files.tar The-Real-Katie/*')
    put('deploy-files.tar', '/tmp/deploy/deploy-files.tar')
    sudo('tar xvf /tmp/deploy/deploy-files.tar -C /tmp/deploy')
    local('rm -rf The-Real-Katie')

def place_files(site_name, site_url, wsgi_name):
    sudo('mv /tmp/deploy/The-Real-Katie/config/%s /etc/apache2/sites-available/' % site_url)
    
    sudo('mkdir -p /var/www/mydjango/django_templates/%s' % site_name)
    sudo('mkdir -p /var/www/mydjango/media/%s/img' % site_name)
    sudo('mkdir -p /var/www/mydjango/media/%s/css' % site_name)
    
    sudo('cp -r /tmp/deploy/The-Real-Katie/sites/%s/templates/* /var/www/mydjango/django_templates/%s/' % (site_name, site_name))
    sudo('cp -r /tmp/deploy/The-Real-Katie/sites/%s/media/css /var/www/mydjango/media/%s/' % (site_name, site_name))

    sudo('mkdir -p /var/www/mydjango/django_projects/%s' % site_name)
    sudo('cp /tmp/deploy/The-Real-Katie/django/%s/*.py /var/www/mydjango/django_projects/%s' % (site_name, site_name))
    try:
        sudo('cp /tmp/deploy/The-Real-Katie/django/%s/%s.db /var/www/mydjango/data/' % (site_name, site_name))
        sudo('chown www-data /var/www/mydjango/data/%s.db' % site_name)
    except:
        print "No database."
        
    sudo('cp /tmp/deploy/The-Real-Katie/config/%s /var/www/mydjango/apache/' % wsgi_name)

    

        
def deploy():
    site_name = "realjacob"
    site_url = "therealjacob.net"
    wsgi_name = "trj.wsgi"
    put_files()
    place_files(site_name=site_name, site_url=site_url, wsgi_name=wsgi_name)
    services(site_url=site_url)
    