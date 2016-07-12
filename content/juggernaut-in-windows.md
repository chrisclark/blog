Title: Juggernaut in Windows
Date: 2012-03-09 19:49
Author: Chris
Slug: juggernaut-in-windows
Category: Code & Tutorials

**Note**: This is an old post, and no longer relevant as Juggernaut is
no longer a thing. Just use
[socket.io](https://github.com/socketio/socket.io/) directly.

I've fallen in love with
[Juggernaut](https://github.com/maccman/juggernaut).

> Juggernaut gives you a realtime connection between your servers and
> client browsers. You can literally push data to clients using your web
> application, which lets you do awesome things like multiplayer gaming,
> chat, group collaboration and more.

It's built on node.js, [socket.io](http://socket.io/), and Redis and
makes implementing PubSub in your web apps super easy. (*How easy is
it?*) This easy:

**Client side** (subscriber)

    :::javascript
    var jug = new Juggernaut;
    jug.subscribe("channel1", function(data){
        alert("New message: " + data);
    });

**Server side** (publisher - I'll use Python, but Ruby is similar)

    :::python
    jug = Juggernaut()
    jug.publish('channel', {'message': 'Hello World!'})

I use Juggernaut to implement real time features in my
[Flask](http://flask.pocoo.org/) application. Flask is a traditional web
framework and not very well suited to real-time. Juggernaut is a great
complement. My development environment is Windows, so I needed to get
Juggernaut running there. It wasn't terribly difficult but there were
enough gotchas that I thought I'd share how it's done (and that it can
be done).
  
This assumes you have [Python 2.7
installed](http://www.python.org/download/releases/2.7.2/). I would not
recommend deploying Juggernaut in production on Windows. Here we go:

- Get Redis
    - [Redis](http://redis.io/) [isn't
    supported](http://redis.io/download) on Windows but there is a great
    native port available that seems to work well enough. I wouldn't run
    it in production, but it's been stable for me in development.
    [Download it here](https://github.com/dmajkic/redis/downloads) and
    extract to a folder anywhere you please.
- Get Node.js
    - Node now supports Windows! Download and install it
    [here](http://nodejs.org/#download).
- Get Juggernaut
    - You'll install [Juggernaut](https://github.com/maccman/juggernaut)
    via the Node Package Manager (npm). Npm is installed by default
    with Node. Open a command window and navigate to the install
    directory for Node (this is ``C:\Program
    Files (x86)\nodejs`` on my machine). Run ``npm install -g juggernaut``
- Get the Python library
    - Armin Ronacher has written a [simple Python
    library](https://github.com/mitsuhiko/python-juggernaut) to connect
    to Juggernaut. Install it by running ``pip install
    juggernaut`` at the Windows
    command line. ([don't have
    pip](http://stackoverflow.com/questions/4750806/how-to-install-pip-on-windows)?)</span>
- Run it!
    - Fire up ``redis-server.exe``
    from the directory that you extracted Redis to.
    - Run juggernaut from a Windows command line (just type ``juggernaut``)
    - Juggernaut helpfully comes with a nice little example
    implementation (index.html). Npm installs it here by default: ``C:\Users\AppData\Roaming\npm\node\_modules\juggernaut\public``
    - Not-so-helpfully, the test
    implementation connects to Juggernaut over port 80, which is silly
    because Juggernaut serves messages over port 8080. So crack open
    that index.html file and change line 37 from "80" to "8080"
    - Next, copy index.html and
    application.js (which is the client side Juggernaut library) to a
    directory in IIS so you can hit it locally. You do need to serve the
    file from a web server - you can't just open the static file in a
    browser because when the sample tries to connect to Juggernaut the
    browser will view it as a cross-domain request and reject it.
    - Now, browse to
    http://127.0.0.1/index.html:
    ![screen1](http://2.bp.blogspot.com/-gnoojdIsbBk/T05OuECnVSI/AAAAAAAAAFM/1Ut0DOb9n3M/s1600/jug_test.png)
    - Almost done! Finally, fire up IDLE (or a python interpreter) and try
    the following. You'll see the message immediately in the client app.
    Cool!
    ![jug_2](http://1.bp.blogspot.com/-n4TvFTCnnDk/T05Q4Pb3QJI/AAAAAAAAAFc/7nWDrQqaolk/s1600/jug_2.png)

Hope this helped some folks. Enjoy your shiny new real-time web component!
