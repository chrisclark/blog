#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Chris Clark'
SITENAME = u'blog.untrod.com'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()

# Social widget
SOCIAL = (('Github', 'https://www.github.com/chrisclark'),)

DEFAULT_PAGINATION = 200

THEME = 'theme'

ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}.html'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}.html'


# Theme settings
# https://github.com/molivier/nest

NEST_HEADER_LOGO = None

NEST_INDEX_HEAD_TITLE = u'blog.untrod.com'
NEST_INDEX_HEADER_TITLE = u'Untrod Software'
NEST_INDEX_HEADER_SUBTITLE = u'Comments on software, technology, and teams, from Chris Clark.'
NEST_INDEX_CONTENT_TITLE = u'Posts'
NEST_COPYRIGHT = "Copyright 2016, Chris Clark"
