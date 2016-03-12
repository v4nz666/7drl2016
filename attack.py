from explosion import Explosion

__author__ = 'jripley'

from RoguePy.libtcod import libtcod

class Attack():
  def __init__(self, map, src, target, dmg, rad):
    self.map = map

    self.source = src
    self.x = src.x
    self.y = src.y
    self.target = target
    self.targetX = target.x
    self.targetY = target.y
    self.ch = "."

    self.damage = dmg
    self.radius = rad
    self.explosion = None



  def __repr__(self):
    return "Self: (%d,%d) Target: (%d,%d)" % (self.x, self.y, self.targetX, self.targetY)

  def update(self):
    if self.x == self.targetX and self.y == self.targetY:
      if not self.explosion:
        print "exploding"
        self.explode()

    libtcod.line_init(self.x, self.y, self.targetX, self.targetY)
    x, y = libtcod.line_step()
    if (x and y):
      self.x = x
      self.y = y

  def explode(self):
    for c in self.map.getCellsInRad(self.x, self.y, self.radius):
      e = c.entity
      if e is not None:
        self.map.trigger('entity_explosion', self.source, e)



    self.explosion = Explosion(self)
    # self.map.trigger("attack_hit")
    