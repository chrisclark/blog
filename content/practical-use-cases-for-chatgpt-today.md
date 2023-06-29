Title: Early Thoughts on Recent LLM Developments
Date: 2032-04-04
Author: Chris Clark
Slug: practical-use-cases-for-chatgpt
Status: Draft

1. Help writing templates in an email system. Or code gen within a data tool.

2. Automatic copy generation for PDPs (including summarizing reviews)

3. Creating KB articles from call transcripts

4. Scrubbing copy for compliance / consistency

Things that this does not work well for:
1. Dynamically generating personalized content on a website. It's too slow. It's also possibly too expensive. The cardinality of the data you want to operate on has to be e.g. "Products in a catalog" not "customers on a website" (assuming you have lots of customers). GPT3.5 doesn't comply very well with "system" prompts (and is weaker in general) so for anything customer-facing we would presumably want to use GPT4. But it is significantly slower, and expensive. We looked at using GPT-4 to generate personalized content in the background, to be used later in emails -- this sidesteps the "slow" problem, but we needed a significant amount of context injected into the prompts and it quickly became prohibitively expensive (on the order of $0.20 per API call!)
2. Answering questions, chatbot-style. It's too unpredictable.

# Some open questions

## Is GPT4 at some sort of limit? Will quality stop decreasing with more training?

## Context window appears to be the limiting factor for many applications. What will we do about this? A few observations:
1. The 'retrieval' method (e.g. using vector databases) and essentially "making it easy to try and shove the right context into the prompt" is a hack. And it doesn't work in a number of scenarios.
2. Does anyone actually have access to the 32k context size version of GPT4? I haven't heard of anyone getting it.
3. Does RWKV really work? If it has theoretically 'infinite" context length -- why aren't we hearing more about it? What are the real constraints here?
