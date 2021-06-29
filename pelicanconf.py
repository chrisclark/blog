#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from datetime import datetime

AUTHOR = 'Chris Clark'
SITENAME = 'Chris Clark'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/Los_Angeles'

PLUGIN_PATHS = ['plugins']
PLUGINS = ['pelican.plugins.webassets', 'summary']

DEFAULT_LANG = 'en'
DEFAULT_DATE_FORMAT = ('%x')
DEFAULT_METADATA = {
    'status': 'draft',
}

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

DEFAULT_PAGINATION = 15

THEME = 'theme'

ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}.html'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}.html'
AUTHOR_SAVE_AS = ''
AUTHOR_URL = 'pages/about.html'
DISPLAY_PAGES_ON_MENU = True

DEFAULT_CATEGORY = 'Everything Else'

S3_BUCKET = 'blog.untrod.com'
AWS_PROFILE = 'blog'

# Theming

# header & index
NEST_HEADER_LOGO = None
NEST_INDEX_HEAD_TITLE = 'untrod.com'
NEST_INDEX_HEADER_TITLE = 'untrod.com'
NEST_INDEX_HEADER_SUBTITLE = 'Comments on software, technology, and teams.'
NEST_INDEX_CONTENT_TITLE = 'Posts'
# footer.html
NEST_SITEMAP_COLUMN_TITLE = 'Sitemap'
NEST_SITEMAP_MENU = [('Categories','/categories.html'),
                     ('Archives', '/archives.html'),
                     ('About', '/pages/about.html'),]
NEST_SOCIAL_COLUMN_TITLE = 'Social'
NEST_LINKS_COLUMN_TITLE = 'Links'
NEST_COPYRIGHT = '&copy; untrod.com %s<br/>' % datetime.now().strftime('%Y')
NEST_FOOTER_HTML = u'Built with<br><a href="http://getpelican.com">Pelican</a> & <a href="https://github.com/molivier/nest">Nest</a>'
# archives.html
NEST_ARCHIVES_HEAD_TITLE = 'Archives'
NEST_ARCHIVES_HEAD_DESCRIPTION = 'Post Archives'
NEST_ARCHIVES_HEADER_TITLE = 'Archives'
NEST_ARCHIVES_HEADER_SUBTITLE = 'Archives for all posts'
NEST_ARCHIVES_CONTENT_TITLE = 'Archives'
# article.html
NEST_ARTICLE_HEADER_BY = 'By'
NEST_ARTICLE_HEADER_MODIFIED = 'modified'
NEST_ARTICLE_HEADER_IN = 'in'
# categories.html
NEST_CATEGORIES_HEAD_TITLE = 'Categories'
NEST_CATEGORIES_HEAD_DESCRIPTION = 'Archives listed by category'
NEST_CATEGORIES_HEADER_TITLE = 'Categories'
NEST_CATEGORIES_HEADER_SUBTITLE = ''
# category.html
NEST_CATEGORY_HEAD_TITLE = 'Category Archive'
NEST_CATEGORY_HEAD_DESCRIPTION = 'Category Archive'
NEST_CATEGORY_HEADER_TITLE = 'Untrod'
NEST_CATEGORY_HEADER_SUBTITLE = 'Archive for Category'
# pagination.html
NEST_PAGINATION_PREVIOUS = 'Previous'
NEST_PAGINATION_NEXT = 'Next'
