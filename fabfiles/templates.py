from fabric.api import run, sudo, hosts, settings, abort, warn, cd, local, put, get
from fabric.contrib.console import confirm
from fabric.contrib.files import exists, sed

from library import get_files, put_files, place_files, services
    
site_url = "therealkatie.net"
site = "realkatie"
    
UPDATE_SETTINGS = (
    )
    
UPDATE_TEMPLATES = (
    ('base.html', ''),
    ('front_page.html', 'flatpages'),
    )
    
UPDATE_MEDIA = (
    ('main.css', 'css'),
    )

    
def deploy():
    get_files(UPDATE_TEMPLATES=UPDATE_TEMPLATES, UPDATE_MEDIA=UPDATE_MEDIA, site=site)
    put_files()
    place_files(UPDATE_TEMPLATES=UPDATE_TEMPLATES, UPDATE_MEDIA=UPDATE_MEDIA, site=site)
    services(site_url = site_url)
    
