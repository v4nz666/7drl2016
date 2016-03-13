from attack import Attack

class Entity(object):
  def __init__(self, name, ch, fg, opts = {}):
    self.name = name
    self.ch = ch
    self.fg = fg
    self.item = None
    #likely overwritten in the loop below
    self.cooldown = 0
    for o in opts:
      setattr(self, o, opts[o])

    self.cooldownTimer = self.cooldown
    self.isDead = False

  def tick(self):
    self.cooldownTimer -= 1

  def spawn(self, map, x, y, hp):
    print "spawning", self.name, x, y
    self.map = map
    self.x = x
    self.y = y
    self.hp = hp

    return map.addEntity(self, x, y)

  def findTarget(self):
    cells = self.map.getCellsInRad(self.x, self.y, self.range)
    for c in cells:
      if not c.entity:
        continue
      for tType in self.targetPrio:
        if isinstance(c.entity, tType):
          if c.entity.isDead:
            continue
          return c.entity
    return False

  def attack(self, t, melee = False):
    self.cooldownTimer = self.cooldown
    if melee:
      if self.map.distance(self.x, self.y, t.x, t.y) == 1:
        print "Entity melee attacking"
        self.map.trigger('entityAttack', self, t)
    else:
      if type(t) == tuple:
        x, y = t
      else:
        x, y = t.x, t.y
      damage = self.techAdjust(self.damage, self.map.shroom.net.nodeCount)
      radius = self.techAdjust(self.radius, self.map.shroom.net.nodeCount)
      
      a = Attack(self.map, self, x, y, damage, radius)
      self.map.addAttack(a)


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

  # Check on our cooldown timer, decrement (or reset) as appropriate.
  def readyToAttack(self):
    return self.cooldownTimer <= 0

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
      self.map.trigger('entityInteract', self, dest.entity)
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

#### These do not belong here :(
  def getTechLevel(self, c):
    tech = [
      {
        'count': 0,
        'mul': 1
      },{
        'count': 3,
        'mul': 1.25
      },{
        'count': 7,
        'mul': 1.5
      },{
        'count': 10,
        'mul': 2.25
      }
    ]
    level = None
    for techLevel in tech:
      if c >= techLevel['count']:
        level = techLevel
    return level

  def techAdjust(self, val, nodeCount):
    tech = self.getTechLevel(nodeCount)
    val = int(val * tech['mul'])
    return val