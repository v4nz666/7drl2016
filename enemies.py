from RoguePy.Game import Map

__author__ = 'jripley'

from RoguePy.UI import Colors


genero = {
  'target': 'shroom',
  'hp': 10,
  'damage': 5,
  'range': 1
}

enemy = ["Enemy", '%', Colors.green, 'shroom', Map.pathFunc, genero]
