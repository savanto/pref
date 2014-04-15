#!/usr/bin/env python

"""
Preferans for terminal.
"""

import sys
import cmd

VERSION = '0.1'

BANNER = """\
Preferans for terminal v{}
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
    params = cmd.new(inpt)
    if params != None:
      pool_size, variant = params
      print("Pool: {}, Size: {}".format(variant, pool_size))
      print("TODO: start new game")

  # quit
  elif inpt[0] in ['quit', 'q']:
    cmd.bye()
  
  # Unknown command
  else:
    print("Not a valid command: <{}>".format(inpt[0]))
