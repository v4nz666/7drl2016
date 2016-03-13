from entities import Enemy
import items

__author__ = 'jripley'

from RoguePy.libtcod import libtcod

manaRate = 0.0025

### Random
rand = libtcod.random_get_instance()
def randint(max, min=0):
  return libtcod.random_get_int(rand, min, max)

ui = {
  'uiWidth': 96,
  'uiHeight': 60,

  'msgW': 24,
  'msgH': 16,
  'msgX': 96 - 24,
  'msgY': 60 - 16,

  'invX': 96 - 24,
  'invY': 4,
  'invW': 24,
  'invH': 10,

  'netX': 96 - 24,
  'netY': 14,
  'netW': 24,
  'netH': 16
}

world = {
  'mapWidth': ui['uiWidth'] * 2,
  'mapHeight' : ui['uiHeight'] * 2,
  'mapMin': 0,
  'mapMax': 1024
}

player = {
  'viewRadius': 16,
  'hp': 100
}

shroom = {
  'hp': 100,
  'targetPrio': [Enemy],
  'damage': 20,
  'range': 16,
  'radius': 3,
  'cooldown': 5,
  'attackCost': 50
}

node = {
  'hp': 25,
  'targetPrio': [Enemy],
  'damage': 12,
  'range': 8,
  'radius': 1,
  'cooldown': 3,
  'attackCost': 25,
  'item': items.spore
}

