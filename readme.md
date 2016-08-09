# Writing blog posts

1. workon blog (or if virtualenv doesn't exist, pip install -r requirements.txt)
2. ``eval $(cat .env | sed 's/^/export /')``
3. Create a new .md file in /content/
4. Run ``fab dev`` to build the site, and run an auto-reloading webserver.
5. When you're ready, run ``fab publish`` to publish to s3 (and reset the CF cache)

Note that using this syntax for code blocks:

    #!python
    print 'Hello World'

prints line numbers, while this:

    :::python
    print 'Hello World'

has no line numbers.

# To set up on another machine

You'll need to configure s3_cmd, which is required for uploading to s3.

Get the AWS access key and secret key, and then ``s3cmd --configure``

# Theme

A lightly-modified version of Nest (https://github.com/molivier/nest)

# TODO

- [ ] set up https (needs s3 cert, then enable cloudflare)
- [ ] simplify typography (http://devinhunt.github.io/typebase.css/)
