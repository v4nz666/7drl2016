from RoguePy.Game import Map
from entities import *

__author__ = 'jripley'

from RoguePy.UI import Colors


genero = {
  'targetPrio': [Node, Shroom, Player],
  'hp': 10,
  'damage': 5,
  'range': 1
}

enemy = ["Enemy", '%', Colors.green, 'shroom', Map.pathFunc, genero]
