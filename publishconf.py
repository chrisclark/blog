#!/usr/bin/env python
# -*- coding: utf-8 -*- #

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'http://blog.untrod.com'
RELATIVE_URLS = False

WEBASSET_DEBUG = False
DEBUG = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
#CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

DISQUS_SITENAME = 'untrodblog'
GOOGLE_ANALYTICS = 'UA-9552542-1'
