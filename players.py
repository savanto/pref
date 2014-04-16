#!/usr/bin/env python

"""
"""

from random import randint

# Players
W = 0; E = 1; S = 2

# Bids
PASS = 0
_6S = 1; _6C = 2; _6D = 3; _6H = 4; _6NT = 5
_7S = 6; _7C = 7; _7D = 8; _7H = 9; _7NT = 10
_8S = 11; _8C = 12; _8D = 13; _8H = 14; _8NT = 15
MISERE = 16
_9S = 17; _9C = 18; _9D = 19; _9H = 20; _9NT = 21
_10S = 22; _10C = 23; _10D = 24; _10H = 25; _10NT = 26


# Keys are all lowercase with no whitespace
BIDS = {
    'pass': PASS, 'пас': PASS, '-1': PASS,

    '6s': _6S, '6п': _6S, 's': _6S, 'п': _6S, 'one': _6S, 'раз': _6S, '1': _6S,
    'spades': _6S, 'пика': _6S, 'пики': _6S, '6\u2660': _6S, '6\u2664': _6S,
    '6c': _6C, '6т': _6C, 'c': _6C, 'т': _6C, 'two': _6C, 'два': _6C, '2': _6C,
    'clubs': _6C, 'трефа': _6C, 'трефы': _6C, '6\u2663': _6S, '6\u2667': _6S,
    '6d': _6D, '6б': _6D, 'd': _6D, 'б': _6D, 'three': _6D, 'три': _6D,
    '3': _6D, 'diamonds': _6D, 'буба': _6D, 'бубны': _6D, '6\u2662': _6S,
      '6\u2666': _6S,
    '6h': _6H, '6ч': _6H, 'h': _6H, 'ч': _6H, 'four': _6H, 'четыре': _6H,
    '4': _6H, 'hearts': _6H, 'черва': _6H, 'червы': _6H, '6\u2661': _6S,
      '6\u2665': _6S,
    '6nt': _6NT, '6бк': _6NT, 'nt': _6NT, 'бк': _6NT, 'five': _6NT,
    'пять': _6NT, '5': _6NT, '6NT': _6NT, '6БК': _6NT,
    
    '7s': _7S, '7п': _7S, '6': _7S,
    '7c': _7C, '7т': _7C, '7': _7C,
    '7d': _7D, '7б': _7D, '8': _7D,
    '7h': _7H, '7ч': _7H, '9': _7H,
    '7nt': _7NT, '7бк': _7NT, '10': _7NT,

    '8s': _8S, '8п': _8S, '11': _8S,
    '8c': _8C, '8т': _8C, '12': _8C,
    '8d': _8D, '8б': _8D, '13': _8D,
    '8h': _8H, '8ч': _8H, '14': _8H,
    '8nt': _8NT, '8бк': _8NT, '15': _8NT,

    'misere': MISERE, 'мизер': MISERE, '0': MISERE, '16': MISERE,

    '9s': _9S, '9п': _9S, '17': _9S,
    '9c': _9C, '9т': _9C, '18': _9C,
    '9d': _9D, '9б': _9D, '19': _9D,
    '9h': _9H, '9ч': _9H, '20': _9H,
    '9nt': _9NT, '9бк': _9NT, '21': _9NT,

    '10s': _10S, '10п': _10S, '22': _10S,
    '10c': _10C, '10т': _10C, '23': _10C,
    '10d': _10D, '10б': _10D, '24': _10D,
    '10h': _10H, '10ч': _10H, '25': _10H,
    '10nt': _10NT, '10бк': _10NT, '26': _10NT }

BIDS_FORMAT = {
    PASS: "Pass",
    _6S: "6\u2664", _6C: "6\u2667", _6D: "6\u2666", _6H: "6\u2665", _6NT: "6NT",
    _7S: "7\u2664", _7C: "7\u2667", _7D: "7\u2666", _7H: "7\u2665", _7NT: "7NT",
    _8S: "8\u2664", _8C: "8\u2667", _8D: "8\u2666", _8H: "8\u2665", _8NT: "8NT",
    MISERE: "Misère", 
    _9S: "9\u2664", _9C: "9\u2667", _9D: "9\u2666", _9H: "9\u2665", _9NT: "9NT",
    _10S: "10\u2664", _10C: "10\u2667", _10D: "10\u2666", _10H: "10\u2665",
      _10NT: "10NT" }



class Player(object):
  def __init__(self, ai=False):
    self.ai = ai
    self.hand = None


  def set_hand(self, hand):
    self.hand = hand


  def make_bid(self, turn, bids):
    if self.ai:
      bids[turn] = BIDS_FORMAT[randint(0, 26)]
    else:
      bid = input("Bid > ").replace(' ', '').lower()
      while bid not in BIDS:
        print("Invalid bid <{}>".format(bid))
        bid = input("Bid > ").replace(' ', '').lower()
      bids[turn] = BIDS_FORMAT[BIDS[bid]]


  def ncards(self):
    return sum(len(s) for s in self.hand)
