#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'http://blog.untrod.com'
RELATIVE_URLS = False

ASSET_DEBUG = False
DEBUG = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

DISQUS_SITENAME = 'untrodblog'
GOOGLE_ANALYTICS = 'UA-9552542-1'
