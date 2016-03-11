from RoguePy.libtcod import libtcod
from RoguePy.Game import Entity

__author__ = 'jripley'

class Enemy(Entity):

  def __init__(self, name, ch, clr, target, pathFunc):
    super(Enemy, self).__init__(name, ch, clr)
    self.target = target
    self.targetCoord = None
    self.path = None
    self.pathFunc = pathFunc

    self.range = 1


  def spawn(self, map, x, y):
    print "Enemy spawned at", x, y
    if super(Enemy, self).spawn(map, x, y):
      self.updateTarget()

  def updateTarget(self):
    print "Updating target"
    if self.target == 'shroom':
      self.targetCoord = (self.map.shroom.x, self.map.shroom.y)

    if self.path:
      libtcod.path_delete(self.path)

    pathFunc = lambda x1, y1, x2, y2, userData: self.pathFunc(self.map, self, x1, y1, x2, y2)
    print "creating path"
    self.path = libtcod.path_new_using_function(self.map.width, self.map.height, pathFunc)
    print "done"
    self.computePath()

  def computePath(self):
    print "computing path from ", self.x, self.y, " TO ", self.targetCoord[0], self.targetCoord[1]
    libtcod.path_compute(self.path, self.x, self.y, self.targetCoord[0], self.targetCoord[1])
    print "done"


  def takeTurn(self):
    print "taking turn"
    ### Attack if we can
    # In range, we can attack whether we have a path or not.
    if self.map.distance(self.x, self.y, self.targetCoord[0], self.targetCoord[1]) <= self.range:
      #try attack()
      # # Our attack timer has elapsed
      # if self.waitLeft == 0:
      #   # Reset the wait timer
      #   self.attacking = True
      #   self.waitLeft = self.waitTimeout
      #   return True
      # # Not yet time to attack, returning False will trigger an idleUpdate()
      # else:
      #   return False
      print "In range!"
      return True

    ### Try to move
    pathSize = libtcod.path_size(self.path)
    if pathSize > self.range:
      (newX, newY) = libtcod.path_walk(self.path, False)

      if not (newX and newY):
        print "failed to move, recalculating"
        self.computePath()
        return False
      dx = newX - self.x
      dy = newY - self.y
      if self.tryMove(dx,dy):
        print "moved to ", self.x, self.y
        return True
      else :
        print "failed to move, recalculating"
        self.computePath()
    return False


    #Attack cooldown
    # if self.waitLeft > 0:
    #   self.waitLeft -= 1
