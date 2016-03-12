from attack import Attack
from entities.enemy import Enemy

__author__ = 'jripley'

from RoguePy.Game import Entity


class Node(Entity):
  netRadius = 8
  def findTarget(self):
    cells = self.map.getCellsInRad(self.x, self.y, self.radius)
    for c in cells:
      if not c.entity:
        continue
      if isinstance(c.entity, Enemy):
        a = Attack(self.map, self, c.entity, self.damage, self.radius)
        self.map.addAttack(a)


    
    
  