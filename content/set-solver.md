Title: Set Solver: Ruining My Favorite Card Game
Date: 2021-06-28
Author: Chris Clark
Slug: set-solver-in-python

Set is a classic pattern-matching card game that's been around since the 1970s, but really took off in the 90s. It hits all the right marks for a great game casual game; easy to learn, works for any number of players, you can play for 5 minutes or for hours, little equipment required, and it's always competitive.

Here's how it works: using a special set of 81 cards, deal 12 at random, face up. Each card is has a unique combination of 4 attributes: Color, shape, fill, and number, each of which has three different possible values. So after dealing you get something like this:

![dealing-set]({static}/images/set.png)

Players shout "set!" when they identify a "valid set". A valid set consists of exactly three cards, for which each of the four attributes are either *all the same* or *all different*. So here's a valid set from the deal above:

![dealing-set]({static}/images/valid-set.png)

You can see that, for each of the four attributes, all the cards either completely match or are completely different.

| Attribute | Card 1   | Card 2   | Card 3   | Set       |
|-----------|----------|----------|----------|-----------|
| Number    | 3        | 2        | 1        | Different |
| Fill      | Lined    | Open     | Solid    | Different |
| Color     | Green    | Red      | Purple   | Different |
| Shape     | Squiggle | Squiggle | Squiggle | Same      |


If you were to change any attribute on any of the cards in the set, you'd have some attribute for which 2 cards matched, and the third different, thus making it an invalid set. When someone finds a set, you remove it, and deal three new cards in their place. You go through the entire deck until there are <=12 cards left, with no more sets. Whoever claimed the most sets wins.

The rules are very simple, but the fun comes from staring at the cards as they are dealt, frantically trying to find sets before you opponent. I wanted to understand how many sets are likely to be in the first 12 cards that are dealt. In practice, this is a less useful data point than it appears because every time a set is identified, it is removed.

    :::python
    from collections import namedtuple
    from itertools import combinations
    import random

    attributes = ['number', 'fill', 'color', 'shape']
    Card = namedtuple('Card', ','.join(attributes))

    def valid(elems):
        # Members of elems are all the same, or all different
        return len(set(elems)) in [1, len(elems)]

    def is_set(a,b,c):
        return all([
            valid([getattr(a, atr), getattr(b, atr), getattr(c, atr)])
            for atr in attributes
        ])

    def find_sets(cards):
        return [c for c in combinations(cards, 3)
                if is_set(*c)]

    def make_cards():
        numbers = ['1','2','3']
        fills = ['o','s','f'] # open, shaded, filled
        colors = ['p', 'g', 'r'] # purple, green, red
        shapes = ['d', 's', 'o'] # diamond, squiggle, oval
        return [Card(n, f, c, s)
                for n in numbers for f in fills for c in colors for s in shapes]

That's all we need to simulate a large number of set deals, and examine the results:

    :::python
    sets = [len(find_sets(random.sample(make_cards(), 12)))
            for _ in range(100000)]
    print("Avg sets:", sum(sets) / len(sets))
    print("Min sets:", min(sets))
    print("Max sets:", max(sets))

    for x in range(min(sets), max(sets)+1):
        print("{} sets {:.4%} of the time ({} of {})".format(x, sets.count(x) / len(sets), sets.count(x), len(sets)))

The output is:

    Avg sets: 2.78679
    Min sets: 0
    Max sets: 10

    0 sets 3.2360% of the time (3236 of 100000)
    1 sets 14.5530% of the time (14553 of 100000)
    2 sets 25.9080% of the time (25908 of 100000)
    3 sets 27.1880% of the time (27188 of 100000)
    4 sets 18.3200% of the time (18320 of 100000)
    5 sets 7.9440% of the time (7944 of 100000)
    6 sets 2.3180% of the time (2318 of 100000)
    7 sets 0.4510% of the time (451 of 100000)
    8 sets 0.0610% of the time (61 of 100000)
    9 sets 0.0170% of the time (17 of 100000)
    10 sets 0.0040% of the time (4 of 100000)

To build the intuition a bit more, we can plot it:

    :::python
    import matplotlib.pyplot as plt
    plt.plot([x for x in range(min(sets), max(sets)+1)],
             [sets.count(x) for x in range(min(sets), max(sets)+1)])
    plt.show()

We get:

![dealing-set]({static}/images/set-stats.png)

Cool!
