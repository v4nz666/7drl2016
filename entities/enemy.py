from RoguePy.libtcod import libtcod
from RoguePy.Game import Entity
import entities

__author__ = 'jripley'

class Enemy(Entity):

  def __init__(self, name, ch, clr, target, pathFunc, opts):
    super(Enemy, self).__init__(name, ch, clr, opts)
    self.targetCoord = None
    self.path = None
    self.pathFunc = pathFunc

  def spawn(self, map, x, y, hp):
    print "Enemy spawned at", x, y
    if super(Enemy, self).spawn(map, x, y, hp):
      self.updateTarget()

  def updateTarget(self):

    for t in self.targetPrio:
      if t == entities.Shroom:
        self.targetCoord = (self.map.shroom.x, self.map.shroom.y)
        break
      elif t == entities.Node:
        net = self.map.shroom.net

        index = 0
        closest = 0
        d = 99999

        for n in net.nodes:
          if self.map.distance(self.x, self.y, n.x, n.y) < d:
            closest = index
          index += 1
        closestNode = net.nodes[closest]
        self.targetCoord = (closestNode.x, closestNode.y)
        break
      elif t == entities.Player:
        self.targetCoord = self.map.getPlayerCoords()
        break

    if self.path:
      libtcod.path_delete(self.path)

    pathFunc = lambda x1, y1, x2, y2, userData: self.pathFunc(self.map, self, x1, y1, x2, y2)
    self.path = libtcod.path_new_using_function(self.map.width, self.map.height, pathFunc)
    self.computePath()

  def computePath(self):
    libtcod.path_compute(self.path, self.x, self.y, self.targetCoord[0], self.targetCoord[1])


  def takeTurn(self):
    ### Attack if we can
    # In range, we can attack whether we have a path or not.
    tx, ty = self.targetCoord[0], self.targetCoord[1]
    dist = self.map.distance(self.x, self.y, tx, ty)
    if int(dist) <= self.range:
      if self.readyToAttack():
        target = self.map.getCell(tx, ty).entity
        if target:
          self.attack(target, True)

        pass
      return True

    ### Try to move
    pathSize = libtcod.path_size(self.path)
    if pathSize > self.range:
      (newX, newY) = libtcod.path_walk(self.path, False)

      if not (newX and newY):
        # print "failed to move, recalculating"
        self.computePath()
        return False
      dx = newX - self.x
      dy = newY - self.y
      if self.tryMove(dx,dy):
        # print "moved to ", self.x, self.y
        return True
      else :
        # print "failed to move, recalculating"
        self.computePath()
    return False


    #Attack cooldown
    # if self.waitLeft > 0:
    #   self.waitLeft -= 1
