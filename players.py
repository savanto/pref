#!/usr/bin/env python

"""
"""

# Players
W = 0; E = 1; S = 2

# Bids





class Player(object):
  def __init__(self, ai=False):
    self.ai = ai
    self.hand = None


  def set_hand(self, hand):
    self.hand = hand


  def make_bid(self, turn, bids):
    if self.ai:
      bids[turn] = "Pass"
    else:
      invalid_bid = True
      while invalid_bid:
        inpt = input("Bid> ")
        if inpt == 'pass':
          invalid_bid = False
          bids[turn] = "Pass"


  def ncards(self):
    return sum(len(s) for s in self.hand)
