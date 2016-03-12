from attack import Attack
from entities.enemy import Enemy

__author__ = 'jripley'

from RoguePy.Game import Entity


class Node(Entity):
  def findTarget(self):
    cells = self.map.getCellsInRad(self.x, self.y, self.range)
    for c in cells:
      if not c.entity:
        continue
      if isinstance(c.entity, Enemy):
        if c.entity.isDead:
          continue
        a = Attack(self.map, self, c.entity, self.damage, self.radius)
        self.map.addAttack(a)


    
    
  