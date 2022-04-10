Title: Guidepost - Services & Monoliths
Date: 2022-04-09
Author: Chris Clark
Slug: guidepost-services-and-monoliths
Category: Guideposts
Status: Published

Monoliths are not inherently problematic. Perhaps they are even good! Close coupling is the evil to avoid. With good design, monoliths can avoid tight coupling. Services can also be a valuable tool for achieving this. But the purpose of decreasing coupling is to decrease overall complexity. Therefore a service that decreases coupling, but increases overall complexity (e.g. introduces fiendish distributed systems problems), is to be avoided.

When we say “service” we really mean “a piece of software with a well-defined boundary”, which doesn’t necessarily mean “web service that ships and operates independently of the monolith”.

A more formal definition might be “functionality that is accessed using a prescribed interface and conforms to constraints and policies specified by a service description”. Note this definition does not say “and it needs a separate CI/CD pipeline”.

Services are also a management tool.

Conway’s Law is, broadly, that you ship your org chart; if you are building a compiler, and you have three teams working on it, you’ll get a three-pass compiler. Services are useful through this lens. They create boundaries between pieces of technology so that small teams can operate independently and have ownership of their results.

Create service boundaries when it’s useful to create ownership over a problem domain and when the service decreases net complexity.
