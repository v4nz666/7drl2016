__author__ = 'jripley'

from attack import Attack
from entities.enemy import Enemy


from RoguePy.Game import Entity

class Player(Entity):
  pass

  def spawn(self, map, x, y, hp):
    super(Player, self).spawn(map, x, y, hp)
    self.map.setPlayer(self)
    
    