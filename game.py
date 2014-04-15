#!/usr/bin/env python

"""
"""

import cards, players, cmd
from cards import SUIT, RANK

# Players
W = 0; E = 1; S = 2

def play(pool_size=10, variant='rostov'):
  """
  """
  # Initialize new game
  pool_closed = False
  pls = [ players.Player(computer=True),
      players.Player(computer=True),
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

    draw_table(first=first, bidding=True, player=pls[S].hand.cards)
    
    break

def draw_table(first=None, blind=None, bidding=False, tricks=[0,0,0],
    bids=[None,None,None], ncards=[10,10,10], player=None):
  table = """\
W {:<2} {:<9}              E {:<2} {:<6}
----       {:^9}        ----
{:<4}                        {:<4}
{:<4}                        {:<4}
{:<4}                        {:<4}
{:<4}                        {:<4}
{:<4}                        {:<4}
        S {:<2} {:<6}
        ----------------
        {} {}
        {} {}
        {} {}
        {} {}
""".format(1 if first == W else tricks[W] if tricks[W] != 0 else '',
      bids[W] if bids[W] != None else '',
      1 if first == E else tricks[E] if tricks[E] != 0 else '',
      bids[E] if bids[E] != None else '',
    
      str(blind) if blind != None else "☐ ☐ " if bidding else '',

      '☐ ☐ ' if ncards[W] >= 2 else '☐ ' if ncards[W] == 1 else '',
      '☐ ☐ ' if ncards[E] >= 2 else '☐ ' if ncards[E] == 1 else '',
      '☐ ☐ ' if ncards[W] >= 4 else '☐ ' if ncards[W] == 3 else '',
      '☐ ☐ ' if ncards[E] >= 4 else '☐ ' if ncards[E] == 3 else '',
      '☐ ☐ ' if ncards[W] >= 6 else '☐ ' if ncards[W] == 5 else '',
      '☐ ☐ ' if ncards[E] >= 6 else '☐ ' if ncards[E] == 5 else '',
      '☐ ☐ ' if ncards[W] >= 8 else '☐ ' if ncards[W] == 7 else '',
      '☐ ☐ ' if ncards[E] >= 8 else '☐ ' if ncards[E] == 7 else '',
      '☐ ☐ ' if ncards[W] >= 10 else '☐ ' if ncards[W] == 9 else '',
      '☐ ☐ ' if ncards[E] >= 10 else '☐ ' if ncards[E] == 9 else '',
      
      1 if first == S else tricks[S] if tricks[S] != 0 else '',
      bids[S] if bids[S] != None else '',

      cards.SUITS['u_wb'][cards.S],
      ','.join(cards.FACES['en'][c[RANK]-11] if cards.J <= c[RANK] <= cards.A \
          else str(c[RANK]) for c in player[cards.S]) \
          if len(player[cards.S]) != 0 else '-' if player != None else '',
      cards.SUITS['u_wb'][cards.C],
      ','.join(cards.FACES['en'][c[RANK]-11] if cards.J <= c[RANK] <= cards.A \
          else str(c[RANK]) for c in player[cards.C]) \
          if len(player[cards.C]) != 0 else '-' if player != None else '',
      cards.SUITS['u_wb'][cards.D],
      ','.join(cards.FACES['en'][c[RANK]-11] if cards.J <= c[RANK] <= cards.A \
          else str(c[RANK]) for c in player[cards.D]) \
          if len(player[cards.D]) != 0 else '-' if player != None else '',
      cards.SUITS['u_wb'][cards.H],
      ','.join(cards.FACES['en'][c[RANK]-11] if cards.J <= c[RANK] <= cards.A \
          else str(c[RANK]) for c in player[cards.H]) \
          if len(player[cards.H]) != 0 else '-' if player != None else '')

  print(table)



"""
W                     x:10 x:10     E
----------------                    ----------------
s:A,K,J,10,9,8,7                    s:A,K,J,10,9,8,7
c:A,K,J,10,9,8,7                    s:A,K,J,10,9,8,7
d:A,K,J,10,9,8,7                    s:A,K,J,10,9,8,7
h:A,K,J,10,9,8,7                    s:A,K,J,10,9,8,7

                  S
                  ----------------
                  s:A,K,J,10,9,8,7
                  c:A,K,J,10,9,8,7
                  d:A,K,J,10,9,8,7
                  h:A,K,J,10,9,8,7
"""

if __name__ == "__main__":
  play()
