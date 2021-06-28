Title: Building Software and Building Bridges
Date: 2012-02-21 14:57
Author: Chris Clark
Slug: building-software-and-building-bridges
Category: Engineering Management
Status: Published

We have a problem. People can't get from one area of town to a
neighboring area because there is a river in between and no road. So
let's build a bridge.

<!-- PELICAN_END_SUMMARY -->

### Step 1: Requirements

We'll get detailed requirements from civil engineers and government
officials, including environmental constraints, safety guidelines,
traffic considerations, and all sorts of other arcana.

### Step 2: Design

We'll have architects, designers, and engineers create a plan that meets
all of the criteria. We'll do a tremendous amount of pre-planning. We'll
take public opinion surveys. We'll invest a huge amount of time and
energy up front to ensure that everyone knows exactly what kind of
bridge we're building and exactly how much it will cost. Our engineers
and designers will have estimates of exactly how many pounds of concrete
we'll need. And how many nails. And which suppliers the nails will be
coming from. And backup nail suppliers in case something happens to the
primary supplier.

### Step 3: Implementation

Contractors go to work. Using the detailed design a team of
professionals can reasonably be expected to deliver this massive project
on time, and on budget. And we have our bridge!

Hmmm...

**Requirements--&gt; Design--&gt; Implementation**

Does that sound familiar? Oh yeah! It's [waterfall
development](http://en.wikipedia.org/wiki/Waterfall_model)! And it
doesn't work for software.

Since the beginning, we've tried to wrap traditional project management
and construction metaphors around software development. It sounds
reasonable - in both cases we have teams of designers and engineers
delivering a very complex, expensive solution over a long period of
time. In the construction world, if we're over budget or late, it's
probably due to some flaw in the requirements or design process. If only
we had invested more time up front! As software projects blow past their
budgets and deadlines
([whoosh](http://www.quotationspage.com/quote/723.html)!), companies
also often react by investing more up front. We get long, detailed
requirements documents that no one reads. Using construction techniques
to solve software problems doesn't work because it's a flawed analogy.

### Let's try that bridge again, but with software

We're going to start by focusing on the problem to solve: get people
from A to B. With software, the solution isn't necessarily as obvious as
it is in the physical world. Maybe we need a bridge. But maybe we need a
ferry. Or a helicopter service. Or maybe we should just move the two
pieces of land closer together. Or freeze the river.

Customers speak in terms of solutions: I want a bridge. I want a bigger
kitchen. But with software we know to be wary of this: unlike the
physical world, the users of software often do not have a good intuitive
understanding of what's possible. So while they speak in terms of
functionality and solutions, it's our job to root out the real problem
and come up with an appropriate solution.

But let's say a bridge is the right answer and we've settled on the
bridge we want to build. It's big, it's complicated. Unlike building a
real bridge, spending lots and lots of time up front on our software
bridge will not lead to accurate estimates for our bridge's
construction. There are lots of reasons for this: programming is
fundamentally an individual task and developers work at dramatically
different levels of productivity. We may not know which developers are
working on our bridge. Or the ones that provide the estimate may not
deliver the parts they estimated.

Furthermore, software complexity increases exponentially with the size
of the project. A 10,000 line program is hundreds of times more complex
than a 1,000 line program. But a 10,000sqft house is linearly more
complex than a 1,000sqft house\*.

The result is we have a unique statistical challenge when estimating
software. Michael Church on Hacker News [explains it
beautifully](http://news.ycombinator.com/item?id=3522910):

> Let's say that you have 20 tasks. Each involves rolling a 10-sided
> die. If it's a 1 through 8, wait that number of minutes. If it's a 9,
> wait 15 minutes. If it's a 10, wait an hour.

> How long is this string of tasks going to take? Summing the median
> time expectancy, we get a sum 110 minutes, because the median time for
> a task is 5.5 minutes. The actual expected time to completion is 222
> minutes, with 5+ hours not being unreasonable if one rolls a lot of
> 9's and 10's.

> This is an obvious example where summing the median expected time for
> the tasks is ridiculous, but it's exactly what people do when they
> compute time estimates, even though the reality on the field is that
> the time-cost distribution has a lot more weight on the right. (That
> is, it's more common for a "6-month" project to take 8 months than 4.
> In statistics-wonk terms, the distribution is "log-normal".)

> Software estimates are generally computed (implicitly) by summing the
> good-case (25th to 50th percentile) times-to-completion, assuming
> perfect parallelism with no communication overhead, and with a
> tendency for unexpected tasks, undocumented responsibilities, and bugs
> to be overlooked outright.

Software teams will not be able to tell you the number of nails needed.
Or the pounds of concrete. Software estimates are unintuitive and must
account for a great degree of uncertainty.

Good software teams use a completely different set of techniques to
battle uncertainty: They ship frequently (there are not many shippable
increments when building a bridge), run lots of experiments, and
integrate the design, implementation, validation, and requirements
phases together into one process. We encourage iterative, creative
thinking. We want to try lots of things, fail fast, and move on. It's
not unusual to read something like this about building software (from
[Little
Bets](http://www.amazon.com/Little-Bets-Breakthrough-Emerge-Discoveries/dp/1439170428)):

> Learn by doing. Fail quickly to learn fast. Develop experiments and
> prototypes to gather insights, identify problems, and build up
> creative ideas, like Beethoven did to in order to discover new musical
> styles and forms.

It's not surprising that the waterfall approach to software has failed.
Waterfall was taken from the world of construction, but construction is
simply not analogous to software. We need new processes.

It's only in the last ten years with the emergence of Agile, Kanban,
rapid prototyping, and general acceptance of iterative, fail-fast
approaches that software development has come into its own. We are good
at building bridges, and we're finally getting good at building
software.

\* <small>I was a little uncomfortable
making this assertion without knowing much about construction, so I
called up a friend who is a project manager for medium/large sized
construction projects (industrial parks, housing developments, etc) and
discussed. He backed the claim.</small>
