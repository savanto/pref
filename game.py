#!/usr/bin/env python

"""
"""

import cards, players, cmd
from cards import SUIT, RANK
from players import W, E, S

SUITS = cards.SUITS['u_wb']
FACES = cards.FACES['en']
BACK = cards.SUITS['u_wb'][cards.BACK]
TWO_BACKS = "{} {}".format(BACK, BACK)


def play(pool_size=10, variant='rostov'):
  """
  """
  # Initialize new game
  pool_closed = False
  pls = [ players.Player(ai=True),
      players.Player(ai=True),
      players.Player()
    ]
  d = cards.Deck()
  first = W
  turn = W

  # Play
  while not pool_closed:  # TODO: change to keep track of score
    hands, blind = d.deal()
    for i in range(3):
      # Deal in proper order: from first hand onwards
      pls[(i+turn)%3].set_hand(hands[i])

    # Bidding
    bidding = True
    bids = [None, None, None]
    while bidding:
      if not pls[turn].ai:
        draw_table(first=first, bidding=True, bids=bids,# blind=blind,
           hands=[pls[W].ncards(), pls[E].ncards(), pls[S].hand])
      pls[turn].make_bid(turn, bids)
      turn = (turn + 1) % 3


def draw_table(first=None, blind=None, bidding=False, tricks=[0,0,0],
    bids=[None,None,None], hands=[10,10,10]):

  table = """\
W {:<2} {:<9}              E {:<2} {:<6}
----       {:^9}        ----
{:<16}            {:<16}
{:<16}            {:<16}
{:<16}            {:<16}
{:<16}            {:<16}
{:<16}            {:<16}
        S {:<2} {:<6}
        ----------------
        {:<16}
        {:<16}
        {:<16}
        {:<16}
        {:<16}""".format(
      # W tricks/first bid
      1 if first == W else tricks[W] if tricks[W] != 0 else '',
      bids[W] if bids[W] != None else '',

      # E tricks/first bid
      1 if first == E else tricks[E] if tricks[E] != 0 else '',
      bids[E] if bids[E] != None else '',
    
      # Blind (open/closed)
      ' '.join(' '.join("{} {}".format(SUITS[c[SUIT]], FACES[c[RANK]-11] \
          if cards.J <= c[RANK] <= cards.A else c[RANK]) \
          for c in s) for s in blind if len(s) != 0) \
          if blind is not None else TWO_BACKS if bidding else '',

      # W/E cards (open/closed)
      "{} {}".format(SUITS[cards.S], ','.join(FACES[c[RANK]-11] \
          if cards.J <= c[RANK] <= cards.A else \
          str(c[RANK]) for c in hands[W][cards.S]) \
          if len(hands[W][cards.S]) != 0 else '-') \
          if type(hands[W]) is list else TWO_BACKS \
          if hands[W] >= 2 else BACK if hands[W] == 1 else '',
      "{} {}".format(SUITS[cards.S], ','.join(FACES[c[RANK]-11] \
          if cards.J <= c[RANK] <= cards.A else \
          str(c[RANK]) for c in hands[E][cards.S]) \
          if len(hands[E][cards.S]) != 0 else '-') \
          if type(hands[E]) is list else TWO_BACKS \
          if hands[E] >= 2 else BACK if hands[E] == 1 else '',
      "{} {}".format(SUITS[cards.C], ','.join(FACES[c[RANK]-11] \
          if cards.J <= c[RANK] <= cards.A else \
          str(c[RANK]) for c in hands[W][cards.C]) \
          if len(hands[W][cards.C]) != 0 else '-') \
          if type(hands[W]) is list else TWO_BACKS \
          if hands[W] >= 4 else BACK if hands[W] == 3 else '',
      "{} {}".format(SUITS[cards.C], ','.join(FACES[c[RANK]-11] \
          if cards.J <= c[RANK] <= cards.A else \
          str(c[RANK]) for c in hands[E][cards.C]) \
          if len(hands[E][cards.C]) != 0 else '-') \
          if type(hands[E]) is list else TWO_BACKS \
          if hands[E] >= 4 else BACK if hands[E] == 3 else '',
      "{} {}".format(SUITS[cards.D], ','.join(FACES[c[RANK]-11] \
          if cards.J <= c[RANK] <= cards.A else \
          str(c[RANK]) for c in hands[W][cards.D]) \
          if len(hands[W][cards.D]) != 0 else '-') \
          if type(hands[W]) is list else TWO_BACKS \
          if hands[W] >= 6 else BACK if hands[W] == 5 else '',
      "{} {}".format(SUITS[cards.D], ','.join(FACES[c[RANK]-11] \
          if cards.J <= c[RANK] <= cards.A else \
          str(c[RANK]) for c in hands[E][cards.D]) \
          if len(hands[E][cards.D]) != 0 else '-') \
          if type(hands[E]) is list else TWO_BACKS \
          if hands[E] >= 6 else BACK if hands[E] == 5 else '',
      "{} {}".format(SUITS[cards.H], ','.join(FACES[c[RANK]-11] \
          if cards.J <= c[RANK] <= cards.A else \
          str(c[RANK]) for c in hands[W][cards.H]) \
          if len(hands[W][cards.H]) != 0 else '-') \
          if type(hands[W]) is list else TWO_BACKS \
          if hands[W] >= 8 else BACK if hands[W] == 7 else '',
      "{} {}".format(SUITS[cards.H], ','.join(FACES[c[RANK]-11] \
          if cards.J <= c[RANK] <= cards.A else \
          str(c[RANK]) for c in hands[E][cards.H]) \
          if len(hands[E][cards.H]) != 0 else '-') \
          if type(hands[E]) is list else TWO_BACKS \
          if hands[E] >= 8 else BACK if hands[E] == 7 else '',
      '' if type(hands[W]) is list else TWO_BACKS \
          if hands[W] >= 10 else BACK if hands[W] == 9 else '',
      '' if type(hands[E]) is list else TWO_BACKS \
          if hands[E] >= 10 else BACK if hands[E] == 9 else '',
      
      # S tricks/first bid
      1 if first == S else tricks[S] if tricks[S] != 0 else '',
      bids[S] if bids[S] != None else '',

      # S hand (open/closed)
      "{} {}".format(SUITS[cards.S], ','.join(FACES[c[RANK]-11] \
          if cards.J <= c[RANK] <= cards.A else \
          str(c[RANK]) for c in hands[S][cards.S]) \
          if len(hands[S][cards.S]) != 0 else '-') \
          if type(hands[S]) is list else TWO_BACKS \
          if hands[S] >= 2 else BACK if hands[S] == 1 else '',
      "{} {}".format(SUITS[cards.C], ','.join(FACES[c[RANK]-11] \
          if cards.J <= c[RANK] <= cards.A else \
          str(c[RANK]) for c in hands[S][cards.C]) \
          if len(hands[S][cards.C]) != 0 else '-') \
          if type(hands[S]) is list else TWO_BACKS \
          if hands[S] >= 4 else BACK if hands[S] == 3 else '',
      "{} {}".format(SUITS[cards.D], ','.join(FACES[c[RANK]-11] \
          if cards.J <= c[RANK] <= cards.A else \
          str(c[RANK]) for c in hands[S][cards.D]) \
          if len(hands[S][cards.D]) != 0 else '-') \
          if type(hands[S]) is list else TWO_BACKS \
          if hands[S] >= 6 else BACK if hands[S] == 5 else '',
      "{} {}".format(SUITS[cards.H], ','.join(FACES[c[RANK]-11] \
          if cards.J <= c[RANK] <= cards.A else \
          str(c[RANK]) for c in hands[S][cards.H]) \
          if len(hands[S][cards.H]) != 0 else '-') \
          if type(hands[S]) is list else TWO_BACKS \
          if hands[S] >= 8 else BACK if hands[S] == 7 else '',
      '' if type(hands[S]) is list else TWO_BACKS \
          if hands[S] >= 10 else BACK if hands[S] == 9 else '')

  print(table)


if __name__ == "__main__":
  play()
