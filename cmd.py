#!/usr/bin/env python

"""
"""


VARIANTS = ['rostov']

import sys

def bye(message="\nBye", code=0):
  print(message)
  sys.exit(code)

def new(inpt):
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
      return
    except KeyboardInterrupt:
      bye()

  if pool_size > 0:
    variant = ""
    if len(inpt) > 2:
      if inpt[2] in VARIANTS:
        variant = inpt[2]
      else:
        print("Invalid variant <{}>".format(inpt[2]))
    while variant == "":
      try:
        variant = input("Variant {{ {} }}: ".format(', '.join(VARIANTS))).\
            strip().lower()
      except EOFError:
        return
      except KeyboardInterrupt:
        bye()
      if variant not in VARIANTS:
        print("Invalid variant <{}>".format(variant))
        variant = ""

  if pool_size > 0 and variant in VARIANTS:
    return pool_size, variant


HELP = {
'new':  "new [pool size] [variant] -- Start a new game.",
'help': "help [cmd1] [cmd2] ...    -- Show help for given command(s).",
'quit': "quit                      -- Exit the game."
}

def help(inpt):
  if len(inpt) == 1:
    for item in HELP:
      print(HELP[item])
  else:
    for item in inpt[1:]:
      print(HELP.get(item, "Invalid command: <{}>".format(item)))


DEFAULT_CONFIG = {
'variant':  ["rostov"],
'whist': []
}

def config(inpt):
  pass
