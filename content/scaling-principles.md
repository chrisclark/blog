Title: Guidepost - Scaling Principles
Date: 2022-04-09
Author: Chris Clark
Slug: guidepost-scaling-principles
Category: Guideposts
Status: Published

Distributed systems are hard. We should exhaust many options before the solution is “do something distributed”. This is also why we are fine creating services, but are not advocates of “micro services”.

Similarly, in most cases we should exhaust vertical scaling before moving to horizontal. It’s almost always less expensive to buy a larger box than it is to staff a complex distributed systems project. In a business like Grove’s, we should make prudent financial decisions with our tech choices, but ultimately the economic drivers of the business are elsewhere — not in technology OpEx. Note that other companies, mostly SaaS companies that are, on some level, reselling infrastructure; Mixpanel, Segment, etc, do have tech OpEx as a key part of cost structure. It’s just not the case here.

We believe that better code can address a lot of scaling challenges; it’s just a website selling soap, after all. While we are “at scale” from a revenue standpoint, we are relatively low-volume in the scheme of web applications, simply because of the size and access patterns of our customers. This is not to trivialize the complexity of scaling, but we believe that, at this stage, the answer is more likely to be “create a better data model with smarter caching” rather than “shard the database”.
