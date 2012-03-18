from fabric.api import run, sudo, hosts, settings, abort, warn, cd, local, put, get
from fabric.contrib.console import confirm
from fabric.contrib.files import exists, sed

def apt_get_install(APT_GET_APPS=()):
    for app in APT_GET_APPS:
        sudo('apt-get -y install %s' % app)
    
def pip_install(PIP_APPS=()):
    for app in PIP_APPS:
        sudo('pip install %s' % app)

def get_db():
    local('mkdir -p temp')
    get('/var/www/mydjango/data/realkatie.db', 'temp/realkatie.db')
    try:
        local('mv ../realkatie/data.db ../sites/realkatie/data.db-bak')
    except:
        print "No db"
    local('cp temp/realkatie.db ../django/data.db')
    
def update_db_prod_only():
    # sudo -u www-data python manage.py syncdb
    pass
    
def update_db():
    local('cp ../realkatie/data.db temp/realkatie.db')
    try:
        local('mv ../realkatie/data.db-bak ../realkatie/data.db')
    except:
        print "No db"
    local('tar uvf deploy-files.tar temp/realkatie.db')
    
def put_files():
    sudo('rm -rf /tmp/deploy')
    sudo('mkdir -p /tmp/deploy')
    sudo('chown kcunning:kcunning /tmp/deploy')
    put('deploy-files.tar', '/tmp/deploy/deploy-files.tar')
    sudo('tar xvf /tmp/deploy/deploy-files.tar -C /tmp/deploy')
    
def place_files(UPDATE_TEMPLATES=(), UPDATE_MEDIA=(), UPDATE_SETTINGS=(), site=""):
    for f, p in UPDATE_TEMPLATES:
        sudo('mkdir -p /var/www/mydjango/django_templates/%s/%s' % (site, p))
        sudo('mv /tmp/deploy/The-Real-Katie/sites/%s/templates/%s/%s /var/www/mydjango/django_templates/%s/%s/%s' % (site, p, f, site, p, f))
    for f, p in UPDATE_MEDIA:
        sudo('mkdir -p /var/www/mydjango/media/%s/%s' % (site, p))
        sudo('mv /tmp/deploy/The-Real-Katie/sites/%s/media/%s/%s /var/www/mydjango/media/%s/%s/%s' % (site, p, f, site, p, f))
    for f in UPDATE_SETTINGS:
        sudo('mv /tmp/deploy/The-Real-Katie/django/%s/%s /var/www/mydjango/django_projects/%s/%s' % (site, f, site, f) )
    
def get_files(UPDATE_TEMPLATES=(), UPDATE_MEDIA=(), UPDATE_SETTINGS=(), site=""):
    try:
        local('rm -rf The-Real-Katie')
        local('rm deploy-files.tar')
    except:
        pass
    local('git clone git@github.com:kcunning/The-Real-Katie.git')
    local('touch deploy-files.tar')
    for filename in UPDATE_SETTINGS:
        local('tar uvf deploy-files.tar The-Real-Katie/django/%s/%s' % (site, filename))
    for filename, path in UPDATE_TEMPLATES:
        local('tar uvf deploy-files.tar The-Real-Katie/sites/%s/templates/%s/%s' % (site, path, filename))
    for filename, path in UPDATE_MEDIA:
        local('tar uvf deploy-files.tar The-Real-Katie/sites/%s/media/%s/%s' % (site, path, filename))

def services(site_url=""):
    sudo('a2ensite %s' % site_url)
    sudo('service apache2 restart')
