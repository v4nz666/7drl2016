__author__ = 'jripley'

from RoguePy.libtcod import libtcod

### Random
seed = 666
rand = libtcod.random_new_from_seed(seed)
def randint(max, min=0):
  return libtcod.random_get_int(rand, min, max)

ui = {
  'uiWidth': 96,
  'uiHeight': 60,
  'msgW': 24,
  'msgH': 16,
  'msgX': 96 - 24,
  'msgY': 60 - 16
}

world = {
  'mapWidth': ui['uiWidth'] * 2,
  'mapHeight' : ui['uiHeight'] * 2,
  'mapMin': 0,
  'mapMax': 1024
}

player = {
  'viewRadius': 12
}