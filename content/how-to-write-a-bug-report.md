Title: How to Write a Bug Report
Date: 2013-07-11 00:32
Author: Chris
Slug: how-to-write-bug-report
Category: Engineering Management

Writing good bug reports is the difference between actually seeing your
bug get fixed and sending protracted emails over the course of a week
convincing a developer that there is, in fact, a bug. By far the most
important information you can provide in a bug report are clear
reproduction steps. Here's my guidance on how to write these:

1. Pretend you are writing to someone who has a *very* basic understanding of the product.
2. Now also pretend that this person is an idiot.
3. Tell them, step-by-step, how to reproduce the issue.

So good reproduction steps look like this:

1. Log in as user test@test.com with password "foo" on the live website
2. View the dashboard
3. Note the dollar amount in the "Your subscription plan" area in the
lower left
4. Hit the "pay" button next to that amount

**Expected Result**
"Today's Payment" is populated in step 1 of the checkout form

**Actual Result**
"Today's Payment" is blank

Yes this can be a little tedious, but if you get in the habit of doing
it, it only takes like 30 seconds more per bug, and if it takes longer
it's because it's forcing you to actually reproduce the thing
consistently, which is the whole point in the first place.

And using this numbered, step-wise, idiot-proof format will cut down on
the back-and-forth between you and whoever is fixing the bug by an order
of magnitude. So it's ultimately a huge time saver and a great habit to
get into. You life will contain 25% fewer bugs and developers will hug
you.

Bonus tip: Whenever possible, provide screenshots!
