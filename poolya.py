#!/usr/bin/env python

"""
Interactive recording of protocol and calculation of scores.

  USAGE: poolya.py <POOL SIZE> [VARIANT]
"""

# Bids
MISERE = 0; PASS = 1; HWHIST = 2; WHIST = 3; CONTRACT = 4

# Players
#PLAYERS = 3
W = 0; S = 1; E = 2; N = 3

class Pool(object):
  """
  Pool base class. Provides some generic scoring methods, probably similar to
  Lenningrad/Peter or the Sochi variants. This class is meant to be overloaded
  by a specific preferans variant to fine-tune scoring methods.
  Provides default new game initialization, and conversion of the scoresheet
  to string.
  """
  def __init__(self, pool_size=10, players=3, running_tally=True):
    # Scoring constants
    self.CONTRACT_VALUE = { 0: 10, 6: 2, 7: 4, 8: 6, 9: 8, 10: 10 }
    self.WHIST_OBLIGATION = { 6: 4, 7: 2, 8: 1, 9: 1, 10: 1 }
    self.WHIST_COEFF = 1
    self.WHIST_REMISE_COEFF = 1
    self.AID_WHIST_VALUE = 10
    self.HILL_WHIST_VALUE = 3

    # Game config
    self.pool_size = pool_size
    self.players = players
    self.running_tally = running_tally

    # New game init
    self.hill = [0, 0, 0, 0]
    self.pool = [0, 0, 0, 0]
    self.whists = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    self.closed = False


  def __str__(self):
    """
    Produces an ASCII representation of the poolya score sheet.
    """
    tally = self.tally() if self.running_tally or self.closed else ""

    if self.players == 3:
      return """\
Pool: {}, Size: {}
+---------------------------+
|   |   |     |     |   |   |
|   |   |     |     |   |   |
|{:^3}|   |     |     |   |{:^3}|
|   |   | {:^3} | {:^3} |   |   |
|   |   |    W|E    |   |   |
|---|{:^3}|    /S\    |{:^3}|---|
|   |   |  /     \  |   |   |
|   |   |/   {:^3}   \|   |   |
|{:^3}|  /+-----------+\  |{:^3}|
|   |/       {:^3}       \|   |
|  /+-------------------+\  |
|/     {:^3}    |   {:^3}      \|
+---------------------------+
""".format(self.VARIANT, self.pool_size, 
      self.whists[W][E], self.whists[E][W],
      self.hill[W], self.hill[E],
      self.pool[W], self.pool[E],
      self.hill[S],
      self.whists[W][S], self.whists[E][S],
      self.pool[S],
      self.whists[S][W], self.whists[S][E]) + tally

    else:
      return """\
Pool: {}, Size: {}
+---------------------------+
|\    {:^3}  | {:^3} |  {:^3}    /|
|  \+-------------------+/  |
|   |\       {:^3}       /|   |
|{:^3}|  \+-----------+/  |{:^3}|
|   |   |\   {:^3}   /|   |   |
|---|   |  \     /  |   |---|
|   |   |    \\N/    |   |   |
|{:^3}|{:^3}|{:^3} WXE {:^3}|{:^3}|{:^3}|
|   |   |    /S\    |   |   |
|---|   |  /     \  |   |---|
|   |   |/   {:^3}   \|   |   |
|{:^3}|  /+-----------+\  |{:^3}|
|   |/       {:^3}       \|   |
|  /+-------------------+\  |
|/    {:^3}  | {:^3} |  {:^3}    \|
+---------------------------+
""".format(self.VARIANT, self.pool_size, 
      self.whists[N][W], self.whists[N][S], self.whists[N][E],
      self.pool[N],
      self.whists[W][N], self.whists[E][N],
      self.hill[N],
      self.whists[W][E], self.pool[W], self.hill[W], self.hill[E], self.hill[E],
        self.whists[E][W],
      self.hill[S],
      self.whists[W][S], self.whists[E][S],
      self.pool[S],
      self.whists[S][W], self.whists[S][N], self.whists[S][E]) + tally


  def set_scores(self, pool, hill, whists):
    """
    Sets the game to any score given by the pool, hill and whists passed in.
    """
    for i in range(self.players):
      self.pool[i] = pool[i][-1]
      self.hill[i] = hill[i][-1]
      for j in range(self.players):
        self.whists[i][j] = whists[i][j][-1]


  def inc_whists(self, player, target, amt):
    """
    Write whists of player against target.
    """
    self.whists[player][target] += amt


  def inc_pool(self, player, amt):
    """
    Write points into player's pool.
    """
    self.pool[player] += amt


  def inc_hill(self, player, amt):
    """
    Write points into player's hill."
    """
    self.hill[player] += amt


  def score_passes(self, tricks):
    """
    Base scoring of passes round."
    """
    raise NotImplementedError("Scoring passes round not implemented.")


  def score_consolation(self, player, tricks):
    """
    All players receive consolation whists against player in the case of
    player's remise.
    """
    for w in range(self.players):
      if w != player:
        self.inc_whists(w, player, self.CONSOLATION_VALUE * tricks)


  def score_misere(self, player, tricks):
    """
    Base scoring of a misere contract round.
    """
    # Successful misere, player receives value of contract into the pool
    if tricks == 0:
      self.inc_pool(player, self.CONTRACT_VALUE[MISERE])
    # Failed misere, player receives value of contract for every trick taken
    #   into the hill.
    else:
      self.inc_hill(player, self.CONTRACT_VALUE[MISERE] * tricks)
      # All other opponents (including dealer) write a consolation in whists
      #   against player.
      self.score_consolation(player, tricks)

    
  def score_contract(self, player, contract,
      whister1=None, tricks=None, whister2=None):
    """
    Base scoring of 6-10 contract rounds.
    """
    # Uncontested contract; player receives value of contract into the pool.
    if whister1 == None:
      self.inc_pool(player, self.CONTRACT_VALUE[contract])
    # whister1 is actually a half-whister; player receives full value of
    #   contract into the pool, whister1 receives whists against player as if
    #   he had taken half of the required number of whisting tricks.
    elif tricks == None:
      self.inc_whists(whister1, player,
          self.CONTRACT_VALUE[contract] * self.WHIST_COEFF *
          self.WHIST_OBLIGATION // 2)
    # Contract is whisted
    else:
      # Player makes the contract and receives value of contract into the pool
      if tricks[player] >= contract:
        self.inc_pool(player, self.CONTRACT_VALUE[contract])
      # Player fails to make the contract and receives value of the contract
      #   _per undertrick_ into the hill. Additionally, all others including
      #   the dealer write a consolation in whists against player.
      else:
        self.inc_hill(player, self.CONTRACT_VALUE[contract] *
            (contract - tricks[player]))
        self.score_consolation(player, contract - tricks[player])

      # Single whister
      if whister2 == None:
        # Greedy whist:
        # Whister receives whists against player for all whisted tricks taken.
        whisted_tricks = sum(tricks[i] for i in range(3) if i != player)
        self.inc_whists(whister1, player,
            self.CONTRACT_VALUE[contract] * self.WHIST_COEFF * whisted_tricks)
        # If whister fails to fulfill whisting obligation, he receives points
        #   into the hill
        undertricks = max(self.WHIST_OBLIGATION[contract] - whisted_tricks, 0)
        if undertricks != 0:
          self.inc_hill(whister1, int(self.CONTRACT_VALUE[contract] *
              self.WHIST_REMISE_COEFF) * undertricks)

      # Two whisters
      else:
        # Each whister receives whists against player for the whisted tricks
        #   they took individually.
        whisted_tricks = tricks[whister1] + tricks[whister2]
        self.inc_whists(whister1, player,
            self.CONTRACT_VALUE[contract] * self.WHIST_COEFF * tricks[whister1])
        self.inc_whists(whister2, player,
            self.CONTRACT_VALUE[contract] * self.WHIST_COEFF * tricks[whister2])
        # If whisters fail to collectively fulfill their whisting obligation,
        #   they are each liable for their half of whisted tricks for contracts
        #   of 6 and 7. For contracts 8-10, the _second_ whister (ie. the one
        #   to the right of the player) is liable. For whist undertricks, the
        #   responsible whister(s) receive(s) points into the hill.
        undertricks = max(self.WHIST_OBLIGATION[contract] - whisted_tricks, 0)
        if undertricks != 0:
          if contract < 8:
            obligation = self.WHIST_OBLIGATION[contract] // 2
            self.inc_hill(whister1, int(self.CONTRACT_VALUE[contract] *
              self.WHIST_REMISE_COEFF) * max(obligation - tricks[whister1], 0))
            self.inc_hill(whister2, int(self.CONTRACT_VALUE[contract] *
              self.WHIST_REMISE_COEFF) * max(obligation - tricks[whister2], 0))
          else:
            obligation = self.WHIST_OBLIGATION[contract]
            liable = (player + 1) % 3 # whister to the right of player
            self.inc_hill(liable, int(self.CONTRACT_VALUE[contract] *
              self.WHIST_REMISE_COEFF) *
              max(obligation - (tricks[whister1] + tricks[whister2]), 0))

  def give_aid(self, aider, aidee, aid):
    """
    Give aidee aid points into the pool, in exchange for which the aider writes
    whists against aidee.
    """
    needs = self.pool_size - self.pool[aidee]
    gets = min(needs, aid)
    self.pool[aidee] += gets
    # Compensation for every point of aid in whists
    self.inc_whists(aider, aidee, self.AID_WHIST_VALUE * gets)
    # Return any aid that is left
    return aid - gets


  def tally(self):
    """
    Calculate intermediate and final scores.
    """
    hill = [0, 0, 0]
    whist_adjust = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    # Write incomplete pool into the hill for intermediate tallies.
    for i in range(self.players):
      hill[i] = self.hill[i] + (self.pool_size - self.pool[i])
    for i in range(self.players):
      # Increment/decrement hill value to prevent non-integral whist values.
      #   If hill is incremented, player writes compensation whists against the
      #   other two. If decremented, they write whists against him.
      if hill[i] % self.players == 0:
        pass
      elif hill[i] % self.players > self.players / 2:
        hill[i] += 1
        for j in range(self.players):
          if j != i:
            whist_adjust[i][j] += self.HILL_WHIST_VALUE
      elif hill[i] % self.players < self.players / 2:
        hill[i] -= 1
        for j in range(self.players):
          if j != i:
            whist_adjust[j][i] += self.HILL_WHIST_VALUE
  
    for i in range(self.players):
      for j in range(self.players):
        if j != i:
          self.whists[j][j] += (hill[i] - hill[j]) * 10 // self.players
          self.whists[i][i] += (self.whists[i][j] + whist_adjust[i][j]) - \
              (self.whists[j][i] + whist_adjust[j][i])

    tally = "W: {:d}  S: {:d}  E: {:d}".format(self.whists[W][W],
        self.whists[S][S], self.whists[E][E])
    if self.players == 4:
      tally = "N: {:d}  ".format(self.whists[N][N]) + tally
    return tally


class Rostov(Pool):
  """
  Rostov/Moscow preferans variant. Characterized by:
    - Semi-responsible whist: remise of whister is punished by half the cost
      of the contract into the hill for every undertrick.
    - Consolation due to player's remise is received by all other players,
      including the dealer.
    - Gentlemanly whist: in the event of player's remise, points for taken whist
      tricks are split evenly among defenders, even if one of the whisters
      passed.
    - Passes round is scored in whists, usually 5 whists per trick taken. The
      winner of the passes round is the player(s) who took the fewest tricks.
      This player writes whists against all others based on the number of tricks
      they took.
    - No progression for passes round.
    - For zero tricks during a passes round, a player writes 1 point into the
      pool.
    - The blind is never opened during the passes round.
    - If there are four players, the dealer writes 1 point into the pool, as for
      zero tricks.
    - The game is played until all players reach the agreed-upon pool value. If
      a player has more in his pool than this value, the excess is given to
      another player as aid, in exchange for whists in a ten-fold quantity.
  """
  def __init__(self, pool_size=10, players=3):
    super().__init__(pool_size, players)
    self.VARIANT = "Rostov"
    self.PASSES_WHIST_VALUE = 5
    self.CONSOLATION_VALUE = 10
    self.WHIST_COEFF = 1
    self.WHIST_REMISE_COEFF = 0.5
    self.AID_WHIST_VALUE = 10


  def inc_pool(self, player, amt):
    """
    Increment a player's pool, without permitting the value to exceed the
    pool_size. Excess points are given to another player as aid in exchange for
    whists, or written off from the hill of the player.
    """
    self.pool[player] += amt
    # Check for too much in the pool, determine aid
    aid = max(self.pool[player] - self.pool_size, 0)
    left = (player - 1 + self.players) % self.players
    right = (player + 1) % self.players
    while aid != 0:
      self.pool[player] = self.pool_size
      # Determine aidee: the player with the next highest pool, or the player
      #   on the left if they have equal pools.
      #   If neither parther needs aid, it is written off from the hill.
      #   If there are fewer points in the hill of the player than the
      #   remaining aid, then these points are written into the hills of the
      #   other players.
      if (self.pool[left] == self.pool_size and
          self.pool[right] == self.pool_size):
        if self.hill[player] == 0:
          self.inc_hill(left, aid)
          self.inc_hill(right, aid)
        else:
          gets = min(self.hill[player], aid)
          self.inc_hill(player, gets * -1)
          aid -= gets
      elif self.pool[left] == self.pool_size:
        aid = self.give_aid(player, right, aid)
      elif self.pool[right] == self.pool_size:
        aid = self.give_aid(player, left, aid)
      else:
        aidee = right if self.pool[right] > self.pool[left] else left
        aid = self.give_aid(player, aidee, aid)

    # Check if pool of each player has reached the pool_size; game over
    for i in range(self.players):
      if self.pool[i] != self.pool_size:
        return
    self.closed = True


  def score_passes(self, tricks):
    """
    The winner of the passes round is the player(s) who took the fewest tricks.
    This/these player(s) write whists against the others for the number of
    tricks that the others took. If a player took no tricks, he writes 1 point
    into the pool.
    """
    m = min(tricks) # fewest tricks taken
    # Segregate winners and losers.
    winners = []
    losers = []
    for i in range(3):
      if tricks[i] > m:
        losers.append(i)
      else:
        winners.append(i)
    # Two winners possible: split whists against the loser
    if len(winners) == 2:
      l = losers[0]
      for w in winners:
        self.inc_whists(w, l, tricks[l] // 2 * self.PASSES_WHIST_VALUE)
    else: # one winner: writes whists against both losers
      w = winners[0]
      for l in losers:
        self.inc_whists(w, l, tricks[l] * self.PASSES_WHIST_VALUE)
    # If winners took 0 tricks, increment pool by 1
    if m == 0:
      for w in winners:
        self.inc_pool(w, 1)


  def score_contract(self, player, contract,
      whister1=None, tricks=None, whister2=None):
    """
    For successfully completing the contract, the player writes the worth of
    the contract into his pool; for a remise, he writes the worth of the
    contract into the hill for every undertrick. The whisters receive whists for
    tricks taken and consolation for the player's remise.
      - Semi-responsible whist (punishement for remise of whisters is half)
      - Gentlemanly whist (whisters always split whists for player's remise)
    """
    # Uncontested contract; player receives value of contract into the pool.
    if whister1 == None:
      self.inc_pool(player, self.CONTRACT_VALUE[contract])
    # whister1 is actually a half-whister; player receives full value of
    #   contract into the pool, whister1 receives whists against player as if
    #   he had taken half of the required number of whisting tricks.
    elif tricks == None:
      self.inc_whists(whister1, player,
          self.CONTRACT_VALUE[contract] * self.WHIST_COEFF *
          self.WHIST_OBLIGATION // 2)
    # Contract is whisted
    else:
      # Player makes the contract and receives value of contract into the pool
      if tricks[player] >= contract:
        self.inc_pool(player, self.CONTRACT_VALUE[contract])
      # Player fails to make the contract and receives value of the contract
      #   _per undertrick_ into the hill. Additionally, all others including
      #   the dealer write a consolation in whists against player.
      else:
        self.inc_hill(player, self.CONTRACT_VALUE[contract] *
            (contract - tricks[player]))
        self.score_consolation(player, contract - tricks[player])

      # Single whister
      if whister2 == None:
        whisted_tricks = 0
        for i in range(3):
          if i != player:
            whisted_tricks += tricks[i]
            if i != whister1:
              whister2 = i

        # Gentlemanly whist: if player is in remise, whists are split among both
        #   whisters, no matter that one passed.
        if tricks[player] < contract:
          whists = (self.CONTRACT_VALUE[contract] * self.WHIST_COEFF *
              whisted_tricks // 2)
          self.inc_whists(whister1, player, whists)
          self.inc_whists(whister2, player, whists)
        # Otherwise, whister receives whists against player for all whisted
        #   tricks taken.
        else:
          self.inc_whists(whister1, player,
              self.CONTRACT_VALUE[contract] * self.WHIST_COEFF * whisted_tricks)
        # If whister fails to fulfill whisting obligation, he receives points
        #   into the hill
        undertricks = max(self.WHIST_OBLIGATION[contract] - whisted_tricks, 0)
        if undertricks != 0:
          self.inc_hill(whister1, int(self.CONTRACT_VALUE[contract] *
              self.WHIST_REMISE_COEFF) * undertricks)

      # Two whisters
      else:
        # Each whister receives whists against player for the whisted tricks
        #   they took individually.
        whisted_tricks = tricks[whister1] + tricks[whister2]
        self.inc_whists(whister1, player,
            self.CONTRACT_VALUE[contract] * self.WHIST_COEFF * tricks[whister1])
        self.inc_whists(whister2, player,
            self.CONTRACT_VALUE[contract] * self.WHIST_COEFF * tricks[whister2])
        # If whisters fail to collectively fulfill their whisting obligation,
        #   they are each liable for their half of whisted tricks for contracts
        #   of 6 and 7. For contracts 8-10, the _second_ whister (ie. the one
        #   to the right of the player) is liable. For whist undertricks, the
        #   responsible whister(s) receive(s) points into the hill.
        undertricks = max(self.WHIST_OBLIGATION[contract] - whisted_tricks, 0)
        if undertricks != 0:
          if contract < 8:
            obligation = self.WHIST_OBLIGATION[contract] // 2
            self.inc_hill(whister1, int(self.CONTRACT_VALUE[contract] *
              self.WHIST_REMISE_COEFF) * max(obligation - tricks[whister1], 0))
            self.inc_hill(whister2, int(self.CONTRACT_VALUE[contract] *
              self.WHIST_REMISE_COEFF) * max(obligation - tricks[whister2], 0))
          else:
            obligation = self.WHIST_OBLIGATION[contract]
            liable = (player + 1) % 3 # whister to the right of player
            self.inc_hill(liable, int(self.CONTRACT_VALUE[contract] *
              self.WHIST_REMISE_COEFF) *
              max(obligation - (tricks[whister1] + tricks[whister2]), 0))


###############################################################################
EN = 'en'
RU = 'ru'
LANG = EN
PROMPT = {}
PROMPT[EN] = """\
+-----------++---+---+---+  1:    Pass        | -N: Revert back N deals
|    BID    || # TRICKS  |  2:    Half-whist  | Ctrl-D/Ctrl-C: Quit
+---+---+---||---+---+---+  3:    Whist       |
| W | S | E || W | S | E |  6-10: Contract    |
+---+---+---++---+---+---+  0:    Misere      |
> """

PROMPT[RU] = """\
+-----------++---+---+---+  1:    Пас
|    ТОРГ   || # ВЗЯТКИ  |  2:    Пол-виста
+---+---+---||---+---+---+  3:    Вист
| З | Ю | В || З | Ю | В |  6-10: Контракт
+---+---+---++---+---+---+  0:    Мизер
> """

VARIANTS = ["Rostov"]

DEFAULT_POOL = 10
DEFAULT_VARIANT = "Rostov"

if __name__ == "__main__":
  from sys import argv, exit

  try:
    pool = int(argv[1])
  except IndexError:
    print("No pool size given, defaulting to {}.".format(DEFAULT_POOL))
    pool = DEFAULT_POOL
  except ValueError:
    print("Error: Invalid pool size given.")
    print(__doc__)
    exit(1)

  try:
    variant = argv[2]
  except IndexError:
    print("No variant given, defaulting to {}.".format(DEFAULT_VARIANT))
    variant = DEFAULT_VARIANT
  if variant not in VARIANTS:
    print("Error: Invalid variant selected.")
    print(__doc__)
    exit(1)

  if variant == "Rostov":
    p = Rostov(pool)
  #elif variant == "Peter":
    #pass
  #elif variant == "Sochi":
    #pass
  else:
    p = Pool()

  # History
  pool_hist = [ [0], [0], [0] ]
  hill_hist = [ [0], [0], [0] ]
  whists_hist = [ [ [0], [0], [0] ], [ [0], [0], [0] ], [ [0], [0], [0] ] ]
  deals = 0

  # Main game loop
  while not p.closed:
    # Output poolya
    print(p)

    # Input loop
    input_valid = False
    while not input_valid:
      try:
        data = [ int(i) for i in input(PROMPT[LANG]).split() ]
      except ValueError:
        print("Error: non-integer arguments.")
        continue
      except (EOFError, KeyboardInterrupt):
        p.closed = True
        input_valid = True
        continue

      # Check for input validity
      if len(data) == 1 and data[0] < 0:
        # Attempt to revert some deals
        revert = data[0]
        if revert + deals < 0:
          print("Error: attempt to revert more deals than have been dealt.")
          continue
        else:
          for i in range(p.players):
            pool_hist[i] = pool_hist[i][:revert]
            hill_hist[i] = hill_hist[i][:revert]
            for j in range(p.players):
              whists_hist[i][j] = whists_hist[i][j][:revert]
          deals += revert
          p.set_scores(pool_hist, hill_hist, whists_hist)
          input_valid = True
          continue
      elif len(data) != 6:
        print("Error: invalid number of arguments.")
        continue

      bid = data[:3]
      tricks = data[3:]

      # Count up _types_ of bids
      # 0: miseres, 1: passes, 2: half-whists, 3: whists, 4: contracts
      bids = [0] * 5
      for b in bid:
        if 6 <= b <= 10:
          bids[CONTRACT] += 1
        elif 0 <= b <= 3:
          bids[b] += 1

      # Illegal bid combos
      if sum(bids) != 3:
        print("Error: invalid number of bids.")
        continue
      elif bids[MISERE] + bids[CONTRACT] > 1:
        print("Error: only one contract permitted.")
        continue
      elif bids[HWHIST] > 1:
        print("Error: only one player may half-whist.")
        continue
      elif bids[WHIST] > 2:
        print("Error: only two players may whist.")
        continue
      elif bids[WHIST] != 0 and bids[HWHIST] != 0:
        print("Error: whist and half-whist are mutually exclusive.")
        continue

      # Passes round
      elif bids[PASS] == 3:
        if sum(tricks) == 10:
          p.score_passes(tricks)
          input_valid = True
        else:
          print("Error: invalid number of tricks.")
          continue

      # Misere round
      elif bids[MISERE] == 1:
        player = bid.index(MISERE)
        p.score_misere(player, tricks[player])
        input_valid = True

      # Contract round
      elif bids[CONTRACT] == 1:
        whisters = []
        for i in range(3):
          if 6 <= bid[i] <= 10:
            player = i
            contract = bid[i]
          elif bid[i] == WHIST:
            whisters.append(i)
          elif bid[i] == HWHIST:
            hwhister = i

        # Both opponents pass, unwhisted contract
        if bids[PASS] == 2:
          p.score_contract(player, contract)
          input_valid = True
        # One opponent declares half-whist
        elif bids[HWHIST] == 1:
          if contract < 8:
            p.score_contract(player, contract, hwhister)
            input_valid = True
          else:
            print("Error: only contracts of 6 and 7 may be half-whisted.")
            continue
        # One opponent whists
        elif bids[WHIST] == 1:
          if sum(tricks) == 10:
            p.score_contract(player, contract, whisters[0], tricks)
            input_valid = True
          else:
            print("Error: invalid number of tricks.")
            continue
        # Both opponents whist
        elif bids[WHIST] == 2:
          if sum(tricks) == 10:
            p.score_contract(player, contract, whisters[0], tricks, whisters[1])
            input_valid = True
          else:
            print("Error: invalid number of tricks.")
            continue

      if input_valid:
        deals += 1
        for i in range(p.players):
          pool_hist[i].append(p.pool[i])
          hill_hist[i].append(p.hill[i])
          for j in range(p.players):
            whists_hist[i][j].append(p.whists[i][j])

  # Print final score sheet before exit.
  print(p)
