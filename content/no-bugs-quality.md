Title: No Bugs != Quality
Date: 2012-01-29 19:48
Author: Chris Clark
Slug: no-bugs-quality

A low bug count is not a good indicator of quality software. Lack of
typos and grammatical errors is not indicative of a quality book.  
  
If your software has nagging "quality problems", driving the open bug
count to zero probably won't be much help (not least because it only
addresses the bugs you've found - not the multitude inevitably lurking
in obscure code paths). If the software is hard to use; if it doesn't
solve the problem it was designed to solve; if it's slow; if you pay a
huge engineering tax whenever you make a change because the code base is
spaghetti; then bug count may not be your problem.  
  
In fact, a high bug count isn't even a reliable indicator of poor
quality. Google Chrome, the world's second most popular browser, has
over [32 *thousand* open
issues](http://code.google.com/p/chromium/issues/list?can=2&q=&colspec=ID+Pri+Mstone+ReleaseBlock+Area+Feature+Status+Owner+Summary&x=mstone&y=owner&cells=tiles).  
  
I'm all for keeping bug counts low - fewer bugs is better than more bugs
- but if you have a large number of infrequently-reported bugs, then bug
count is little more than a vanity metric.   
  
Fixing every outstanding edge-case bugs will not create happy users out
of [net detractors](http://www.netpromoter.com/np/calculate.jsp).
Playing whac-a-mole with bugs is ineffective. Quality issues demand
stepping back and taking [different
approaches](http://www.grahambrooks.com/blog/metrics-based-refactoring-for-cleaner-code/).
Bugs are symptoms, not causes.
