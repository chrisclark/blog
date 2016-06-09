Title: How to Improve Chrome Web App Adoption
Date: 2012-01-03 17:51
Author: Chris Clark (noreply@blogger.com)
Slug: how-to-improve-chrome-web-app-adoption

There was big news in the browser world this month, as Google's Chrome
browser [eclipsed Firefox's market
share](http://www.tomshardware.com/news/chrome-firefox-internet-explorer-browser,14147.html),
making is the \#2 most popular browser in the world. Google's goals with
regard to Chrome have always been clear. As Peter Kasting, a founding
member of the Chrome team at Google, [puts it](https://plus.google.com/114128403856330399812/posts/9dKsD7Mi7JU):  
  
"The primary goal of Chrome is to make the web advance as much and as
quickly as possible"  
  
And they've been doing that very effectively, as I've [blogged about
before](http://blog.untrod.com/2011/07/google-chrome-product-strategy.html).  
  
While I don't doubt this as the primary motivation for building the
browser, there are clearly some tangential opportunities that Google is
exploring. For instance, [there is a fascination
theory](http://ipullrank.com/googlebot-is-chrome/) that the Googlebot
(the crawler responsible for maintaining Google's search index) is in
fact running Chrome under the hood in order to index JavaScript and
other dynamic content.  
  
There is also the [Chrome Web
Store](http://en.wikipedia.org/wiki/Chrome_Web_Store), which has emerged
in over the last 12 months as a way for Chrome users to browser through
a (very) lightly curated selection of web "apps" and install them to
Chrome - an app store in the footsteps of Apple, for the browser & web.
The store appears to have about [65 million
users](http://www.chromeosapps.org/) (though it's unclear what counts as
a user) and about 18,000 apps available.  
  
I have some theories about Google's strategic goals of the Chrome store
(in all likelihood it's to support  [Chrome
OS](http://en.wikipedia.org/wiki/Google_Chrome_OS), but it might not be.
What else, say you? To drive Chrome adoption? To turn a profit by
pushing Google Checkout? To simply "advance the web"?) but ultimately we
can make the safe assumption that the success of the Chrome Web Store is
predicated on people installing and using Chrome apps. More app installs
= execution of strategy (whatever it is).  
  
So how is the store doing? With 65 million users, based on Chrome's
\~[25% market share](http://gs.statcounter.com/) and the [2bn worldwide
internet users](http://www.internetworldstats.com/stats.htm), about 13%
of Chrome users have made use of the store. Given how the store works
today I'm actually surprised it's that high, but I'm guessing that
iPhone users' adoption of the Apple app store is close to 100% and that
the Google team is not satisfying mucking around at 13% adoption.  
  
Let's see if we can help them out.  
  
But first, it's worth noting that there are really easy ways to drive
Chrome app adoption: aggressively promote the store from within Chrome
itself, show app results in Google search results, and in general
promote the store across Google properties. However Google has wisely
resisted such cheap promotion in the past (edit: [maybe
not](http://searchengineland.com/googles-jaw-dropping-sponsored-post-campaign-for-chrome-106348)),
so this discussion is focused on how the Chrome store can succeed on its
own merits, not on Google marketing it to a captive audience.  
  
So let's try and divine what exactly a "Chrome App" is, versus a
"normal" web app that's just run through the browser. I'll go ahead and
install the ever-present Angry Birds (which over 1m Chrome users have
also done). It's easy enough through the Chrome Store, and here's the
end result:

![chrome-app](http://3.bp.blogspot.com/-YbtPqp66Res/Tv3y4yPT9II/AAAAAAAAACY/fOZRT5FPas8/s1600/chrome+app.png)
I installed Angry Birds!
  
Voilà! I now have an Angry Birds icon available whenever I open a new
Chrome tab.  
  
When I click it, Chrome navigates to http://chrome.angrybirds.com where
I can, surprise, surprise, play Angry Birds. It's worth noting that I
can just as easily hit this URL *without* the Web App installed. In
fact, I can even hit in IE and it works fine.  
  
So what's the big deal? Surely there is something to Chrome Web Apps
other than a handy link on new browser tabs, right? Well, there is. The
difference is near the bottom of the screen, and here's what it says
when I have the app installed:  

![installing-offline](http://3.bp.blogspot.com/-zEwt8dCBZNA/Tv31sIgTL5I/AAAAAAAAACk/X1wzKNGnUr8/s1600/installing+offline.png)
  
Ah-ha! It's installing the offline version. And indeed, without the app
installed, I see this instead:  

![offline-not-available](http://4.bp.blogspot.com/-i-yO5w7383I/Tv310-XsIkI/AAAAAAAAACw/vQD7NoKmAkE/s1600/offline+not+available.png)
  
In fact, it's the same message I see in IE:  

![angry-birds-ie](http://3.bp.blogspot.com/-qcMwM7A2Aes/Tv32GqlH2AI/AAAAAAAAAC8/wd-d5CKxxXI/s1600/angry+birds+IE.png)
  
Hmmm, well that seems...minor. The handy shortcut is fine and good, and
apparently the app also gets access to some local storage, but if that's
it then the store may be in for a lot of comments like this, from
a Google's "[Why You Should Create an
App](http://www.youtube.com/watch?v=yn_imZgWPtc)" video:

![glorified-bookmarks](http://2.bp.blogspot.com/-LpLe-9N7cGk/Tv4twS4w-wI/AAAAAAAAADI/G5uqDv8ccmI/s1600/glorified+bookmarks.png)
  
But Angry Birds is just one example - there must be more, right? Let's
hear from Google directly, which will surely convince us that the app
store is more than a directory of useful web sites.  
  
Here is how Google describes the benefits of a web app, [buried deep in
an FAQ](http://code.google.com/chrome/webstore/faq.html#faq-gen-07):  

> **Why would someone install a web app instead of just using a bookmark
> or typing in a URL?**  
> Installing an app ensures it is launchable from the New Tab Page via
> the Chrome apps launcher. Installing an app also allows you to grant
> it privileges such as unlimited local storage and background pages.

That's pretty much the entirety of Google's explanation of why Chrome
apps exist. Even the way the question is posed makes the apps sound
ridiculous.  
  
To encourage app installs, the benefits of doing so need to be obvious
and tangible. Right now they are neither. There are in fact real
benefits to the app approach, but Google has seemingly little interest
in conveying them to end users. As a result, users view apps as
glorified bookmarks.  
  
The situation for developers is no better. The developer portal
[describes the
problem](http://code.google.com/chrome/apps/docs/index.html) apps solve
as "requests for permission are annoying" (really, this is what it
says). Again, benefits are not spelled out and developers are left
guessing as to why, exactly, they would make an app.  
  
Ask an iOS developer what the benefits of a native app are (even shimmed
HTML5 apps made with technologies like PhoneGap). They'll say:  

-   Frictionless purchasing
-   In-app payments
-   Rich APIs
-   Exposure via the App Store
-   Available offline/no network lag
-   (and yes) Elevated permissions

In fact, Chrome Apps offer many of the same benefits but they are poorly
explained to both users and developers. Paid apps, integrated with
Google Wallet, [are
available](https://chrome.google.com/webstore/detail/cgllhajannolhgkllnfpapalgaioobkg)
(albeit poorly adopted - this was literally the only example I could
find after 20 minutes of searching), as is an [in-app payments
API](http://www.youtube.com/watch?v=bAcyP06KqPs).  
  
Google just needs to explain this better. And it's not hard. Here's 10
minutes of effort in [Balsamiq](http://www.balsamiq.com/):  

![chrome-app-benefits](http://1.bp.blogspot.com/-MmHMy-Buu88/TwI_2hxTCJI/AAAAAAAAAD4/FB5v-KK93pw/s1600/chrome+app+benefits.png)
  
Google needs to make the benefits clearer.  
  
But even existing apps are not taking advantage of these benefits. For
instance, [Prezi](http://www.prezi.com/) is a fairly popular
productivity app in the store, with about 50,000 users. As far as I can
tell the app is literally a glorified bookmark, just linking to
Prezi.com. I still have to sign up (create a username and password) for
Prezi.com, and if I want to purchase a paid version I get a form that
looks like this:

![sign-up](http://4.bp.blogspot.com/-3CgocWAcEvQ/TwM7kRYnp6I/AAAAAAAAAEE/PqNfndT4il0/s1600/sign+up.png)
  
Wowza! Lots of form fields! Given that I have installed this as a Chrome
app, shouldn't Prezi know something about who I am, and have some sort
of access to my data? At best, signing up should be a one-click process
(similar to purchasing an app in the first place) and at worst, couldn't
it at least have an account already created for me and pre-populate some
of the fields? It's unclear to me how much of this is possible with the
current APIs, but this type of thing should be the default, expected
behavior for anything installed as an application (and only applications
that take advantage of the benefits of being an app should be featured
in the store). Rapid, secure registration and payment are clear benefits
to both users and developers of apps.  
  
If I *haven't* installed Prezi as an app, Google should allow developers
to easily incorporate the "Add to Chrome" button to their site, which
would allow the site to then take advantage of easy registration and
payment options. Imagine if, above all of those Prezi registration
fields, there was a button:

![add-to-chrome-button](http://4.bp.blogspot.com/-E6Vtyf11ppQ/TwM8usR2uJI/AAAAAAAAAEQ/7WKgqskQjlI/s1600/add+to+chrome+button.png)
  
A user could then choose between simply clicking this button, or filling
out then entire form. I'd click the button every time for rapid, safe,
and centralized payment and registration.  
  
Finally, the store itself needs better curation. Browsing around the
Games category, it seems half of the games are simply links to [little
Flash
games](http://www.chromegamebox.com/sports/sports201112098608.html)
surrounded by ads - hardly the slick HTML5 "apps" Google wants to
promote. With a higher threshold for quality, and some improved
discovery features, the store could quickly become a great way to find
new services.  
  
In conclusion, the Chrome store has great potential but needs to make
changes to avoid becoming nothing more than a cool bookmarking service.
Specifically:

-   Make the benefits of apps clearer to users and developers
-   Create better registration and payment APIs, and help developers
    incorporate them into existing services
-   Create an Add to Chrome button that can be used outside of the store
    itself
-   Improve quality and discoverability of apps in the store
  
I look forward to see how store adoption grows, and how this new take on
the app concept plays into Google's larger strategy and offerings.
