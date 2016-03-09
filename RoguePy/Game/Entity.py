from RoguePy.libtcod import libtcod


class Entity:
    def __init__(self, map, x, y, name, ch, fg):
        c = map.getCell(x, y)
        if ( c.entity != None ):
          raise Exception("Entity already present in map cell (%d,%d)" % (x, y))
        c.entity = self
        self.map = map
        self.x = x
        self.y = y
        self.name = name
        self.ch = ch
        self.fg = fg
        self.inventory = []

    def pickup(self, item):

      self.inventory.append(item)
    def drop(self, item):
      if item in self.inventory:
        self.inventory.remove(item)

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
