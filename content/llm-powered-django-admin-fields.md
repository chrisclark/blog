Title: LLM-Powered Django Admin Fields
Date: 2024-06-10
Author: Chris Clark
Slug: llm-chatgpt-powered-django-admin-fields
Status: Draft


## Short version:

We put little buttons next to a bunch of text fields in the Django admin site that allows administrators to generate copy using chatGPT. We also wrapped the underlying prompts in the Django admin so the prompts themselves are editable by e.g. our copy team, who can tweak them, test them, get the best possible results. It's not encapsulated enough to be releasable as a standalone Django app, but much of the code can be re-used if you'd like to do it yourself. Code, and discussion of learnings, is below.

## Long version:

Here are the major constraints in using GPT4 for consumer companies, as I've come to understand them over the past few months:

1. *Trust.* Prompt injection is unsolved, and they have a loose relationship with the truth. So I don't trust them to e.g. answer customer service questions -- but as a tool to comprehend and compose written language, GPT4 is very nearly faultless. It is a terrific copywriter.
2. *Expense.* If you need to call ChatGPT N times, and N="customers on your website", you can't afford it. At Grove, N can be "products in our catalog" or "outbound marketing campaigns", but it can't be any use case that requires writing different copy for each customer. It's too expensive (unless, I suppose, you have a really short prompt).
3. *Speed.* They are too slow to use in-band when e.g. rendering a webpage. I can't block a page from rendering while GPT4 streams output for 30 seconds. LLM-generated content must be created asynchronously, in advance.

Given these constraints,

We at Grove had explored a few different copywriting use cases for personalization -- but the tech is still somewhat limited for consumer-facing applications. It's slow (dynamically generating anything on a web page blocks for an unacceptable amount of time) and it's expensive (generating unqiue content per-person gets pricey in a hurry). As we understood the constraints better, one of our first 'production' use cases was to re-write a particular field on our product detail pages in a 'house style'. Over the years, inconsistencies had crept into bits of copy across a few thousand different product pages. Initially, we wrote a simple script in a Jupyter notebook to generate consistent copy for the problematic field for each product, and bulk-updated the database. Easy enough. It looked something like this (the bulk-update was done separately):

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

And -- good news! Our merchants were quite excited about this. They wanted to do it in other places, with different prompts and different bits of context. The logical next step was to start building this into the software directly. We're a Django shop, and wound up with the following.

## Store Prompts in Django

First up, a simple model to allow admin users to create and edit prompts.

![llm-django-prompts]({static}/images/gpt-django-prompts.png)

```python

class GPTPrompt(CoreModel):
    system_message_template = models.TextField(blank=False)
    human_message_template = models.TextField(blank=False)
    key = models.CharField(blank=False, unique=True, max_length=100)
    model = models.IntegerField(choices=GPT_MODELS, default=GPT3)

    def prompt(self):
        return ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(self.system_message_template),
                HumanMessagePromptTemplate.from_template(self.human_message_template),
            ]
        )

    @property
    def model_name(self):
        return GPT_MODELS[self.model][1]

    def __str__(self):
        return self.key

```

There is a bit of magic to the "key" value, which maps to a hard-coded value on a class that knows to how to inject the proper contextual data for a given prompt.





## Ability to generate text for admin fields

![llm-django-field]({static}/images/gpt-django-textarea.png)

Torturing the Django admin is never particularly fun, but I eventually developed a widget that I could stick next to arbitrary model text fields, and map to different endpoints, corresponding with different ChatGPT prompts. The Widget is simple:

```python
class LLMTextAreaWidget(Textarea):
    template_name = "widgets/llm_text_area_widget.html"

    def __init__(self, req_url, *args, **kwargs):
        self.llm_req_url = req_url
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["llm_req_url"] = self.llm_req_url
        context["widget"]["btn_class"] = f"{name}-generate-btn"
        return context
```

But the corresponding JavaScript is kind of a mess -- but functional. For the sake of brevity, you can find the HTML template (and the JS) [here](https://gist.github.com/chrisclark/902686040fc28481baba69129650a02a).

Under the covers there is a


The views are nothing special:

```python
def believe_text(request):
    resp_text = BelieveLLM(request.GET.get("model_id")).get_text()
    return HttpResponse(json.dumps({"text": resp_text}),
                        content_type="application/json")
```

Simply calling off to a class (in this case BelieveLLM) that builds





![llm-django-prompts]({static}/images/gpt-django-playground.png)
