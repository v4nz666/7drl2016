from math import sqrt
import sys
from RoguePy.libtcod import libtcod
from RoguePy.UI import Colors
import chars

import config
from entities import Enemy


class Map:
  def __init__(self, w, h, cells=None):
    self.width = w
    self.height = h
    if cells == None:
      self.cells = [Cell('floor') for dummy in range(w*h)]
    else:
      self.cells = cells
    self.listeners = {}

    self.buildSites = {}

  def addBuildSite(self, x, y, b):
    if not (x, y) in self.buildSites:
      self.buildSites[(x, y)] = b
  def removeBuildSite(self, x, y):
    if (x,y) in self.buildSites:
      del self.buildSites[(x,y)]

  def purgeBuildSites(self):
    rm = []
    for x, y in self.buildSites:
      if self.buildSites[x,y].timer <= 0:
        rm.append((x,y))
    for x, y in rm:
      self.removeBuildSite(x, y)

  @staticmethod
  def FromFile(path):
    lines = open(path).read().splitlines()
    return Map.FromStringList(lines)

  @staticmethod
  def FromStringList(lines):
    # Get map dimensions, while ensuring all lines are the same length.
    w = None
    linenum = 0
    for x in lines:
      if w is None:
        w = len(x)
      elif len(x) != w:
        raise Exception("Line(%d) length = %d, expected = %d" % (linenum, len(x), w))
      linenum += 1
    h = len(lines)

    # Convert characters into map cells.
    cells = []
    for row in lines:
      for ch in row:
        cells.append(Map.CharToCell(ch))
    return Map(w, h, cells)

  @staticmethod
  def FromHeightmap(hm, thresholds):
    mapMin, mapMax = libtcod.heightmap_get_minmax(hm)
    mapMax = mapMax - mapMin
    mapMin = mapMin - mapMin
    w = config.world['mapWidth']
    h = config.world['mapHeight']

    cells = []

    for c in range(w*h):
      x = c%w
      y = c/w

      v = libtcod.heightmap_get_value(hm, x, y)
      for t in thresholds:
        if v <= t['range'] * mapMax:
          cells.append(Cell(t['type']))
          break
    return Map(w, h, cells)

  @staticmethod
  def CharToCell(ch):
    # TODO: This is not only game-specific, it's LOAD specific. No reason not to allow different
    #   lookups for different map data files / strings.
    cell = {
      '#': Cell('wall'),
      '.': Cell('floor'),
      'd': Cell('door'),
      'w': Cell('window'),
      }.get(ch)
    if cell == None:
      raise Exception("Unknown cell token [" + ch + "]")
    return cell

  def getCell(self, x, y):
    if not (0 <= x and x < self.width) or \
          not (0 <= y and y < self.height):
      return False

    return self.cells[x + y * self.width]

  def setCell(self, x, y, cell):
    self.cells[x + y * self.width] = cell

  def on(self, eventName, fn):
    eventListeners = self.listeners.get(eventName)
    if eventListeners is None:
      eventListeners = []
      self.listeners[eventName] = eventListeners
    eventListeners.append(fn)

  def trigger(self, eventName, sender, e):
    eventListeners = self.listeners.get(eventName)
    if not eventListeners: return
    for listener in eventListeners:
      listener(sender, e)

  # Hard coded 1 entity per tile
  def removeEntity(self, e, x, y):
    c = self.getCell(x, y)
    if c.entity == e:
      c.entity = None
      return True
    return False
  def addEntity(self, e, x, y):
    c = self.getCell(x, y)
    if c.entity is None:
      self.getCell(x, y).entity = e
      return True
    return False


  def addItem(self, i, x, y):
    c =  self.getCell(x, y)
    if not c.passable:
      return False

    if c.entity is not None:
      # TODO trigger item_interact
      return False

    if c.item is None:
      c.item = i
      return True
    return False
  def removeItem(self, i, x, y):
    c = self.getCell(x, y)
    if c.item == i:
      c.item = None
      return i
    return False


  def pathFunc(self, enemy, _x1, _y1, _x2, _y2):
    # print "(%d, %d),(%d,%d)" % (_x1,_y1,_x2,_y2)
    dest = self.getCell(_x2,_y2)
    if not dest.passable:
      # print "P: ", _x1, _y1, "**", _x2, _y2, dest.entity.x, dest.entity.y
      return 0.0
    elif isinstance(dest.entity, Enemy):
      # print "E Type:", type(dest.entity)
      # print "E: ", _x1, _y1, "**", _x2, _y2, dest.entity.x, dest.entity.y
      # sys.exit()
      return 0.0
    else:
      return 0.1 + 0.1 * dest.moveCost


  @staticmethod
  def distance(x1,y1,x2,y2):
    dx = x2 - x1
    dy = y2 - y1
    d = sqrt(dx**2 + dy**2)
    return d

class Cell:
  def __init__(self, type):
    self.setType(type)
    self.entity = None
    self.item = None
    self.seen = False
    pass

  def setType(self, type):
    self.type = type
    self.terrain = CellType.All[type]
    self.setOpts()

  def setOpts(self):
    for opt in self.terrain.opts:
      setattr(self, opt, self.terrain.opts[opt])

  def resetMoveCost(self):
    self.moveCost = self.terrain.opts['moveCost']

  def discover(self):
    self.seen = True

class CellType:
  def __init__(self, char, fg, bg, opts):
    self.char = char
    self.fg = fg
    self.bg = bg
    self.opts = opts

water = {
  'passable': False,
  'transparent': True,
  'destructible': False,
}
grass = {
  'passable': True,
  'transparent': True,
  'destructible': False,
  'moveCost': 0
}
tree = {
  'passable': True,
  'transparent': True,
  'destructible': True,
  'leaves': 'grass',
  'moveCost': 1
}
mountain = {
  'passable': True,
  'transparent': False,
  'destructible': True,
  'leaves': 'rockFloor',
  'moveCost': 2
}
rockFloor = {
  'passable': True,
  'transparent': True,
  'destructible': False,
  'moveCost': 0
}


CellType.All = {
  'water': CellType(chars.water, Colors.white, Colors.dark_blue, water),
  'grass': CellType(chars.grass, Colors.white, Colors.darker_green, grass),
  'tree': CellType(chars.tree, Colors.white, Colors.darker_green, tree),
  'mountain': CellType(chars.mountain, Colors.white, Colors.darker_green, mountain),
  'rockFloor': CellType('.', Colors.grey, Colors.darkest_grey, rockFloor)
}
