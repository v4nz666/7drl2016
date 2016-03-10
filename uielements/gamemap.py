from RoguePy.UI.Elements.Map import CellView
import config

__author__ = 'jripley'
from math import sqrt
from RoguePy.UI import Elements
from RoguePy.UI import Colors
from RoguePy.libtcod import libtcod

class GameMap(Elements.Map):

  buildChars = ['\\', '|', '/', '-']
  buildCharIndex = 0

  def __init__(self, x, y, w, h, map):
    super(GameMap, self).__init__(x, y, w, h, map)
    self.player = None
    self.buildSites = []


  def setPlayer(self, player):
    self.player = player
    self._initFovMap()
    self.calculateFovMap()

  def addBuildSite(self, x, y):
    if not (x, y) in self.buildSites:
      self.buildSites.append((x, y))
  def removeBuildSite(self, x, y):
    if (x,y) in self.buildSites:
      self.buildSites.remove((x,y))

  def updateBuildChar(self):
    self.buildCharIndex += 1
    if self.buildCharIndex >= len(self.buildChars):
      self.buildCharIndex = 0

    onScreen = False
    for (x, y) in self.buildSites:
      if not self.onScreen(x, y):
        continue
      onScreen = True

    if onScreen:
      self.setDirty()

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
          cv = self.cellToView(c, mapX, mapY)
          libtcod.console_put_char_ex(self.console, onScreenX, onScreenY, cv.char, cv.fg, cv.bg)
          if self.map.shroom.active and self.map.shroom.inNetwork(mapX, mapY):
            # print "%d, %d : %d, %d" % (onScreenX, onScreenY, mapX, mapY)
            libtcod.console_set_char_background(
              self.console, onScreenX, onScreenY, Colors.chartreuse, flag=libtcod.BKGND_ADDALPHA(0.1))

    self.setDirty(False)

  def cellToView(self, c, x, y):
    result = super(GameMap, self).cellToView(c)
    if (x, y) in self.buildSites:
      result = CellView(self.buildChars[self.buildCharIndex], result.fg, result.bg)
    return result

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


