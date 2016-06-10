Title: Extensible, Single-Line Fizzbuzz in a Tweet
Date: 2012-11-01 19:55
Author: Chris Clark
Slug: extensible-single-line-fizzbuzz-in-tweet
Category: Code & Tutorials

Yep, it's a
[fizzbuzz](http://www.codinghorror.com/blog/2007/02/why-cant-programmers-program.html)
blog post! I can hardly believe I've gone this long without ever doing
one.
  
I was thinking about hiring and what I would do if someone asked me
fizzbuzz, and I think I would have used it as an opportunity to show off
some engineering practices. Basically, I'd write unit tests and make it
extensible. Before I knew it this was no longer a thought exercise and I
was fiddling around in IPython Notebook (which is great for this sort of
thing) and created very explicit implementation:

    :::python
    swaps = []
    swaps.append((3, "fizz"))
    swaps.append((5, "buzz"))
    for i in xrange(1,101):  
        out = ""
        for s in swaps:
            if i % s[0] == 0: out = out + s[1]
        if not len(out):
            out = i
        print out


I like this approach because it's reasonably extensible - just add more
tuples to the list of swaps and everything works. Want to print "bazz"
for multiples of 4? Just add swaps.append((4, "bazz")).

But it's pretty boring. As I'm always trying to get better at writing
idiomatic Python, I started swapping in some more Pythonic constructs:

    :::python
    swaps = []
    swaps.append((3, "fizz"))
    swaps.append((5, "buzz"))
    for i in xrange(1,101):
        out = "".join([s[1] if i % s[0] == 0 else "" for s in swaps])
        print out or i

Now of course, I'm hooked and decide I want to shrink it down to fit in
a Tweet. Not terribly difficult, just rename variables, eliminate
spaces, and condense variable declarations:

    :::python
    s=[(3,"fizz"),(5,"buzz")]
    for i in range(1,101):
       o="".join([x[1] if i%x[0]==0 else "" for x in s])
        print o or i
 

And I still have 21 characters to spare. But Twitter doesn't support
linebreaks so if I were to Tweet it, no one could run it without
guessing at the indentation and linebreaks. The semicolon trick almost
works but only gets me this far (the line break after the semicolon is
still required):

    :::python
    s=[(3,"fizz"),(5,"buzz")];for i in range(1,101): o="".join([x[1] if i%x[0]==0 else "" for x in s]);print o or i

This is because Python won't let you inline control flow statements. I
don't want to move the variable declaration inline because it
contradicts any semblance of extensibility still here (I know this is
silly, but ya gotta have yer principles), so I have to get creative.

Instead of a loop, a construct like ``map(lambda, range(1,101))``  will
work. Again though, a  little creativity is in order because
"print" is a statement and can't appear inside a lambda ([only
expressions](http://docs.python.org/2/reference/expressions.html#lambda)
are allowed). Instead I can use ``sys.stdout.write``. Finally, I added a
neat little trick to avoid the if/else (multiplying a string by a
boolean value) and wound up with this functioning, extensible, single
line Fizzbuzz that fits in a Tweet:

    :::python
    s=[(3,"fizz"),(5,"buzz")];map(lambda i: sys.stdout.write("%s\n" % ("".join((i%x[0]==0)*x[1] for x in s) or i)), range(1,101))

Sure there are [shorter
versions](http://stackoverflow.com/a/6890045/221390) out there, but I
had a lot of fun with my version and picked up a couple additional
Python tricks on the way.

(for completeness, if I caved and inlined the variable declaration, I
get this, which is pretty darn short)

    :::python
    for i in range(1,101):print "".join((i%x[0]==0)*x[1] for x in [(3,"fizz"),(5,"buzz")]) or i

