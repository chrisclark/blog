Title: Adventures in Candy Land
Date: 2021-07-23
Author: Chris Clark
Slug: adventures-in-candy-land
Status: Published

I play Candy Land occasionally with my two boys (the six year old gets
it much more than the three year old). It has the strange property of
involving both zero skill and zero agency. There are absolutely no
decisions for the player to make at any point; the outcome of the game
is determined as soon as the cards are shuffled.

This makes it reduce to a game that is about as fun as flipping a
coin, but significantly more fun to hack together in Python one
afternoon and explore. Let's do it!

We'll do a rules refresher in a sec, but first, some simple classes
representing the board, a player, and a "move" object, which doesn't
affect gameplay, but will keep track of each turn so we can analyze
games later.

    :::python
    class Board(object):

        def __init__(self, shortcuts, colors, specials, licorice):
            self.shortcuts = shortcuts
            self.colors = colors
            self.specials = list(specials.keys())
            self.licorice = licorice
            self.spaces = (self.colors * 22)[:128]
            for k, v in specials.items():
                self.spaces.insert(v, k)


    class Player(object):

        def __init__(self, name):
            self.name = name
            self.position = -1


    class Move(object):

        def __init__(self, player, card, new_position):
            self.player = player.name
            self.card = card
            self.new_position = new_position

Now we can create a variety of different Candy Land boards. Here's a
board with full fidelity to the original game (which you can see
[here]({static}/images/candyland1.jpg)). For the morbidly curious, I
got the right indices for the licorice, specials, etc by laying out
the board in a
[spreadsheet]({static}/files/candyland/candy-land-board.csv).

    :::python
    COLORS = list('RPYBOG')
    SPECIALS = {
        'Plumpy': 8,
        'Mr. Mint': 17,
        'Jolly': 42,
        'Gramma Nut': 74,
        'Princess Lolly': 94,
        'Queen Frostine': 103
    }
    LICORICE = [47,85,120]
    SHORTCUTS = {4:58, 33:46}

    board = Board(SHORTCUTS, COLORS, SPECIALS, LICORICE)

    def spc_fmt(i, s):
        if i in board.licorice:
            return '*{}*'.format(s)
        if i in board.shortcuts.keys():
            return '^{}^'.format(s)
        return s

    print([spc_fmt(i, s) for i, s in enumerate(board.spaces)])

Here's our board with some formatting to signify licorice and shortcuts:

    :::python
    ['R', 'P', 'Y', 'B', '^O^', 'G', 'R', 'P', 'Plumpy', 'Y', 'B', 'O', 'G', 'R', 'P', 'Y', 'B', 'Mr. Mint', 'O', 'G', 'R', 'P', 'Y', 'B', 'O', 'G', 'R', 'P', 'Y', 'B', 'O', 'G', 'R', '^P^', 'Y', 'B', 'O', 'G', 'R', 'P', 'Y', 'B', 'Jolly', 'O', 'G', 'R', 'P', '*Y*', 'B', 'O', 'G', 'R', 'P', 'Y', 'B', 'O', 'G', 'R', 'P', 'Y', 'B', 'O', 'G', 'R', 'P', 'Y', 'B', 'O', 'G', 'R', 'P', 'Y', 'B', 'O', 'Gramma Nut', 'G', 'R', 'P', 'Y', 'B', 'O', 'G', 'R', 'P', 'Y', '*B*', 'O', 'G', 'R', 'P', 'Y', 'B', 'O', 'G', 'Princess Lolly', 'R', 'P', 'Y', 'B', 'O', 'G', 'R', 'P', 'Queen Frostine', 'Y', 'B', 'O', 'G', 'R', 'P', 'Y', 'B', 'O', 'G', 'R', 'P', 'Y', 'B', 'O', 'G', '*R*', 'P', 'Y', 'B', 'O', 'G', 'R', 'P', 'Y', 'B', 'O', 'G', 'R', 'P']

Good stuff.

Ok, onto the game! For those of you who have _not_ played Candy Land
recently, you can read the official rules
[here]({static}/files/candyland/cl_rules.pdf), but the most salient
bits are:

- Players draw a cards on each turn and do what the card says. There
  is zero decision making on the part of the player.
- In the original game (which are mirrored in the settings above),
  there are 66 cards; 6 "special character" cards, and 60 color
  cards. There are six colors, with eight "single" and two "double"
  cards in each color. The next block of code we'll look at will
  generate the deck based on the board settings.
- When a player draws a color card, move forward to the next color of
  that space. For double color cards, move to the next-next color of
  that space.
- If the card is a "special character" card, go directly to that space
  (even if it is behind you).
- There are three "licorice" spaces. If you land on one of these, you
  are stuck until you draw that color again. Note that in more recent
  versions the player simply loses a turn on these spaces. We are
  keeping with the old-school "stuck" rules.
- There are two "shortcuts". If you land exactly on one of the
  shortcut spaces, immediately follow the shortcut.
- You win by getting to the "end" of the board (e.g. drawing a color
  that does not appear in front of you).

