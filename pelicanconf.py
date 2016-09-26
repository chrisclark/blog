#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from datetime import datetime

AUTHOR = u'Chris Clark'
SITENAME = u'untrod.com'
SITEURL = ''

PATH = 'content'
STATIC_PATHS = ['files','images']

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = u'en'

PLUGIN_PATHS = ['plugins']
PLUGINS = ['assets', 'summary']
ASSET_DEBUG = True

DEFAULT_DATE_FORMAT = ('%x')

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()

# Social widget
SOCIAL = (('Github', 'https://www.github.com/chrisclark'),
          ('LinkedIn', 'https://www.linkedin.com/in/chriswclark'),
          ('Flickr', 'https://www.flickr.com/photos/chriscl/'),)

DEFAULT_PAGINATION = 200

THEME = 'theme'

ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}.html'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}.html'
AUTHOR_SAVE_AS = ''
AUTHOR_URL = 'pages/about.html'
DISPLAY_PAGES_ON_MENU = True

DEFAULT_CATEGORY = 'Everything Else'

# Theming

# header & index
NEST_HEADER_LOGO = None
NEST_INDEX_HEAD_TITLE = u'untrod.com'
NEST_INDEX_HEADER_TITLE = u'<small>a blog by</small></br/><a href="pages/about.html">CHRIS CLARK</a>'
NEST_INDEX_HEADER_SUBTITLE = u'Comments on software, technology, and teams.'
NEST_INDEX_CONTENT_TITLE = u'Posts'
# footer.html
NEST_SITEMAP_COLUMN_TITLE = u'Sitemap'
NEST_SITEMAP_MENU = [('Categories','/categories.html'),
                     ('Archives', '/archives.html'),
                     ('About', '/pages/about.html'),]
NEST_SOCIAL_COLUMN_TITLE = u'Social'
NEST_LINKS_COLUMN_TITLE = u'Links'
NEST_COPYRIGHT = '&copy; untrod.com %s<br/>' % datetime.now().strftime('%Y')
NEST_FOOTER_HTML = u'Powered by <a href="http://getpelican.com">Pelican</a> & <a href="https://github.com/molivier/nest">Nest</a>'
# archives.html
NEST_ARCHIVES_HEAD_TITLE = u'Archives'
NEST_ARCHIVES_HEAD_DESCRIPTION = u'Post Archives'
NEST_ARCHIVES_HEADER_TITLE = u'Archives'
NEST_ARCHIVES_HEADER_SUBTITLE = u'Archives for all posts'
NEST_ARCHIVES_CONTENT_TITLE = u'Archives'
# article.html
NEST_ARTICLE_HEADER_BY = u'By'
NEST_ARTICLE_HEADER_MODIFIED = u'modified'
NEST_ARTICLE_HEADER_IN = u'in'
# categories.html
NEST_CATEGORIES_HEAD_TITLE = u'Categories'
NEST_CATEGORIES_HEAD_DESCRIPTION = u'Archives listed by category'
NEST_CATEGORIES_HEADER_TITLE = u'Categories'
NEST_CATEGORIES_HEADER_SUBTITLE = u''
# category.html
NEST_CATEGORY_HEAD_TITLE = u'Category Archive'
NEST_CATEGORY_HEAD_DESCRIPTION = u'Category Archive'
NEST_CATEGORY_HEADER_TITLE = u'Untrod'
NEST_CATEGORY_HEADER_SUBTITLE = u'Archive for Category'
# pagination.html
NEST_PAGINATION_PREVIOUS = u'Previous'
NEST_PAGINATION_NEXT = u'Next'
