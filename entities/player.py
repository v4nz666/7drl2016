__author__ = 'jripley'

from RoguePy.Game import Entity

class Player(Entity):
  def canEnter(self, dest):
    if dest.passable:

      while dest.moveCost:
        dest.moveCost -= 1
        self.map.trigger("moveWait", self, self)
      dest.resetMoveCost()
      return True
    else:
      return False
