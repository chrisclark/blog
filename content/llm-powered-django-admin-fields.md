Title: LLM-Powered Django Admin Fields
Date: 2024-04-14
Author: Chris Clark
Slug: llm-chatgpt-powered-django-admin-fields
Status: Published

*Note*: All relevant code can be found in the corresponding [Github repo](https://github.com/chrisclark/django-llm-fields).

I work at Grove -- and ecommerce company that sells thousands of different products. We use Django and the Django admin as our product information system to manage, among other things, all of the copy on our Product Detail Pages (PDPs). In order to more efficiently and consistently write copy for different PDP sections, we integrated ChatGPT directly into the Django Admin.

While not *quite* encapsulated enough to make it standalone Django plugin, the code is generic enough to quickly integrate ChatGPT with any Django text field, and provides a number of affordances to Django admin users to modify and test the underlying prompts.

## What we did

In short, we now have little buttons next to Django Admin text fields that will generate copy according to a specific prompt and data payload. For example, we have a section on our PDPs titled "Why we believe in this product". That's an attribute on the Product model called `why_we_believe`. In the Django Admin, when viewing a Product model, there is a button that our merchandising team can use to populate the field. The text is editable and reviewable; ChatGPT provides initial copy, but humans are still very much in the loop.

![llm-django-field]({static}/images/gpt-django-textarea.png)

Each "LLM-enabled" text field is maped to a specific prompt, and a data payload that provides the model-specific context to ChatGPT.

We also have prompts and buttons for fields like "review summary" (summarizes the pros and cons of a product based on customer reviews), "hero ingredients", and "packaging description". The underlying prompts are editable in the admin as well so users can tweak the copy that ChatGPT is generating without getting in touch with engineering:

![llm-django-prompts]({static}/images/gpt-django-prompts.png)

And a playground area allows admin users to test the prompts out without leaving Django.

![llm-django-prompt-playground]({static}/images/gpt-django-playground.png)

This basic framework allows us to quickly add GPT-powered copywriting to any text field, on any model, in the Django Admin. The relevant code is available in a [Github repo](https://github.com/chrisclark/django-llm-fields), with some instructions on how to get started. The balance of this post simply explicates the code and patterns.

## How it works

Note that some of the code below is slightly simplified from what's in the repo in order to aid comprehension.

First up, a simple model to store and manage the prompts that will power each text field:

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

After registering the model in the Django admin, the prompts are now editable.

![llm-django-prompt-admin]({static}/images/gpt-django-prompt-admin.png)

There is a bit of magic to the "key" value, which maps to a hard-coded value on a class that knows to how to inject the proper contextual data for a given prompt. For example, the prompt in the screenshot above needs to know how to get `product_json`. So we write a little class that can provide that data (one class for each prompt):

```python

class BelievePromptData(object):
    PROMPT_KEY = "WHY_WE_BELIEVE_PROMPT"

    def __init__(self, model_id):
        self.product = Product.objects.get(pk=model_id)

    def __call__(self):
        keys = ["name", "selling_points", "manufacturer_description", "ingredients"]
        return {"product_json": json.dumps({k: str(getattr(self.product, k)) for k in keys})}

```

A single Django view will handle all of the client-side text-generation requests coming from the admin buttons:

```python

def generic_llm_prompt_view(request, promptDataCls=None):
    prompt = GPTPrompt.objects.get(key=promptDataCls.PROMPT_KEY)
    prompt.prompt_data = promptDataCls(request.GET.get("model_id"))
    return HttpResponse(json.dumps({"text": prompt.get_text()}), content_type="application/json")
```

The correct PromptData class is injected when registering the URLs:

```python

from functools import partial

urlpatterns += [
    re_path(r"^generate-believe-text/", partial(generic_llm_prompt_view, promptDataCls=BelievePromptData), name="generate-believe-text"),
]
```

Note in the [repo](https://github.com/chrisclark/django-llm-fields), there are also URLs registered for the playground.

To recap:
1. A request comes in to e.g. `generate-believe-text/?model_id=123`
2. The generic `llm_prompt_view` passes the model_id into the PromptData object specified in the URL endpoint (in this case `BelievePromptData`)
3. `BelievePromptData` gets the relevant model and turns it into the JSON blob that we want to inject into our prompt. The key of the PromptData class maps to the correct GPTPrompt object.
4. The GPTPrompt gets loaded, merges in the JSON blob, and calls out to ChatGPT to generate the text.

This pattern makes it really easy to add more prompts; an admin user can create a new prompt (and test it out in the playground), and an engineer adds a corresponding PromptData class and new URL.


## Hooking up the Django Admin UI

Lastly, we have to add the actual button next to the relevant field. Torturing the Django admin is never particularly fun, so we created a widget you can stick next to arbitrary model text fields, and map to the different URLs, corresponding to the various PromptData classes. The Widget is simple:

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

The corresponding JavaScript is kind of a mess -- but functional. The HTML and JS for the widget can be found in the complete repo.

Then simply add the widget to the admin form. E.g.


```python

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "why_we_believe": LLMTextAreaWidget(req_url="/llm/generate-believe-text/"),
        }
```

And voila! Our merchandisers can click the button to generate text and prepopulate the field. This fields remain a 'normal' text field; it's still overrideable by the admin user. Merchants often use the buttons to get started, and then tweak the copy from there.
