Title: A Very Painful Bug
Date: 2012-04-01 18:24
Author: Chris Clark (noreply@blogger.com)
Slug: a-very-painful-bug

I'll lead off this post by listing all of the various things I thought
might have caused this bug, and related phrases that I Googled in the
hopes that it will lead some poor soul chasing the same issue to this
post, thus shaving 2-3 points off that person's long-term systolic blood
pressure.

-   Facebook authentication mobile safari crash
-   jQuery mobile Facebook crash mobile safari
-   Mobile safari crash switching windows
-   mobile firebug
-   Mobile safari ios crash logs
-   Understanding ios crash logs
-   ios crash webthread javascript
-   juggernaut crash mobile safari
-   socket.io mobile safari crash

Basically, there is a problem with how Safari handles websocket
connections. It manifests clearly when, on a mobile device, a page
spawns a child window for something like Facebook authentication (or any
Oauth flow). When the browser returns to the parent window after
authenticating, Safari will completely crash - or, at least, most of the
time it will completely crash. In this case there was a frustrating
dependency that made the bug not 100% reproducible.
  
After hours of debugging (you know you're getting desperate when you
resort to binary-searching for the bug by systematically commenting out
half your JavaScript...) and Googling, I found [this comment on
github](https://github.com/LearnBoost/socket.io/issues/193#issuecomment-4177697)
which describes the symptoms perfectly.
  
I was experiencing it specifically with a connection spun up by
[Juggernaut](https://github.com/maccman/juggernaut), which is based on
[socket.io](https://github.com/learnboost/socket.io). The solution in my
case was simple - just prior to making the FB.login() authentication
call, I explicitly close Juggernaut's websocket and unsubscribe the
client from my PubSub channels:

    :::javascript
    jug.io.socket.disconnect();
    jug.unsubscribe("myChannel");

And then reconnect everything when I return from the Facebook auth
call:

    :::javascript
    jug.io.socket.connect();
    jug.subscribe("myChannel", callBackFn);

Works like a charm, though good god it was painful to identify.
