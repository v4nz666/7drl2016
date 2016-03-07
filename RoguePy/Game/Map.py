from .. import UI
from RoguePy.libtcod import libtcod
from RoguePy.UI import Colors

import config


class Map:
  def __init__(self, w, h, cells=None):
    self.width = w
    self.height = h
    if cells == None:
      self.cells = [Cell('floor') for dummy in range(w*h)]
    else:
      self.cells = cells
    self.listeners = {}


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
    # TODO: Bounds checking.
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


class Cell:
  def __init__(self, type):
    self.setType(type)
    self.entity = None
    self.items = []
    self.seen = False
    pass

  def setType(self, type):
    self.type = type
    self.terrain = CellType.All[type]

  def discover(self):
    self.seen = True

class CellType:
  def __init__(self, char, fg, bg):
    self.char = char
    self.fg = fg
    self.bg = bg
    self.passable = False
    self.transparent = False

  def setPassable(self, passable):
    self.passable = passable
    return self

  def setTransparent(self, transparent):
    self.transparent = transparent
    return self

CellType.All = {
  'water': CellType('~', Colors.dark_blue, Colors.darkest_blue).setPassable(False).setTransparent(True),
  'grass': CellType(',', Colors.dark_green, Colors.darker_green).setPassable(True).setTransparent(True),
  'tree': CellType('}', Colors.dark_green, Colors.darkest_green).setPassable(False).setTransparent(False),
  'mountain': CellType('^', Colors.grey, Colors.darkest_grey).setPassable(False).setTransparent(False)
}
