#!/usr/bin/env python

"""
Initialize and shuffle the deck, and deal three hands and the blind.
"""

from random import randint

S = 0; C = 1; D = 2; H = 3
J = 11; Q = 12; K = 13; A = 14
SUIT = 0; RANK = 1

SUITS = { 'en':      ['s', 'c', 'd', 'h', '*'],
          'ru':      ['п', 'т', 'б', 'ч', '*'],
          'u_black': ['\u2660', '\u2663', '\u2666', '\u2665', '\u2010'],
          'u_white': ['\u2664', '\u2667', '\u2662', '\u2661', '\u2010'],
          'u_bw':    ['\u2660', '\u2663', '\u2662', '\u2661', '\u2010'],
          'u_wb':    ['\u2664', '\u2667', '\u2666', '\u2665', '\u2010'] }

FACES = { 'en':      ['J', 'Q', 'K', 'A'],
          'ru':      ['В', 'Д', 'К', 'Т'] }


class Deck(object):
  """
  Consists of list of tuples representing cards. Helper functions to shuffle
  and deal cards.
  """
  def __init__(self):
    self.cards = []
    for suit in range(4):
      for rank in range(7, 15):
        self.cards.append((suit, rank))


  def __str__(self):
    return ' '.join("{} {}".format(SUITS['u_wb'][c[SUIT]],
      FACES['en'][c[RANK]-11] if J <= c[RANK] <= A else str(c[RANK])) \
          for c in self.cards)


  def shuffle(self, times=7):
    """
    Rebuilds the card list at random the given number of times.
    """
    for t in range(times):
      sh = []
      while len(self.cards) != 0:
        c = randint(0, len(self.cards)-1)
        sh.append(self.cards[c])
        del self.cards[c]
      self.cards = sh


  def deal(self):
    """
    Deals two cards at a time, as per convention. First round of three pairs go
    to the players, then a single pair of cards is set aside as the blind, then
    the remaining cards are given out in pairs to the rest of the players.
    """
    self.shuffle()
    hands = []
    # First round, includes the blind as the fourth pair dealt
    for i in range(4):
      j = i*2
      hands.append(self.cards[j:j+2])
    # Subsequent rounds 2-5, only dealt to three hands
    j = 0
    for i in range(8, 32, 2):
      hands[j] += self.cards[i:i+2]
      j = (j + 1) % 3
    return [ Hand(h) for h in hands[:3] ], Hand(hands[-1])


class Hand(object):
  """
  The cards belonging to a single player (or the blind), segregated by suit and
  sorted.
  """
  def __init__(self, cards, order_asc=True):
    # Arrange cards by suit
    self.cards = [[], [], [], []]
    for c in cards:
      self.cards[c[SUIT]].append(c)
    for hand in self.cards:
      hand.sort()
      if order_asc:
        hand.reverse()


  def __str__(self):
    return ' '.join(' '.join("{} {}".format(SUITS['u_wb'][c[0]],
      FACES['en'][c[1]-11] if J <= c[1] <= A else c[1]) for c in s)
        for s in self.cards if len(s) != 0)
    """
    hand = ""
    for s in range(4):
      hand += "{} ".format(SUITS['u_wb'][s]) + \
          ','.join(FACES['en'][c[RANK]-11] if J <= c[RANK] <= A else \
          str(c[RANK]) for c in self.cards[s]) + '\n'
    return hand
    """

if __name__ == "__main__":
  d = Deck()
  hands, blind = d.deal()
  for hand in hands:
    print(hand)
  print(blind)
