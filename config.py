from entities import Enemy
import items

__author__ = 'jripley'

from RoguePy.libtcod import libtcod

manaRate = 0.005

### Random
rand = libtcod.random_get_instance()
def randint(max, min=0):
  return libtcod.random_get_int(rand, min, max)

ui = {
  'uiWidth': 96,
  'uiHeight': 60,


  'invX': 96 - 24,
  'invY': 4,
  'invW': 24,
  'invH': 3,

  'netX': 96 - 24,
  'netY': 7,
  'netW': 24,
  'netH': 6,
  
  'healthX': 96 - 24,
  'healthY': 13,
  'healthW': 24,
  'healthH': 4,

  'msgW': 24,
  'msgH': 41,
  'msgX': 96 - 24,
  'msgY': 17,
}

world = {
  'mapWidth': ui['uiWidth'] * 2,
  'mapHeight' : ui['uiHeight'] * 2,
  'mapMin': 0,
  'mapMax': 1024
}

player = {
  'viewRadius': 16,
  'hp': 100,
  'damage': 10,
  'range': 16,
  'radius': 1,
  'cooldown': 3,
  'attackCost': 10
}

shroom = {
  'hp': 100,
  'targetPrio': [Enemy],
  'damage': 16,
  'range': 16,
  'radius': 2,
  'cooldown': 7,
  'attackCost': 50
}

node = {
  'hp': 25,
  'targetPrio': [Enemy],
  'damage': 10,
  'range': 8,
  'radius': 1,
  'cooldown': 5,
  'attackCost': 25,
  'item': items.spore
}


