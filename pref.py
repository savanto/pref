#!/usr/bin/env python

"""
Preferans for terminal.
"""

import sys
import deck

VERSION = '0.1'

HELP = { 'new': 
"new <pool size> <variant> -- Start a new game.",
         'help': 
"help <command>            -- Show this or help for a given command.",
         'quit': 
"quit                      -- Exit the game." }

BANNER = """\
Preferans for terminal v{}
Type "help" for available commands.""".format(VERSION)

VARIANTS = ['rostov']


def bye(message="\nBye", code=0):
  print(message)
  sys.exit(code)


print(BANNER)
while True:
  try:
    inpt = input("\n> ").lower().strip().split()
  except (EOFError, KeyboardInterrupt):
    bye()

  # help
  if inpt[0] in ['help', 'h', '?']:
    if len(inpt) == 1:
      for item in HELP:
        print(HELP[item])
    else:
      for item in inpt[1:]:
        print(HELP.get(item, "Invalid command: <{}>".format(item)))

  # new
  elif inpt[0] in ['new', 'n']:
    pool_size = 0
    if len(inpt) > 1:
      try:
        pool_size = int(inpt[1])
        assert pool_size > 0
      except (ValueError, AssertionError):
        print("Invalid pool size: <{}>".format(inpt[1]))
    while pool_size <= 0:
      try:
        inpt = input("Pool size: ").strip()
        pool_size = int(inpt)
        assert pool_size > 0
      except (ValueError, AssertionError):
        print("Invalid pool size: <{}>".format(inpt))
      except EOFError:
        break
      except KeyboardInterrupt:
        bye()

    if pool_size > 0:
      if len(inpt) > 2:
        variant = inpt[2] if inpt[2] in VARIANTS else ""
        print("Invalid variant <{}>".format(inpt[2]))
      else:
        variant = ""
      while variant == "":
        try:
          variant = input("Variant {{ {} }}: ".format(', '.join(VARIANTS))).\
              strip().lower()
        except EOFError:
          break
        except KeyboardInterrupt:
          bye()
        if variant not in VARIANTS:
          print("Invalid variant <{}>".format(variant))
          variant = ""

    if pool_size > 0 and variant in VARIANTS:
      print("Pool: {}, Size: {}".format(variant, pool_size))
      print("TODO: start new game")

  # quit
  elif inpt[0] in ['quit', 'q']:
    bye()
  
  # Unknown command
  else:
    print("Not a valid command: <{}>".format(inpt[0]))
