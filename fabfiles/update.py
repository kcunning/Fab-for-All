from fabric.api import run, sudo, hosts, settings, abort, warn, cd, local, put, get
from fabric.contrib.console import confirm
from fabric.contrib.files import exists, sed

UPDATE_SETTINGS = (
    ('settings.py'),)
    
UPDATE_TEMPLATES = (
    ('default.html', 'flatpages'),
    ('base_blog.html', 'blog'),
    ('post_detail.html', 'blog'),
    ('post_list.html', 'blog'),
    ('base.html', ''))
    
UPDATE_MEDIA = (
    ('main.css', 'static/css'),
    ('scribble_green.jpg', 'static/img'))
    
APT_GET_APPS = (
    ('python-setuptools'),
    ('python-pip'),)
    
CO_APPS = (
    ('git clone https://github.com/nathanborror/django-basic-apps.git', 'django-basic-apps'))
    
PIP_APPS = (
    ('BeautifulSoup==3.2.0'),
    ('Markdown==2.0.3'),
    ('django-basic-apps==0.7'),
    ('django-tagging==0.3.1'),
    ('elementtree==1.2.7-20070827-preview'),
    ('python-dateutil==2.0'),
    ('wsgiref==0.1.2'),
    )
    
def apt_get_install():
    for app in APT_GET_APPS:
        sudo('apt-get -y install %s' % app)
    
def pip_install():
    for app in PIP_APPS:
        sudo('pip install %s' % app)
    
def co_and_move_install():
    pass


def get_db():
    local('mkdir -p temp')
    get('/var/www/mydjango/data/realkatie.db', 'temp/realkatie.db')
    try:
        local('mv /home/kcunning/projects/The-Real-Katie/sites/realkatie/data.db /home/kcunning/projects/The-Real-Katie/realkatie/data.db-bak')
    except:
        print "No db"
    local('cp temp/realkatie.db /home/kcunning/projects/The-Real-Katie/sites/realkatie/data.db')
    
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
    sudo('mkdir -p /tmp/deploy')
    sudo('chown kcunning:kcunning /tmp/deploy')
    put('deploy-files.tar', '/tmp/deploy/')
    sudo('tar xvf /tmp/deploy/deploy-files.tar -C /tmp/deploy')
    
def place_files():
    for f, p in UPDATE_TEMPLATES:
        sudo('mkdir -p /var/www/mydjango/django_templates/%s' % p)
        sudo('mv /tmp/deploy/The-Real-Katie/realkatie/templates/%s/%s /var/www/mydjango/django_templates/%s/%s' % (p, f, p, f))
    for f, p in UPDATE_MEDIA:
        sudo('mkdir -p /var/www/mydjango/media/%s' % p)
        sudo('mv /tmp/deploy/The-Real-Katie/realkatie/media/%s/%s /var/www/mydjango/media/%s/%s' % (p, f, p, f))
    for f in UPDATE_SETTINGS:
        sudo('mv /tmp/deploy/The-Real-Katie/django/%s /var/www/mydjango/django_projects/realkatie/%s' % (f, f) )
    
def get_files():
    try:
        local('rm -rf The-Real-Katie')
        local('rm deploy-files.tar')
    except:
        pass
    local('git clone git@github.com:kcunning/The-Real-Katie.git')
    local('touch deploy-files.tar')
    for filename in UPDATE_SETTINGS:
        local('tar uvf deploy-files.tar The-Real-Katie/django/%s' % (filename))
    for filename, path in UPDATE_TEMPLATES:
        local('tar uvf deploy-files.tar The-Real-Katie/realkatie/templates/%s/%s' % (path, filename))
    for filename, path in UPDATE_MEDIA:
        local('tar uvf deploy-files.tar The-Real-Katie/realkatie/media/%s/%s' % (path, filename))

def services():
    sudo('a2ensite therealkatie.net')
    sudo('service apache2 restart')
        
def deploy1():
    apt_get_install()
    pip_install()
    get_files()
    put_files()
    
def deploy2():
    pass
    
