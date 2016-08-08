from fabric.api import local, env
import os
import shutil
from livereload import Server
from pelican import Pelican
from pelican.settings import read_settings
import requests
import json

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'
DEPLOY_PATH = env.deploy_path

# Remote server configuration
production = 'root@localhost:22'
dest_path = '/var/www'


def clean():
    """Remove generated files"""
    if os.path.isdir(DEPLOY_PATH):
        shutil.rmtree(DEPLOY_PATH)
        os.makedirs(DEPLOY_PATH)


def build():
    """Build local version of site"""
    local('pelican -s pelicanconf.py')


def rebuild():
    """`clean` then `build`"""
    clean()
    build()


def dev():
    """Build, and run a auto-reloading server w/ file watching."""
    rebuild()
    p = Pelican(read_settings('pelicanconf.py'))

    def compile():
        try:
            p.run()
        except SystemExit as e:
            pass

    server = Server()
    server.watch('content/', compile)
    server.watch('theme/', compile)
    server.watch('pelicanconf.py', rebuild)
    server.serve(root='output')


def clear_cache():
    # Purges the CloudFlare cache.
    # Zone was retrieved using:
    # curl -X GET "https://api.cloudflare.com/client/v4/zones?name=untrod.com&status=active&page=1&per_page=20&order=status&direction=desc&match=all" \
    # -H "X-Auth-Email: <email>" \
    # -H "X-Auth-Key: <key>" \
    # -H "Content-Type: application/json"

    cf_zone = 'a5f5672c9471d5fca08912db32d7f1d3'
    cf_auth_key = '55edefc1c418ca263eea896623e6d66c0e4d2'
    cf_email = 'chris@untrod.com'
    url = "https://api.cloudflare.com/client/v4/zones/%s/purge_cache" % cf_zone
    headers = {'X-Auth-Email': cf_email,
               'X-Auth-Key': cf_auth_key,
               'Content-Type': 'application/json'}
    data = {'purge_everything': True}
    requests.delete(url, data=json.dumps(data), headers=headers)


def publish():
    local('make s3_upload')
    print "clearing cache..."
    clear_cache()


def preview():
    """Build production version of site"""
    local('pelican -s publishconf.py')
