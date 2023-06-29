Title: LLM-Powered Django Admin Fields
Date: 2024-06-10
Author: Chris Clark
Slug: llm-chatgpt-powered-django-admin-fields
Status: Draft

## Short version:
We put little buttons next to a bunch of text fields in the Django admin site that allows administrators to generate copy using chatGPT. We also wrapped the prompts that power the fields in a Django model so the prompts themselves are editable by e.g. our copy team, who can tweak them to get the best possible results. It's not encapsulated enough to be releasable as a standalone Django app, but much of the code can be re-used if you'd like to do it yourself. Code, and discussion of learnings, is below.

![llm-django-field]({static}/images/gpt-django-textarea.png)

![llm-django-prompts]({static}/images/gpt-django-prompts.png)

## Long version:

As mind-blowing as state-of-the-art LLMs are under the covers, they are easy as heck to actually use. I wouldn't trust them to answer customer service questions, or even to be particularly accurate when it comes to answering factual questions -- but as a tool to comprehend and compose written language they are very nearly faultless. I have yet to see a grammatical error, and GPT4 in particular has real writing flair and creativity when properly prompted.

We at Grove had explored a few different copywriting use cases -- but the tech is still somewhat limited. It's slow (dynamically generating anything on a web page blocks for an unacceptable amount of time) and it's expensive (generating unqiue content per-person gets pricey in a hurry). As we understood the constraints better, one of our first 'production' use cases was to re-write a particular field on our product detail pages in a 'house style'. Over the years, inconsistencies had crept into bits of copy across a few thousand different product pages. Initially, we wrote a simple script in a Jupyter notebook to generate consistent copy for the problematic field for each product, and bulk-updated the database. Easy enough. It looked something like this (the bulk-update was done separately):

    :::python
    import json, os, requests, openai

    openai.api_key = os.environ.get('OPENAI_API_KEY')

    # Note that the actual prompt was more complex, but you get the idea.
    prompt = """You will receive a description of a consumer product.
        Please write two sentences that will appear on an ecommerce website
        under the heading "Why we believe in this product".

        Write in the first-person plural, and be compelling but not overly verbose.
        """

    # internal API that can get all of our product data as a json blob
    products = requests.get(product_api_url).json()

    def gen_text(p):
        messages= [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f'Here is the product in JSON format: {p}'}
        ]

        resp = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )
        return resp['choices'][0]['message']['content']

    results = [{"pid": p['id'], "copy": gen_text(p)} for p in products]

    with open("output.json", "w") as file:
        json.dump(results, file)

And -- good news! Our merchants were quite excited about this. They wanted to do it in other places, with different prompts and different bits of context. The logical next step was to start building this into the software directly. We're a Django shop, and wound up with something like this:




And indeed it appears that copywriters are the [first casualities](https://www.yahoo.com/lifestyle/chatgpt-took-jobs-now-walk-153907400.html) of GPT-based automation.
