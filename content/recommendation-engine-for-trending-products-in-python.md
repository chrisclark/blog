Title: A Simple Trending Products Recommendation Engine in Python
Date: 2016-12-17
Author: Chris Clark
Slug: recommendation-engine-for-trending-products-in-python.md
Category: Data Science
Status: Draft

Ah, social proof -- that old marketing standby. It's one of those
marketing 'tricks' that isn't really a trick at all; if a bunch of
people really are doing something, then that is legitimate evidence
that there's something to it.

I've learned recently that this applies to product recommendations as
well -- and I didn't recognize it initially, since I had my engineer's
hat on and was focused on 'how' different algorithms worked, rather
than truly understanding what the end result was, and what that meant
to my customers.


I had a chat recently with one of our investors, Paul Martino of
Bullpen Capital, and walked away with a much stronger understanding of
how customers view and interact with on-site product recommendations.

Here are some learnings:

# It's all about the framing

Yahoo! had a name for this phenomenom: The Britney Spears Effect.

Let's say you're reading about this weekend's upcoming NFL
games. Underneath that article are a bunch of additional, recommended
algorithms. In the early 2000s, it turned out just about everyone
wanted to read about Britney Spears. Ev. ery. one.

So you get to the bottom of your NFL game preview and it says "You
might also like:" and then shows you an article about Britney and
K-fed. You feel kind of insulted by the algorithm. Yahoo! thinks I
want to read about Britney Spears??

But instead, what if said "Other people who read this article
read:". Now...huh...ok - I'll click. The framing gives me permission
to click. This stuff matters!

Just like a good catcher can frame a on-the-margin baseball pitch for
an umpire, showing product recommendations on a website in the right
context puts customers in the right mood to buy.

"Recommended for you" -- ick. So the website thinks it knows me, eh?
How about this instead:

"Households like yours frequently buy"

Now I have context. Now I understand. This isn't a retailer shoving
products in front of my face, it's a helpful assemblage of products
that customers just like me found useful. Chock-full of social proof!

# People want narrative

No one cares about the underlying algorithm. The same problem that
affects really complex algorithms in enterprise businesses is present
in consumer-facing, comparatively simple algorithms: humans want
narrative.

# Purchase vs. Navigation

CLick through rates with intent to purchase are 6%. Navigational CTRs
can be closer to 15%.

And navigation can bail out a site with crappy navigation. If the
information hierarchy sucks, and the menu system is confusing...but
you recommend great products, categories, tags, or brands - your users
will use that to navigate instead.

# A great algorithm for social proof

We have a lot of algorithms available to us, and leverage them all
over the site, but wanted something that made sense, had social roof,
and had immediacy on the home page, front and center.

Paul and I landed on the idea of a 'trending products'
recommender. For our site, given the traffic levels and purchase
behavior, 'trending today' seemed to make the most sense (as opposed
to 'trending in the last hour' or 'the last week').

Let's walk through the implementation of a trending products
algorithm. I include a good amount of real sales data here -- though
I've multiplied each dataset by a random integer factor in order to
mask our true sales volumes of any of these products. Since we
normalize all the trends as part of the algorithm, this doesn't affect
any results and gives you, dear reader, actual sample data to look at.

    :::python

    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np

    df = pd.read_csv('sample-sales-data.csv')
    df.sort_values(by=['id', 'age'], inplace=True)

    trends = pd.pivot_table(df, values='count', index=['id', 'age'])

    WINDOWS = {
        'hanning': np.hanning,
        'hamming': np.hamming,
        'bartlett': np.bartlett,
        'blackman': np.blackman,
        'flat': np.ones
    }

    def smooth(series, window_size=9, window=WINDOWS['hamming']):

        # Generate data points 'outside' of x on either side to ensure
        # the smoothing window can operate everywhere.
        ext = numpy.r_[2 * series[0] - series[window_size-1::-1],
                       series,
                       2 * series[-1] - series[-1:-window_size:-1]]

        weights = window(window_size)
        weights[0:window_size/2] = np.zeros(window_size/2)
        smoothed = np.convolve(weights / weights.sum(), ext, mode='same')
        return smoothed[window_size:-window_size+1]  # trim away the excess data


    ID = 19

    trend = np.array(trends[ID])


    smoothed = smooth(
        trend,
        11,
        WINDOWS['hamming']
    )

    def normalize(series):
        return (series - np.median(series)) / np.median(series)

    nsmoothed = normalize(smoothed)
    ntrend = normalize(trend)
    slopes = -(nsmoothed[:-1]-nsmoothed[1:])

    x = np.arange(-len(trend),0)
    plt.plot(x, ntrend, label="Trend")
    plt.plot(x, nsmoothed, label="Smoothed")
    plt.plot(x, np.append([0], slopes), label="Derivative")
    plt.plot(x, [0 for _ in x], label="Baseline")
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title(lookup(ID))
    plt.show()
