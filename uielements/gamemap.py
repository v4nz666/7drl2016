import config

__author__ = 'jripley'
from math import sqrt
from RoguePy.UI import Elements
from RoguePy.UI import Colors
from RoguePy.libtcod import libtcod

class GameMap(Elements.Map):
  def __init__(self, x, y, w, h, map):
    super(GameMap, self).__init__(x, y, w, h, map)
    self.player = None

  def setPlayer(self, player):
    self.player = player
    self._initFovMap()
    self.calculateFovMap()

  def draw(self):
    for onScreenY in range(self.height):
      for onScreenX in range(self.width):
        mapX = onScreenX + self._offsetX
        mapY = onScreenY + self._offsetY
        c = self.map.getCell(mapX, mapY)

        # newly seen
        if not c.seen:
          if libtcod.map_is_in_fov(self.fovMap, mapX, mapY):
            c.discover()
        # GOTCHA: not else, since we want to catch newly seen cells
        if c.seen:
          cv = self.cellToView(c)
          libtcod.console_put_char_ex(self.console, onScreenX, onScreenY, cv.char, cv.fg, cv.bg)

    self.setDirty(False)

  def _initFovMap(self):
    w = config.world['mapWidth']
    h = config.world['mapHeight']
    self.fovMap = libtcod.map_new(w, h)
    for y in range(h):
      for x in range(w):
        c = self.map.getCell(x,y)
        libtcod.map_set_properties(self.fovMap, x, y, c.transparent, c.passable)

  def calculateFovMap(self):
    rad = config.player['viewRadius']
    libtcod.map_compute_fov(
      self.fovMap, self.player.x, self.player.y, rad, True, libtcod.FOV_SHADOW
    )
