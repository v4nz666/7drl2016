
class Entity(object):
  def __init__(self, name, ch, fg, opts = {}):
    self.name = name
    self.ch = ch
    self.fg = fg
    self.item = None
    for o in opts:
      setattr(self, o, opts[o])
    self.isDead = False


  def spawn(self, map, x, y, hp):
    print "spawning", self.name, x, y
    self.map = map
    self.x = x
    self.y = y
    self.hp = hp

    return map.addEntity(self, x, y)

  # Doin damage. Returns true if we died
  def takeDamage(self, dmg):
    print "%s took %d damage" % (self.name, dmg)
    self.hp -= dmg
    if self.hp <= 0:
      self.isDead = True
      return True
    return False

  def die(self):
    print self.name, "died"
    self.map.removeEntity(self, self.x, self.y)
    if self.item:
      self.map.addItem(self.item, self.x, self.y)



  def pickup(self, item):
    if not self.item:
      self.item = item
      return True
    return False

  def drop(self):
    self.item = None

  def tryMove(self, dx, dy):
    # Rest / skip check.
    if dx == 0 and dy == 0:
      return True

    # Adjacency check.
    if abs(dx) >  1 or abs(dy) > 1:
      return False

    dest = self.map.getCell(self.x + dx, self.y + dy)
    if not dest:
      return False

    # Entity check.
    if dest.entity is not None:
      self.map.trigger('entity_interact', self, dest.entity)
      return False

    # Terrain check.
    if not self.canEnter(dest):
      return False

    # TODO: This should be a map call because (a) it's ugly, and (b) it makes assumptions about
    #   how map stores entities.


    self.map.removeEntity(self, self.x, self.y)
    self.x += dx
    self.y += dy
    self.map.addEntity(self,self.x, self.y)

    self.map.trigger('entity_collide', self, dest)
    return True

  def canEnter(self, dest):
    if dest.passable:
      src = self.map.getCell(self.x, self.y)
      if src.moveCost <= 0:
        src.resetMoveCost()
        return True
      else:
        src.moveCost -= 1
        return False
