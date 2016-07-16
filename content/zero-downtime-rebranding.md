Title: Zero Downtime Rebrand
Author: Chris
Date: July 12, 2016

[Noah Smith](https://github.com/noazark/) and I gave this presentation at the San Francisco Django meetup in March of 2016, shortly after we rebranded ePantry to Grove Collaborative. Here's how we pulled it off.

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-01.png)
_Welcome folks!_

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-02.png)
_That's us_

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-03.png)
_We rebranded on March 8, 2016. Grove is an aspiration brand that speaks to our mission and to our customers. ePantry is a practical brand based in the how's and what's instead of the 'why'. We're leaving ePantry behind. Concretelly, this means a redesign, renaming everything to Grove, and moving from epantry.com to grove.co (we couldn't get the .com)._

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-04.png)
_Pretty standard stuff. The bulk of the company is run via a Django monolith webservice backend, and a single-page backbone app on the frontend. We also have an iOS app that consumes the same Django webservices._

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-05.png)
_Here's what the site used to look like under the ePantry brand._

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-06.png)
_And here's the Grove brand._

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-07.png)
_We did this really, really fast. Note that we got the new design (colors, fonts, logo) only 2 weeks before launch. Ah, startups._

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-08.png)

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-09.png)

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-10.png)
_Cloudflare is awesome. It allowed us to have both epantry.com and grove.co point to the same Heroku app (which can only have a single SSL cert)._

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-11.png)
_Here's how the SSL config works. This is probably a 90% solution, in that if you inspect the certs, you'll see this somewhat janky cloudflaressl cert at the end of the chain, instead of a grove.co cert. We still get the green lock in all browsers._

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-12.png)
_Foreshadowing! We'll be redirecting everyone from epantry.com to the new grove.co domain. Can you guess what bad thing is going to happen?_

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-13.png)
_This is bad. We are a subscription commerce site. The last thing you want to do is log out every single one of your users. That is not a way to help retention during the changeover. Not to mention our emails are going to be coming from a different domain, with less sender reputation, and customers may not recognize them. Password managers also won't be aware of the new domain_

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-14.png)
_This is all Noah! He came up with a great way to keep folks logged in (securely) across domains._

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-15.png)
_It basically operates like an OAuth flow; an anonymous user comes to grove.co, we redirect them to epantry.com, detect that there is an active session, then (on the server) literally copy their session data in the database from the epantry.com session into the new grove.co session, and then finally redirect them to their final destination. The code for this is [available on github](https://www.github.com/groveco/rebrand)._

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-16.png)
_In general (and in addition to the session-exchange middleware) we built middleware to redirect all traffic from the old domain to the new one. However there is some traffic we discovered we should not redirect, and instead wanted served by the requested domain. Spiders can get redirected, but not session-exchanged because they do not reliably store cookies. Webhooks get confused by redirects as well, so we just continue serving any webhooks from the original domain. Eventually, we managed to move all webhooks over to the new domain, but there were enough moving pieces without doing that prior to launch._

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-17.png)
_This caught us by surprise. With all of the redirects in Cloudflare to enforce https and www, then all of the session exchange middleware, the redirects were adding up fast! Combine that with the crazy redirects that some advertising vendors use to track theie links, and you could be pushing the browser limit of 20 redirects (10 in old versions of IE!) pretty quickly. We didn't end up hitting it in practice, but something to watch out for. Not to mention the performance hit._

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-18.png)
_Once all of this was set up, we started testing in the wild in production right away. We added a staff check to the middleware so all employees could kick the tires for a couple of weeks on the new domain and try to flush out any issues. Note that the overall redirect is controlled by a Django setting, which maps to an environmental variable. The idea being that when it came time to launch, we could just flip the switch._

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-19.png)
_We didn't want staff copy-pasting URLs to the new domain accidentally, so we created template tags that make folks very aware, if they were on the new domain prior to launch. Also of note, the Sites framework was totally useless during this entire process since it is designed for totally parallel sites, not a single site living on two domains._

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-20.png)


![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-21.png)
_As mentioned on the timeline, we didn't get the design until late in the game. But that didn't mean we couldn't start work! There was a ron of prep to get ready so that, regardless of how the new design turned out, we could get it implemented fast._

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-22.png)
_The first thing was to clean up the colors. This bash command will find all hex colors in our sass stylesheets so we can see how far we've drifted from a common color palette._

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-23.png)
_Same thing for font styles. We use Foundation and all typography should be coming from a small handful of framework classes and styling that we override with sass settings. In theory we should just not have any matches to this expression if we're doing it right (hint: we were not)._

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-24.png)
_Ugh._

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-25.png)
_It's totally amazing how out of control this stuff can get over a few years of rapid development. This was a great opportunity to go back and clean it up. Look at that reduction in colors! And they are all in well-names sass variables for easy resuse. One thing we would strongly encourage for anyone embarking on a project like this is to force their designers to be really consistent with the colors in their mocups. It's easy to say "here's the new palette" but then have subtle differences in different mocked screenshots. That led to a lot of confusion on a short timeline._

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-26.png)

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-27.png)
_Holy moly is font licensing more complex than I anticipated. I'm not really joking when I say "I'm pretty sure you are allowed to read thi." I'm not entirely sure the font license for that title font ("Archer") covers use in a presentation like this. And all of these screenshots are real, from a SINGLE font company, that I had to contend with to purchase and use ONE font. Nuts. If we had known this earlier in the process, I would have made a much stronger recommendation that we just stick to what's available in Google Fonts._

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-28.png)
_Not to mention all of the additional infrastructure involved in using fonts from multiple sources. Thanks Adobe Type Cloud -- I didn't USED to have to dedicate IT resources to fonts, when we were using Google, but I sure as hell do now._

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-29.png)
_Go time!_

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-30.png)
_Look at that Git diff! It's bleeding red! That's what you get from cleaning up all that CSS. We deployed all of the server side code weeks in advance of launch. The actual deploy just consisted of a bunch of static assets deploying. We actually did a test deploy at midnight before launch to verify things worked, and then rolled it back. There were probably a handful of very confused night-owl customers. The once piece you can't take back is redirects. Browsers cache them aggressively so if you do have to roll something back, anyone who hit the redirects will still get pointed to your new domain. Redirects are forever._

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-31.png)
_Here's the real checklist I used for go-live. Each department had their own. It stayed fairly organized thanks to Emacs and Org Mode. A bunch of this stuff could have, in theory, been scripted. But it was easy enough to write out really explicit steps and just do them by hand at launch time. Not everything has to be totally automated._

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-32.png)
_These charts are from Librato. We piped a bunch of custom metrics in, including number of requests to each domain, and watched for anomalous HTTP codes. You can see the cutover happen in the top chart, around 6am as traffic moves from epantry.com (green) to the new domain (blue). Smooth sailing!_

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-33.png)
_Customers getting redirected to the new domain for the first time got a full-page model popover introducing them to the new brand. We used cookies to remember if they had seen it and/or dismissed it._

![first-screen]({filename}/images/rebrand-slides/20160330-Rebrand-Django-Meetup-34.png)
_The orange line shows our recurring purchases for the month. The green line is our target budget number. If the rebrand went poorly (if customers either didn't like it, or were confused) then the canary in the coal mine would be a drop off in repurchase rate. But we saw no such thing and stayed precisely on track. Success!_
