#!/usr/bin/env python

"""
Preferans for terminal.
"""

import sys
import cmd, game

VERSION = '0.1'

BANNER = """\
Preferans v. {}
Type "help" for available commands.""".format(VERSION)



print(BANNER)
while True:
  try:
    inpt = input("\n> ").lower().strip().split()
  except (EOFError, KeyboardInterrupt):
    cmd.bye()

  # help
  if inpt[0] in ['help', 'h', '?']:
    cmd.help(inpt)

  # new
  elif inpt[0] in ['new', 'n']:
    game_params = cmd.new(inpt)
    if game_params != None:
      pool_size, variant = game_params
      game.play(pool_size=pool_size, variant=variant)

  # config
  elif inpt[0] in ['config', 'configure', 'c']:
    cmd.config(inpt)

  # quit
  elif inpt[0] in ['quit', 'q']:
    cmd.bye()
  
  # Unknown command
  else:
    print("Not a valid command: <{}>".format(inpt[0]))
