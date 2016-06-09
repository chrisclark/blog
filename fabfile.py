from fabric.api import *
import fabric.contrib.project as project
import os
import shutil
import sys
import SocketServer
from livereload import Server
from pelican import Pelican
from pelican.settings import read_settings

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'
DEPLOY_PATH = env.deploy_path

# Remote server configuration
production = 'root@localhost:22'
dest_path = '/var/www'

# Port for `serve`
PORT = 8000

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
    p = Pelican(read_settings('pelicanconf.py'))

    def compile():
        try:
            p.run()
        except SystemExit as e:
            pass

    server = Server()
    server.watch('content/', compile)
    server.serve(root='output')

def push():
    local('make s3_upload')

def preview():
    """Build production version of site"""
    local('pelican -s publishconf.py')
