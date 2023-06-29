Title: Using LLMs for Customer Service: Some Thoughts
Date: 2024-06-10
Author: Chris Clark
Slug: using-llms-for-customer-service
Status: Draft


I think "Oh my god I can automate customer service" is one of the first thoughts many operators had when seeing ChatGPT in action for the first time. And I think that will largely become true over time, but there are a handful of challenges in B2B and B2C support that I think will take another year to resolve, before we really see LLM-based support become the norm.

Here's what I've seen so far in terms of what's working, where the problems are, and where we'll end up.

## B2B Businesses

I've been a Looker user for a long time. Looker is a data querying and analysis tool built on top of SQL that allows non-technical users to create drag-and-drop reports. When we get in touch with their support, it's often because we are having some issue modeling a field the way we want, and we need help with LookML (their modelling language) or SQL. Their support folks are quite technical, and can crack open our proprietary Looker repositories to help us track down the problem.

Automating this with today's LLMs seems doable, but faces two major problems:

### 1. Context and domain-specific knowledge.
The state of the art today to deal with domain-specific knowledge is to create a bunch of embeddings, find e.g. the most relevant code files based on the question being asked, and shove it into the LLM prompt alongside the question. This works...ok? But it's a little unclear how you'd do this for a customer support organization. Are you constantly embedding all of your customers' data? Doing it on the fly? I'm just not quite sure how this will work.

### 2. Sending proprietary data off to a 3rd party LLM
I don't really want Looker support sticking big chunks of my code into Bard (Looker is owned by Google - they sure aren't sending it to OpenAI!). That's my code! This will be a blocker for a number of companies.

To solve this, it's conceivable to me that a company like Looker might actually run their own LLM 'locally' on their own hardware. GPT3-quality open-source models are starting to come into their own, and they aren't particularly hard to fine-tune or run. With that said, we're some ways off open-source GPT4 quality models, which are notably better at handling this sort of problem.

The other way this gets resolved is that everyone just gets over it (this seems to be happening for Github Co-pilot) because it is so darn useful to the customer -- they get issues resolved right away!

## B2C Businesses
There are a number of start-ups vying to provide LLM-based support for B2C companies, who seem to be focused on helping agents compose answers to customer inquiries. This strikes me as a totally wrong approach.

In a consumer business, the vast, vast majority of issues have been seen before. Agents are not writing novel responses; they don't need help composing sentences. They are reading the issue, selecting a pre-defined response, customizing it, and taking action to resolve the problem. They are using macros, automation, and tools - not solving problems through english composition.

The magic of LLMs though, is not really in their ability to generate text, it's in their ability to understand it. The ability to confidently map a customer service issue to the correct response and the correct action, is very valuable.

Today, I can set up and run an LLM (on my own hardware - not using openAI) that can do the following:
- Read the support request and select an appropriate response from a set of tempaltes
- Lightly customize the text based on that particular inquiry
- Generate an API call to the endpoint that matches the template (e.g. trigger a refund)
- Escalate to a human if the tone is very angry

Not bad! That's much more useful to me than a writing aid for our agents. I have yet to see that offered commercially though. But I'm sure it's coming. I'll buy it!

With all of these solutions, prompt injection is still potentially problematic, but can be mitigated with good business logic in the API endpoints (e.g. don't give someone a gift card for $1,000,000 just because an authorized LLM said so).

## The merging of features and support

But a completely different paradigm to consider is that we can simply build a huge number of end-user facing features that weren't possible before, that allow cost-efficient self-servicing of most of the issues that would have otherwise resulted in a customer service request.

Most customer service touches (at least in B2C businesses) are really "things that your website doesn't do". I think there's a big opportuntity to use LLMs to rapidly expand the number of actions customers can take on their own, without contacting suppport at all.

For example, I recently saw a demo of a new LLM-based feature in an email marketing platform. Email marketers use a templating language to create emails that will go out to their customers. These templating languages have support for lightweight control-flow like conditions, loops, etc. If a user of this particular solution is having a problem with their template, they can hit a button, describe the problem, and and LLM suggests a fix for their template. Cool! That's not customer service automation - that's just a new feature that wasn't possible before.

I'm not sure if it's apocraphyl or literal, but I have heard that at one point in time Amazon would categorize every customer contact as a software bug. Why wasn't the customer able to solve their problem in a self-service manner?
