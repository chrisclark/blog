Title: What does engineering do here?
Date: 2016-06-23
Author: Chris
Slug: what-does-engineering-do-here
Category: Engineering Management
Status: Draft

My company, [Grove Collaborative](https://www.grove.co), is an online
brand and retailer for household consumables. We sell physical
products on the internet, that get shipped from our warehouses to our
customers.

We do not sell technology. We sell soap and toilet paper. In the very
early days (we've been around for 3 years now), we self-identified as
a technology company. It felt like, in Silicon Valley, you have to be
a tech company. Over time though, it became apparent that we're first
and foremore a brand (we make our own products), and then a retailer,
not a software company. We are a Type B company

Given that we don't directly monetize our technology, our engineering
strategy looks a little different than a software company.

What engineering *does* is pretty much what you'd expect:

- We building and maintain the website.
- We create internal tools; for customer service tools, for inventory
  forecasting, for operations.
- We help teams select and implement software systems.

But that's a list of tasks, not a strategy for what part technology
plays in the business. When I try to develop a strategy, I always
return to this quote from chess grandmaster Savielly Tartakower:

> Tactics are what you do when there is something to do; strategy is
> what you do when there is nothing to do.

At Grove, our engineering team has 3 strategic goals.

# 1. Keep Headcount Growth Sublinear to Revenue Growth

Startups are defined by growth. And it's pretty obvioust that, to be
profitable, you can't just scale headcount perfectly in line with
revenue. Every time you double revenue, you can't double headcount. In
a software business, that's so obvious it mostly doesn't come
up. Twice as many users on the website? Better double-click that
'provision more servers' button in the Heroku dashboard!

When you're shipping physical product though, there are a lot more
parts of the business that, left to their own devices, naturally want
to creep headcount in lockstep with the size of the business. It's
hard to move twice as many boxes through the warehouse without twice
as many people doing it. Or service twice as many customer questions
without twice the number of support reps.

Since day 1 we've operated in a capital-constrained environment, so
throwing bodies at problems has never been an option. Better systems
and better tools are the only way to do more with the same. Every time
we hire a new support rep, we measure our ratio of customers:reps and
make sure that it is signficantly higher than it was when we made the
last hire. We started off with one rep able to support about 5,000
customers, and now a single rep supports upwards of 20,000. And we've
done while *increasing* the average number of touches per customer,
not by hiding our contact page.

# 2. Bear 100% of the Technical Risk

The rest of the business has enough to worry about without fearing
that the website might go down. Technical risk always exists, but we
aim to contain it completely within the engineering
organization. There are parts of the business, like marketing, and
merchandising, and design, and white-label product development, that
need to constantly be pushing the boundaries and charting new
territories. Then there are areas like operations, engineering, and
customer support, that need to be excellent day in and day out, and
meet their service level agreements every time.

The latter are dial-tone services. When you pick up the phone, no one
at AT&T headquarters is scrambling to make sure your phone line is
working. You just get a dial tone and it works, every time. When our
marketing team wants to run a campaign, they don't spend time
wondering if operations can ship the boxes, or whether the website can
handle the traffic. They know that when they pick up the phone, the
dial tone will be there.

# 3. Say 'Yes' to the Rest of the Organization

At the risk of making a blanket statement, engineering always seems to
be the long pole in the tent. It certainly has been at every company
I've worked at. And most of hte companies my friends have worked
at. "Engineering says they can't get to it for a couple of week." "We
can't get the engineering cycles." "Engineering said it's impossible."

Too often other departments are forced to go around engineering. At
Grove, the engineering team has the specific goal of saying "yes" to
the rest of the company; for being an accelerant, not a hindrance, to
other departments' ability to move fast. To succeed as a start-up you
need to be opportunistic, and you need to be fast. Last minute
partnership opportunity that requires a new integration? Don't worry,
we'll get it done. A chance to run a timely promotion, but the site
doesn't support that discounting scheme? Let's make it happen.

This aggressive stance affects how we go about building our
applications. Things needs to be decoupled and flexible; quick-n-dirty
hacks sometimes happen, but we work hard to isolate them to one
function or class so they don't pollute the codebase. We make clear to
the rest of the organization what kind of trade-offs are being made in
order to say 'yes', so we have the space to clean things up, refactor,
and improve when we're not under the gun.

I suspect the yes-man approach sounds scary to a lot of engineering
departments, but it can really work. The secret, of course, is that
the only thing that permits speed, is quality. Without a great
automated test suite, how can you refactor or make changes quickly and
with confidence? Without the ability to deploy into production many
times a day, how can you respond in real-time when marketing campaigns
are running? Without well-factored, simple code, how can you make
changes fast enough to make a difference?

Speed and quality are two sides of the same coin; not competing
priorities. In the long term, it turns out you can't actually pick
speed without also picking quality.
