from RoguePy.Game import Map
from entities import *

__author__ = 'jripley'

from RoguePy.UI import Colors

nodeHunter = {
  'targetPrio': [Node, Shroom, Player],
  'hp': 10,
  'damage': 5,
  'range': 1
}

shroomHunter = {
  'targetPrio': [Shroom, Node, Player],
  'hp': 12,
  'damage': 5,
  'range': 1
}

playerHunter = {
  'targetPrio': [Player, Shroom],
  'hp': 15,
  'damage': 15,
  'range': 1
}

shroomHunter = ["Shroom hunter", '&', Colors.dark_flame, Map.pathFunc, shroomHunter]
nodeHunter = ["Node hunter", 'x', Colors.dark_blue, Map.pathFunc, nodeHunter]
playerHunter = ["Shroom hunter", 'w', Colors.dark_orange, Map.pathFunc, playerHunter]
