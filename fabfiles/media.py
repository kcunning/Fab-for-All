from fabric.api import run, sudo, hosts, settings, abort, warn, cd, local, put, get
from fabric.contrib.console import confirm
from fabric.contrib.files import exists, sed

from library import get_files, put_files, place_files, services


UPDATE_MEDIA = (
    ('main.css', 'css'),
)

UPDATE_TEMPLATES=(
    ('base.html', 'comments'),
)
    
def deploy():
    site = "realkatie"
    site_url = "therealkatie.net"
    print "Getting files"
    get_files(UPDATE_TEMPLATES=UPDATE_TEMPLATES, UPDATE_MEDIA=UPDATE_MEDIA, site=site)
    print "Putting files"
    put_files()
    print "Placing files"
    place_files(UPDATE_TEMPLATES=UPDATE_TEMPLATES, UPDATE_MEDIA=UPDATE_MEDIA, site=site)
    print "Restarting services"
    services(site_url=site_url)
