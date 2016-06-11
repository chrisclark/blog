Title: A Simple "Similar Products" Recommendation Engine in Python
Date: 2016-06-09 05:15
Author: Chris Clark
Slug: simple-similar-products-recommendation-engine-in-python
Category: Data Science
Status: draft

Let's pretend we need to build a recommendation engine for an eCommerce web site.

There are basically two buckets your engine will fall into: content-based, or collaborative-filtering.

Content-based systems are the ones that your friends and colleagues all assume you are building; using actual item properties like description, title, price, etc, etc. If you had never thought about recommendation systems before, and someone put a gun to your head, Swordfish-style, and forced you to describe one out loud in 30 seconds, you would probably describe a content-based system. "Uhh, uhh, I'd like, show a bunch of products from the same manufacturer that has a similar description."

You're using the actual attributes of the item itself to recommend similar products. This makes a ton of sense, as it's how we actually shop in the real world. We go into the Toaster-Oven aisle and look at all the toaster ovens, which are probably physically arranged on the shelf according to brand, or price, or ability to also cook a full turkey in under 30 minutes.

But our goal online is probably a little different; it's easy enough for folks to browse the toaster oven category already. What we really want is a recommendation system that drives incremental sales (e.g. sales that would not have happened otherwise). If a customer is looking at the product details page for Harry Potter and the Chamber of Secrets, and your recommended shows Prisoner of Azkaban, and the customer buys it, the data scientists back at Random House HQ should *not* be high-fiving. It's a safe bet that customer already knew there were more than two books in the series and that PoA was *not* an incremental sale.

Thus, the general academic disdain for content-based recommendations. All hail collaborative-filtering! The big idea behind CF is also pretty intuitive; the product someone is most likely to buy, is the product that a bunch of people like you also bought. Sure, this can lead to the Harry Potter situation, but it's much better at making recommendations from futher afield, from deeper in the product catalog. It's more robust against problems like typos ("Harry Pooter" still gets recommended), and when measured in the real world in terms of generating incremental sales, generally beats the pants of content-based systems.

While the big idea is intuitive, there is one aspect that you will definitely have to explain to colleagues many, many times. Pure CF systems have *no knowledge whatsoever* about the products they are recommending! To the system, it's just a giant grid of product IDs and user IDs, representing who bought what. It's deeply counterintuitive that CF algorithms often see no measurable performance improvements when they are hybridized with content-based systems. Surely knowing *something* about the items you are recommending must help a *little*, right?

Nope.

In most cases, essentially 100% of the 'signal' is retrievable from a simple matrix of who bought what.

Great. With that out of the way, who is excited to learn how to build a content-based recommendation engine??? Anyone still here?

They do have their place, I swear! Sometimes you *do* want to tell people about Harry Potter, or automatically curate the toaster-over aisle. Or, more realistically, let them know that if you love Nike Pro Hypercool Fitted Men's Compression Shirt, you might also love the Nike Pro Hypercool Printed Men's Tights. A content-based engine rocks at picking up related products like this, without a bunch of manual curation (those products don't appear together in the 'pants' category, nor in 'shirts').

Ok, let's build it. It's easy. The meat of it is fewer than 10 lines of Python. But before we get to the big reveal and look at the code, let's talk through the approach.

We're going to use a sample dataset of outdoor clothing and products from Patagonia. The data looks like this, and you can view the whole thing (~550kb) [on github](https://github.com/groveco/content-engine/blob/master/sample-data.csv).

    | id | description                                                                 |
    |----|-----------------------------------------------------------------------------|
    |  1 | Active classic boxers - There's a reason why our boxers are a cult favori...|
    |  2 | Active sport boxer briefs - Skinning up Glory requires enough movement wi...|
    |  3 | Active sport briefs - These superbreathable no-fly briefs are the minimal...|
    |  4 | Alpine guide pants - Skin in, climb ice, switch to rock, traverse a knife...|
    |  5 | Alpine wind jkt - On high ridges, steep ice and anything alpine, this jac...|
    |  6 | Ascensionist jkt - Our most technical soft shell for full-on mountain pur...|
    |  7 | Atom - A multitasker's cloud nine, the Atom plays the part of courier bag...|
    |  8 | Print banded betina btm - Our fullest coverage bottoms, the Betina fits h...|
    |  9 | Baby micro d-luxe cardigan - Micro D-Luxe is a heavenly soft fabric with ...|
    | 10 | Baby sun bucket hat - This hat goes on when the sun rises above the horiz...|

That's it; just IDs and text about the product in the form ``Title - Description``. We're going to use a simple Natural Language Processing technique called TF-IDF (Term Frequency - Inverse Document Frequency) to parse through the descriptions, identify distinct phrases in each item's description, and then find 'similar' products based on those phrases.

TF-IDF works by looking at all (in our case) one, two, and three-word phrases (uni-, bi-, and tri-grams to NLP folks) that appear multiple times in a description (the "term frequency") and divides them by the number of times those same phrases appear in _all_ product descriptions. So terms that are 'more distinct' to a particular product ("Micro D-luxe" in item 9, above) get a higher score, and terms that appear often, but also appear often in other products ("soft fabric", also in item 9) get a lower score.

Once we have the TF-IDF terms and scores for each product, we'll use a measurement called cosine similarity to identify which products are 'closest' to each other.

Luckily, like most algorithms, we don't have to reinvent the wheel; there are ready-made libraries that will do the heavy lifting for us. In this case, Python's SciKit Learn has both an TF-IDF and cosine similarity implementation.

And here's the code

    :::python

    import pandas as pd
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import linear_kernel

    predictions = {}
    ds = pd.read_csv(path_to_data_source)
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(ds['description'])
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    for idx, row in ds.iterrows():
        similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
        predictions[str(row['id'])] = [(cosine_similarities[idx][i], ds['id'][i]) for i in similar_indices][1:]

Blammo!

Before we dig through this thin

