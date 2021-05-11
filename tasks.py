# -*- coding: utf-8 -*-

import os
import shlex
import shutil
import sys
import datetime
import requests
import json

from invoke import task
from invoke.main import program
from invoke.util import cd
from pelican import main as pelican_main
from pelican.server import ComplexHTTPRequestHandler, RootedHTTPServer
from pelican.settings import DEFAULT_CONFIG, get_settings_from_file

SETTINGS_FILE_BASE = 'pelicanconf.py'
SETTINGS = {}
SETTINGS.update(DEFAULT_CONFIG)
LOCAL_SETTINGS = get_settings_from_file(SETTINGS_FILE_BASE)
SETTINGS.update(LOCAL_SETTINGS)

CONFIG = {
    'settings_base': SETTINGS_FILE_BASE,
    'settings_publish': 'publishconf.py',
    's3_bucket': SETTINGS['S3_BUCKET'],
    'aws_profile': SETTINGS['AWS_PROFILE'],
    # Output path. Can be absolute or relative to tasks.py. Default: 'output'
    'deploy_path': SETTINGS['OUTPUT_PATH'],
    # Host and port for `serve`
    'host': 'localhost',
    'port': 8000,
}

@task
def clean(c):
    """Remove generated files"""
    if os.path.isdir(CONFIG['deploy_path']):
        shutil.rmtree(CONFIG['deploy_path'])
        os.makedirs(CONFIG['deploy_path'])

@task
def build(c):
    """Build local version of site"""
    pelican_run('-s {settings_base}'.format(**CONFIG))

@task
def rebuild(c):
    """`build` with the delete switch"""
    pelican_run('-d -s {settings_base}'.format(**CONFIG))

@task
def regenerate(c):
    """Automatically regenerate site upon file modification"""
    pelican_run('-r -s {settings_base}'.format(**CONFIG))

@task
def serve(c):
    """Serve site at http://$HOST:$PORT/ (default is localhost:8000)"""

    class AddressReuseTCPServer(RootedHTTPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(
        CONFIG['deploy_path'],
        (CONFIG['host'], CONFIG['port']),
        ComplexHTTPRequestHandler)

    sys.stderr.write('Serving at {host}:{port} ...\n'.format(**CONFIG))
    server.serve_forever()

@task
def reserve(c):
    """`build`, then `serve`"""
    build(c)
    serve(c)

@task
def preview(c):
    """Build production version of site"""
    pelican_run('-s {settings_publish}'.format(**CONFIG))

@task
def livereload(c):
    """Automatically reload browser tab upon file modification."""
    from livereload import Server

    def cached_build():
        cmd = '-s {settings_base} -e CACHE_CONTENT=True LOAD_CONTENT_CACHE=True'
        pelican_run(cmd.format(**CONFIG))

    cached_build()
    server = Server()
    theme_path = SETTINGS['THEME']
    watched_globs = [
        CONFIG['settings_base'],
        '{}/templates/**/*.html'.format(theme_path),
    ]

    content_file_extensions = ['.md', '.rst']
    for extension in content_file_extensions:
        content_glob = '{0}/**/*{1}'.format(SETTINGS['PATH'], extension)
        watched_globs.append(content_glob)

    static_file_extensions = ['.css', '.js']
    for extension in static_file_extensions:
        static_file_glob = '{0}/static/**/*{1}'.format(theme_path, extension)
        watched_globs.append(static_file_glob)

    for glob in watched_globs:
        server.watch(glob, cached_build)
    server.serve(host=CONFIG['host'], port=CONFIG['port'], root=CONFIG['deploy_path'])

@task
def s3_upload(c):
    """Publish to S3"""
    cmd = 'aws s3 sync "{deploy_path}"/ s3://{s3_bucket} --acl public-read --delete --profile {aws_profile}'.format(
        **CONFIG)
    print(cmd)
    c.run(cmd)

@task
def publish(c):
    """Publish to production via s3 upload"""
    clean(c)
    pelican_run('-s {settings_publish}'.format(**CONFIG))
    s3_upload(c)
    clear_cache(c)

@task
def clear_cache(c):
    ''' Purges the CloudFlare cache.
    Zone was retrieved using:
    curl -X GET "https://api.cloudflare.com/client/v4/zones?name=untrod.com&status=active&page=1&per_page=20&order=status&direction=desc&match=all" \
    -H "X-Auth-Email: <email>" \
    -H "X-Auth-Key: <key>" \
    -H "Content-Type: application/json"
    '''

    cf_zone = os.environ.get('CLOUDFLARE_ZONE')
    cf_auth_key = os.environ.get('CLOUDFLARE_AUTH_KEY')
    cf_email = os.environ.get('CLOUDFLARE_EMAIL')
    url = "https://api.cloudflare.com/client/v4/zones/%s/purge_cache" % cf_zone
    headers = {'X-Auth-Email': cf_email,
               'X-Auth-Key': cf_auth_key,
               'Content-Type': 'application/json'}
    data = {'purge_everything': True}
    requests.delete(url, data=json.dumps(data), headers=headers)


def pelican_run(cmd):
    cmd += ' ' + program.core.remainder  # allows to pass-through args to pelican
    pelican_main(shlex.split(cmd))
