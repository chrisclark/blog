Title: Not even close: A sensible-sounding but totally infeasible use of GPT4
Date: 2024-07-10
Author: Chris Clark
Slug: llm-constraints-for-consumer-companies
Status: Draft

Here's a totally reasonable-sounding use cast for GPT4:

A customer answers some questions on a retailer's website, and gets some product recommendations. We'll use GPT4 to write some copy explaining why those products were recommended.

Prompting GPT4 with, for example, the customers' responses, a JSON representation of the products, and a reasonable well-crafted prompt in fact appears to lead to good results. This should make customers feel great!

But this isn't going to work on at all. Not even close. GPT4 too slow, too expensive, and can't be trusted.





A customer comes to the website, answers some questions about themselves, and

Here are the major constraints in using GPT4 (the state of the art at the time of this writing) for consumer companies, as I've come to understand them over the past few months:

1. *Trust.* Prompt injection is unsolved, and they have a loose relationship with the truth. So I don't trust them to e.g. answer customer service questions -- but as a tool to comprehend and compose written language, GPT4 is very nearly faultless. It is a terrific copywriter.
2. *Expense.* If you need to call ChatGPT N times, and N="customers on your website", it can get expensive in a hurry. When N is "products in the catalog" or "outbound marketing campaigns", the costs won't be a factor. But use cases that requires writing different copy for each customer are often too expensive.
3. *Speed.* They are too slow to use in-band when e.g. rendering a webpage. I can't block a page from rendering while GPT4 streams output for 30 seconds.


** Trust

Any use case where the consumer can influence the prompt is *out*. If you are sending input to an LLM, you are already toast. This isn't like SQL injection, where proper input (or even output) sanitization can save you. [Prompt injection is unsolved](https://simonwillison.net/2023/May/2/prompt-injection-explained/). If the feature is literally "check out our LLM" and you are willing to provide a bunhc of caveats a-la Bing Chat -- then go for it. But your idea for an intelligent assistant/chatbot is going to cause more problems than it solves.

And because ChatGPT has a loose relationship with the truth, any consumer-facing generated text should be reviewable by a human before appears for a consumer. Note I said *reviewable*, not *reviewed*. Not everything needs to be reviewed, but it would be a mistake not to make it reviewable, especially for critical copy or content that could create liability.

** Expense

Pricing for GPT4 is done based on token counts, not on API calls. So the number of calls is not the issue per se -- but of course any call has to contain enough context, and generate enough output, to be useful, which puts a floor on the cost per API call.

Let's say a minimally useful GPT4 prompt contains five input sentences and five output sentences, of 20 words each. Estimating that each word is 1.25 tokens, then for 5000 daily users we're looking at $1800 per month. For a given use case that might be a lot or it might be a little, but the point is that API costs are a factor for a large number of use cases.

** Speed

GPT4 is slow. Generating text on-demand is generally going to be unacceptable to consumers. So you have to do it asynchronously. This limits use cases (you can't respond with LLM text to immediate inputs),
