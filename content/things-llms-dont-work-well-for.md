Title: Things LLMs almost work well for, but don't
Date: 2023-05-16
Author: Chris Clark
Slug: things-llms-almost-work-well-for
Status: Draft

Since ChatGPT has burst on the scene, I've run into a large number of business problems and opportunities (within my day job here at Grove) that seem like a good fit for LLMs...but aren't.

Here are three patterns I've seen where a hole may look LLM-shaped, but an LLM solution doesn't quite work.

# High order "N"
Starting off with a boring one: When you need to make LLM calls for a large "n". At Grove, an ecommerce business, we've quickly learned that when n="number of products in our catalog", we can use LLMs (e.g. to help write product detail page copy). But when n="number of customers", the costs are simply prohibitive.

We tried to use LLMs to summarize results from a personalization quiz that our users were taking. Note that we weren't asking the LLM to actually *make* a recommendation, just to write supporting copy. But once we added in all of the context related to how the decision was made, the API calls quickly became unafforable. Costs will come down with time, of course, but we're constraining ourselves to "small N" for now.

In addition to being expensive, GPT models are slow. Even if OpenAI API calls were free, it turns out we *still* couldn't use them to generate personalized copy in reponse to actions on the website because it's just too darn slow. And of course we can't do it asynchronously to be used in emails later, because...it's expensive.

# Taking action based on unsanitized user input

A quick aside on the customer service opportunity with LLMS:




1. Dynamically generating personalized content on a website. It's too slow. It's also possibly too expensive. The cardinality of the data you want to operate on has to be e.g. "Products in a catalog" not "customers on a website" (assuming you have lots of customers). GPT3.5 doesn't comply very well with "system" prompts (and is weaker in general) so for anything customer-facing we would presumably want to use GPT4. But it is significantly slower, and expensive. We looked at using GPT-4 to generate personalized content in the background, to be used later in emails -- this sidesteps the "slow" problem, but we needed a significant amount of context injected into the prompts and it quickly became prohibitively expensive (on the order of $0.20 per API call!)
2. Doing anything that involves taking action based on end-user input. Prompt injection is real and unsolved.

# Some open questions

## Is GPT4 at some sort of limit? Will quality stop decreasing with more training?

## Context window appears to be the limiting factor for many applications. What will we do about this? A few observations:
1. The 'retrieval' method (e.g. using vector databases) and essentially "making it easy to try and shove the right context into the prompt" is a hack. And it doesn't work in a number of scenarios.
2. Does anyone actually have access to the 32k context size version of GPT4? I haven't heard of anyone getting it.
3. Does RWKV really work? If it has theoretically 'infinite" context length -- why aren't we hearing more about it? What are the real constraints here?
