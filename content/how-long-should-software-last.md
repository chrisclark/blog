Title: Guidepost - How Long Should Software Last?
Date: 2022-04-09
Author: Chris Clark
Slug: guidepost-how-long-should-software-last
Category: Guideposts
Status: Published

At each stage of the business, there is a correspondingly appropriate length of time you should plan for your code to last - the horizon of the software’s utility. In the very early stages of a start-up, code may only need to last a few days. “We’ll try it, and if it works, we can rewrite it next week!”.

And for a series B company, it doesn’t make sense to write software that will take the company public, but you also can’t have code breaking at 2x the scale and rewriting every few months.

In a late stage company (where Grove is today), your code should last for about 3 years. If it has to be rewritten within 12 months, then it is not robust enough. If it breaks in 2-3 years due to growth and/or changes in the business, then so be it. You did your job. But of course, this is a floor on utility – not an ask for planned obsolescence. Obviously code that costs the same to create, and lasts longer, is always preferable.

You don’t need to solve for scale problems that aren’t within the current horizon.

Note that experiments are entirely different. We may write a feature experimentally, which, if it works, will need to be re-written to meet our production/lifetime horizon criteria. Earlier in the company’s history we (like many) had a poor track record of actually re-writing these things and would let hacky experiment code live for a long time. We don’t do that anymore. It’s frustrating for the business, to see the “B” variation of a test do really well, and then have to wait multiple sprints to see it scaled out to 100% of customers -- but that’s the price of operational code that has to last for multiple years.
