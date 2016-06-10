Title: A Simple "Similar Products" Recommendation Engine in Python
Date: 2016-06-09 05:15
Author: Chris Clark
Slug: simple-similar-products-recommendation-engine-in-python
Status: draft

Let's pretend we need to build a recommendation engine for an eCommerce web site.

There are basically two buckets your engine will fall into: content-based, or collaborative-filtering.

Content-based systems are the ones that your friends and colleagues all assume you are building; using actual item properties like description, title, price, etc, etc. If you had never thought about recommendation systems before, and someone put a gun to your head, Swordfish-style, and forced you to describe one out loud in 30 seconds, you would probably describe a content-based system. "Uhh, uhh, I'd like, show a bunch of products from the same manufacturer that has a similar description."

You're using the actual attributes of the item itself to recommend similar products. This makes a ton of sense, as it's how we actually shop in the real world. We go into the Toaster-Oven aisle and look at all the toaster ovens, which are probably physically arranged on the shelf according to brand, or price, or ability to also cook a full turkey in under 30 minutes.

But our goal online is probably a little different; it's easy enough for folks to browse the toaster oven category already. What we really want is a recommendation system that drives incremental sales (e.g. sales that would not have happened otherwise). If a customer is looking at the product details page for Harry Potter and the Chamber of Secrets, and your recommended shows Prisoner of Azkaban, and the customer buys it, the data scientists back at Random House HQ should *not* be high-fiving. It's a safe bet that customer already knew there were more than two books in the series and that PoA was *not* an incremental sale.

Thus, the general academic disdain for content-based recommendations. All hail collaborative-filtering! The big idea behind CF is also pretty intuitive; the product someone is most likely to buy, is the product that a bunch of people like you also bought. Sure, this can lead to the Harry Potter situation, but it's much better at making recommendations from futher afield, from deeper in the product catalog. It's more robust against problems like typos ("Harry Pooter" still gets recommended), and when measured in the real world in terms of generating incremental sales, generally beats the pants of content-based systems.

The one unintuitive thing about CF, that you will definitely have to explain to colleagues many, many times, is that pure CF systems have *no knowledge whatsoever* about the products they are recommending! To the system, it's just a giant grid of product IDs and user IDs, representing who bought what. It's deeply counterintuitive that CF algorithms often see no measurable performance improvement when they are hybridized with content-based systems. Surely knowing *something* about the items you are recommending must help a *little*, right?

Nope.

In many cases, essentially 100% of the 'signal' is retrievable from a simple (if large) matrix of who bought what.

Great. With that out of the way, who is excited to learn how to build a content-based recommendation engine??? Anyone still here?

They do have their place, I swear! Sometimes you *do* want to tell people about Harry Potter, or automatically curate the toaster-over aisle. Or, more realistically, let them know that if you love Nike Pro Hypercool Fitted Men's Compression Shirt, you might also love the Nike Pro Hypercool Printed Men's Tights. A content-based engine rocks at picking up related products like this, without a bunch of manual curation (those products don't appear together in the 'pants' category, nor in 'shirts').

Ok, let's build it. It's easy. It's 9 lines of Python. No kidding.

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

Admittedly, I went through that a little fast, so let's back up, talk about the approach, and walk through the code
