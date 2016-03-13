__author__ = 'jripley'

from attack import Attack
from entities.enemy import Enemy


from RoguePy.Game import Entity

class Player(Entity):

  def spawn(self, map, x, y, hp, damage):
    super(Player, self).spawn(map, x, y, hp)
    self.damage = damage
    self.map.setPlayer(self)
    
    