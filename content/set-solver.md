Title: Set Solver: Ruining My Favorite Card Game
Date: 2016-09-04 11:54
Author: Chris Clark
Status: Draft
Slug: set-solver-in-python

Set is a classic pattern-matching card game that's been around since the 1970s, but really took off in the 90s. It hits all the right marks for a great game casual game; easy to learn, works for any number of players, you can play for 5 minutes or for hours, little equipment required, and it's always competitive.

Here's how it works: using a special set of 81 cards, deal 12 at random, face up. Each card is has a unique combination of 4 attributes: Color, shape, fill, and number, each of which has three different possible values. So after dealing you get something like this:

![dealing-set]({filename}/images/set.png)

Players shout "set!" when they identify a "valid set". A valid set consists of exactly three cards, for which each of the four attributes are either *all the same* or *all different*. So here's a valid set from the deal above:

![dealing-set]({filename}/images/set.png)

You can see that, for each of the four attributes, all the cards either completely match or are completely different.

| Attribute | Card 1   | Card 2   | Card 3   | Set       |
|-----------|----------|----------|----------|-----------|
| Number    | 3        | 2        | 1        | Different |
| Fill      | Lined    | Open     | Solid    | Different |
| Color     | Green    | Red      | Purple   | Different |
| Shape     | Squiggle | Squiggle | Squiggle | Same      |

If you were to change any attribute on any of the cards in the set, you'd have some attribute for which 2 cards matched, and the third different, thus making it an invalid set. When someone finds a set, you remove it, and deal three new cards in their place. You go through the entire deck until there are <=12 cards left, with no more sets. Whoever claimed the most sets wins.

The rules are very simple, but the fun comes from staring at the cards as they are dealt, frantically trying to find sets before you opponent. According to the official website, In a given 12 card deal,

    :::python
    from collections import namedtuple
    from itertools import combinations

    attributes = ['number', 'fill', 'color', 'shape']
    Card = namedtuple('Card', ','.join(attributes))

    def all_same_or_all_different(elems):
        return len(set(elems)) in [len(elems), 0]

    def is_set(a,b,c):
      for atr in attributes:
        vals = [getattr(a, atr), getattr(b, atr), getattr(c, atr)]
        if not all_same_or_all_different(elems):
            return False
      return True

    def find_sets(cards):
        checks = combinations(cards, 3)
        for c in checks:
            if is_set(*c):
                print c

    def make_cards(card_string):
        return [Card(*definition) for definition in card_string.split(',')]

    card_definition = '2ors,2srd,3opd,3lpd,3lgs,2lrs,2lpo,2sps,1opo,1sps,2lro,1lgd'

    find_sets(make_cards(card_definition))
