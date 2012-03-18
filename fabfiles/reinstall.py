from fabric.api import run, sudo, hosts, settings, abort, warn, cd, local, put, get
from fabric.contrib.console import confirm
from fabric.contrib.files import exists, sed

import string, random

PACKAGES=('apache2',
          'subversion',
          'sqlite3',
          'python-setuptools',
          'python-pip',
          'git-core',
          'gitosis',
          'libapache2-mod-wsgi',
          )
          
PIP_PACKAGES = (
  'BeautifulSoup==3.2.0',
  'Markdown==2.0.3',
  'django-tagging==0.3.1',
  'elementtree==1.2.7-20070827-preview',
  'python-dateutil==2.0',
  'wsgiref==0.1.2',
  )
  
GIT_PACKAGES = (
  ('https://github.com/nathanborror/django-basic-apps.git', 'django-basic-apps'),
  )
  
          
DJANGO_REPO="http://code.djangoproject.com/svn/django/tags/releases/1.2.3/"

def add_user(user):
    local('touch passwords')
    sudo('useradd -m %s' % (user))
    sudo('echo "%s ALL=(ALL) ALL" >> /etc/sudoers' % user)
    password = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(8))
    sudo('echo "%s:%s" | chpasswd' % (user, password))
    local('echo "%s:%s" >> passwords' % (user, password))
    
def setup_server():
    sudo('apt-get update')
    for p in PACKAGES:
        sudo('apt-get -y install %s' % p)
    
        
def django_setup():
    sudo('svn co %s /usr/share/django' % DJANGO_REPO)
    sudo('chown -R www-data:www-data /usr/share/django')
    sudo('ln -s /usr/share/django/django /usr/lib/python2.6/dist-packages/django')
    sudo('ln -s /usr/share/django/django/bin/django-admin.py /usr/local/bin/django-admin.py')
    sudo('mkdir -p /var/www/mydjango/django_projects')
    sudo('mkdir -p /var/www/mydjango/data')
    sudo('mkdir -p /var/www/mydjango/apache')
    sudo('mkdir -p /var/www/mydjango/django_templates/realkatie')
    sudo('mkdir -p /var/www/mydjango/media/realkatie/css')
    sudo('mkdir -p /var/www/mydjango/media/realkatie/img')
    sudo('mkdir -p /var/www/mydjango/apache')
    sudo('ln -s /usr/share/django/django/contrib/admin/media /var/www/mydjango/admin_media')
    sudo('chown -R kcunning:kcunning /var/www/mydjango')
    sudo('rm -rf /etc/apache2/sites-available/default')
    sudo('rm -rf /etc/apache2/sites-enabled/*default')
    
def pip_install():
    for package in PIP_PACKAGES:
        sudo('pip install %s' % package)
        
def git_packages():
    sudo('mkdir -p /tmp/deploy')
    for git, package in GIT_PACKAGES:
        with cd('/tmp/deploy/'):
            sudo('git clone %s' % git)
            sudo('python %s/setup.py install' % package)
    
def db_setup():
    sudo('chown www-data /var/www/mydjango/data')
    try:
        sudo('chown www-data /var/www/mydjango/data/realkatie.db')
    except:
        print "No db on the server."
        
    
def put_files():
    sudo('mkdir -p /tmp/deploy/')
    sudo('chown kcunning /tmp/deploy')
    local('rm -rf The-Real-Katie')
    local('git clone git@github.com:kcunning/The-Real-Katie.git')
    local('tar cvf deploy-files.tar The-Real-Katie/*')
    put('deploy-files.tar', '/tmp/deploy/')
    sudo('tar xvf /tmp/deploy/deploy-files.tar -C /tmp/deploy')
    local('rm -rf The-Real-Katie')
    with cd('/tmp/deploy'):
        sudo('git clone https://github.com/nathanborror/django-basic-apps.git')
    
def place_files():
    sudo('mv /tmp/deploy/The-Real-Katie/config/therealkatie.net /etc/apache2/sites-available/')
    sudo('mv /tmp/deploy/The-Real-Katie/config/trk.wsgi /var/www/mydjango/apache/')
    
    sudo('mv /tmp/deploy/The-Real-Katie/sites/realkatie/templates/* /var/www/mydjango/django_templates/realkatie/')
    sudo('mv /tmp/deploy/The-Real-Katie/sites/realkatie/media/css/* /var/www/mydjango/media/realkatie/css')
    sudo('mv /tmp/deploy/The-Real-Katie/sites/realkatie/media/img/* /var/www/mydjango/media/realkatie/img')
    
    sudo('mkdir -p /var/www/mydjango/django_projects/realkatie')
    sudo('mv /tmp/deploy/The-Real-Katie/django/realkatie/*.py /var/www/mydjango/django_projects/realkatie')
    sudo('mv /tmp/deploy/The-Real-Katie/django/realkatie/realkatie.db /var/www/mydjango/data/')
    
    sudo('chown www-data /var/www/mydjango/data/')
    sudo('chown www-data /var/www/mydjango/data/realkatie.db')
    
    sudo('mv /tmp/deploy/django-basic-apps/basic /usr/local/lib/python2.6/dist-packages/')
    
def services():
    sudo('a2ensite therealkatie.net')
    sudo('service apache2 restart')
    
def deploy():
    add_user('kcunning')
    setup_server()
    pip_install()
    put_files()
    django_setup()
    place_files()
    db_setup()
    services()

    