__author__ = 'jripley'

from RoguePy.libtcod import libtcod

### Random
seed = 666
rand = libtcod.random_new_from_seed(seed)
def randint(max):
  return libtcod.random_get_int(rand, 0, max)

ui = {
  'uiWidth': 96,
  'uiHeight': 60,
  'mapWidth': 96,
  'mapHeight': 60,

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