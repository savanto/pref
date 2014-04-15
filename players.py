#!/usr/bin/env python

"""
"""

class Player(object):
  def __init__(self, computer=False):
    self.computer = computer
    self.hand = None


  def set_hand(self, hand):
    self.hand = hand


