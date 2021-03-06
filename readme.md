# Writing blog posts

1. workon blog (or if virtualenv doesn't exist, pip install -r requirements.txt)
2. ``eval $(cat .env | sed 's/^/export /')``
3. Create a new .md file in /content/
4. Run ``invoke livereload`` to build the site, and run an auto-reloading webserver.
5. When you're ready, run ``invoke publish`` to publish to s3 (and reset the CF cache)

Note that using this syntax for code blocks:

    #!python
    print 'Hello World'

prints line numbers, while this:

    :::python
    print 'Hello World'

has no line numbers.

Set up a post like this:

Title: A Very Painful Bug
Date: 2012-04-01 18:24
Author: Chris Clark
Slug: a-very-painful-bug
Category: Engineering Management
Status: Draft <- remove to publish

# To set up on another machine

You'll need to configure s3_cmd, which is required for uploading to
s3: `brew install s3cmd`

Get the AWS access key and secret key, and then ``s3cmd --configure``
(use `/usr/local/bin/gpg` when asked for path to gpg).

You will also need to `pip install requirements.txt` and `brew install
sass/sass/sass`

Set cloudflare environmental variables (see tasks.py for which ones).

# Theme

A modified version of Nest (https://github.com/molivier/nest)

# TODO

- [ ] set up https (needs s3 cert, then enable cloudflare)