With that in mind, here is the game code:

    #!python
    class Game(object):

        def __init__(self, players, board):
            self.cards = []
            self.board = board
            self.players = [Player(p) for p in players]

        def create_cards(self):
            return self.board.specials + self.board.colors*8\
                   + [c+c for c in self.board.colors]*2

        def draw(self):
            import random
            if not self.cards:
                self.cards = self.create_cards()
                random.shuffle(self.cards)
            return self.cards.pop()

        def _gets_unstuck(self, card, position):
            return card not in self.board.specials and\
                   card[:1] == self.board.spaces[position]

        def generate_move(self, player, card):
            if player.position in self.board.licorice:
                if not self._gets_unstuck(card, player.position):
                    return Move(player, card, player.position)

            if card in self.board.specials:
                return Move(player, card, self.board.spaces.index(card))

            pos = player.position

            # Loop to handle 'double' color cards
            for x in card:
                try:
                    pos = self.board.spaces.index(x, pos+1)
                    if pos in self.board.licorice:
                        break
                    pos = self.board.shortcuts.get(pos, pos)
                except ValueError as e:
                    pos = None
                    break

            return Move(player, card, pos)

        def _take_turn(self):
            # arguably "too clever by half" way of determining turns
            player = self.players[len(self.cards) % len(self.players)]
            m = self.generate_move(player, self.draw())
            player.position = m.new_position
            return m

        def play(self):
            moves = []
            while m := self._take_turn():
                moves.append(m)
                if m.new_position is None: break
            return moves

With default settings, the 66 cards of the deck are created in the
`create_cards` method.

The core game logic is in `generate_move`: given a card and a player,
we calculate the new position of the player. This is somewhat
interesting and it's the algorithm that must be running inside my
six-year-old's head, and the algorithm that my three-year-old can't
quite get a handle on.

The `play` game loop simply takes turns until the win condition is met
(which happens when the drawn card's position doesn't is not present
in the remainder of the board - see line 40).

Now that we have our game objects, we can play (using the board we
created previously):

    :::python
    players = ['Chris', 'Maggie']
    g = Game(players, board)
    moves = g.play()

We can print out the moves and see what happened. Weirdly, formating
the move well was perhaps the hardest part of this entire exercise.

    :::python
    def fmt_move(i, m, b):
        if m.new_position is None:
            out = "On turn {0}, {1} draws {2} and WINS!"
        elif m.new_position in b.licorice:
            out = "On turn {0}, {1} draws {2} and is stuck on {3}."
        else:
            out = "On turn {0}, {1} draws {2} and moves to {3}."
        return out.format(
            i+1,
            m.player,
            m.card,
            m.new_position if m.new_position is None else m.new_position+1)

    for i, m in enumerate(moves):
        print(fmt_move(i, m, g.board))

Here's the output, eliding over a number of moves for brevity:

    :::text
    On turn 1, Chris draws Plumpy and moves to 9.
    On turn 2, Maggie draws O and moves to 59.
    ...
    On turn 27, Chris draws P and is stuck on 48.
    On turn 28, Maggie draws GG and is stuck on 121.
    On turn 29, Chris draws RR and is stuck on 48.
    On turn 30, Maggie draws R and moves to 127.
    On turn 31, Chris draws R and is stuck on 48.
    On turn 32, Maggie draws Princess Lolly and moves to 95.
    ...
    On turn 49, Chris draws RR and moves to 89.
    On turn 50, Maggie draws R and moves to 127.
    On turn 51, Chris draws Y and moves to 91.
    On turn 52, Maggie draws GG and WINS!

Grr, I lost. Oh well - I'm sure there will be more games...in
fact...we can build a harness to play _many_ games, and see the effect
of the various board components:

    :::python
    def play_games(config, num):
        return [Game(**config).play() for _ in range(num)]

def analyze(name, results):
        from statistics import mean, median
        lengths = list(map(len, results))
        print("Turn stats for {0} '{1}' games:".format(len(lengths), name))
        print("Mean:    {}".format(mean(lengths)))
        print("Median:  {}".format(median(lengths)))
        print("Min/max: {0}/{1}".format(min(lengths), max(lengths)))
        print("")

    PLAYERS = ['Chris']
    NUM_GAMES = 10000

    STANDARD = {
        'players': PLAYERS,
        'board': Board(SHORTCUTS, COLORS, SPECIALS, LICORICE)}

    NO_LICORICE = {
        'players': PLAYERS,
        'board': Board(SHORTCUTS, COLORS, SPECIALS, [])}

    NO_SPECIALS = {
        'players': PLAYERS,
        'board': Board(SHORTCUTS, COLORS, {}, LICORICE)}

    NO_SHORTCUTS = {
        'players': PLAYERS,
        'board': Board({}, COLORS, SPECIALS, LICORICE)}

    analyze('Standard', play_games(STANDARD, NUM_GAMES))
    analyze('No Licorice', play_games(NO_LICORICE, NUM_GAMES))
    analyze('No Specials', play_games(NO_SPECIALS, NUM_GAMES))
    analyze('No Shortcuts', play_games(NO_SHORTCUTS, NUM_GAMES))

Note that these games have only one player (me!) since they are for
analytical purposes (vs. HARD-CORE COMPETITIVE purposes). The results:

    :::text
    Turn stats for 10000 'Standard' games:
    Mean:    38.6897
    Median:  33.0
    Min/max: 4/242

    Turn stats for 10000 'No Licorice' games:
    Mean:    34.5284
    Median:  30.0
    Min/max: 4/178

    Turn stats for 10000 'No Specials' games:
    Mean:    27.6359
    Median:  28.0
    Min/max: 10/74

    Turn stats for 10000 'No Shortcuts' games:
    Mean:    40.6276
    Median:  35.0
    Min/max: 5/210

You now know a deep secret of the universe: that the 'special' cards
in Candy Land on average send players backwards more often than
forwards. My GOD! I always thought they were there to help! Doing some
simple math, we determine:

    :::text
    Impact of licorice: 4.16 turns
    Impact of specials: 11.05 turns
    Impact of shortcuts: -1.94 turns

Shortcuts reduce games by an average of 1.9 turns, while licorice and
specials add to the average lengths of games. Cool!

I, for one, thoroughly enjoyed acquiring this utterly worthless
knowledge. There was never a chance of discovering a "better" way to
play Candy Land as the player has zero agency. But I suppose that's
the joy of Candy Land for small children; a perfectly even chance of
winning against your far more sophisticated, Python-programming
parents.
