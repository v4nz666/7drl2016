import chars
import config as cfg
from entities import Shroom

__author__ = 'jripley'

import random
from RoguePy.Game import Map, Entity
from RoguePy.Game.Map import Cell
from RoguePy.UI import Elements, View
from RoguePy.UI import Colors
import terrains


import config
import sys
from RoguePy.Input import Keys
from RoguePy.State import GameState
from RoguePy.libtcod import libtcod

class GenerateState(GameState):
  def init(self):
    self.setupView()

    self.addHandler('gen', 1, self.generateWorld)

    self.focusX = self.view.width/2
    self.focusY = self.view.height/2

    self.setupInputs()

  def setupView(self):
    loadingText= "Generating"
    loadingX = (self.view.width - len(loadingText)) / 2
    loadingY = self.view.height / 2 - 3
    self.view.addElement(Elements.Label(loadingX, loadingY, loadingText))\
      .setDefaultForeground(Colors.dark_azure)


  def setupInputs(self):
    
    # Inputs. =================================================================================
    self.view.setInputs({
      'next' : {
        'key' : Keys.Space,
        'ch'  : None,
        'fn'  : self.play
      },
      'quit' : {
        'key' : Keys.Escape,
        'ch'  : None,
        'fn'  : sys.exit
      },
      'move_s': {
          'key' : Keys.NumPad2,
          'ch'  : None,
          'fn'  : lambda: self.moveMap(0,1)
      },
      'move_w': {
          'key' : Keys.NumPad4,
          'ch'  : None,
          'fn'  : lambda: self.moveMap(-1,0)
      },
      'move_e': {
          'key' : Keys.NumPad6,
          'ch'  : None,
          'fn'  : lambda: self.moveMap(1,0)
      },
      'move_n': {
          'key' : Keys.NumPad8,
          'ch'  : None,
          'fn'  : lambda: self.moveMap(0,-1)
      }
    })
  def moveMap(self,dx,dy):
    if self.focusX + dx >= 0 and self.focusX + dx < self.map.width:
      self.focusX += dx
    if self.focusY + dy >= 0 and self.focusY + dy < self.map.height:
      self.focusY += dy
    self.mapElement.center(self.focusX, self.focusY)

  def generateWorld(self):
    while True:
      w = config.world['mapWidth']
      h = config.world['mapHeight']

      hm = libtcod.heightmap_new(w, h)
      rand = config.rand

      hills = 4096
      hillHeight = 15
      hillRad = 50
      libtcod.heightmap_clear(hm)

      for i in range(hills) :
        height= config.randint(hillHeight)
        rad = config.randint(hillRad)

        hillX1 = config.randint(config.world['mapWidth'])
        hillY1 = config.randint(config.world['mapHeight'])

        hillX2 = config.randint(config.world['mapWidth'])
        hillY2 = config.randint(config.world['mapHeight'])

        if config.randint(10) < 3:
          libtcod.heightmap_dig_hill(hm, hillX1, hillY1, height, rad)
          libtcod.heightmap_dig_hill(hm, hillX2, hillY2, height, rad)
        else:
          libtcod.heightmap_add_hill(hm, hillX1, hillY1, height, rad)
          libtcod.heightmap_add_hill(hm, hillX2, hillY2, height, rad)
      libtcod.heightmap_rain_erosion(hm,10000, 0.3, 0.2)
      libtcod.heightmap_normalize(hm, 0.0, 1024.0)

      thresholds = [
        {
          'type': 'water',
          'range': 0.1
        },{
          'type': 'grass',
          'range': 0.666
        },{
          'type': 'mountain',
          'range': 1.0
        }
      ]

      self.map = Map.FromHeightmap(hm, thresholds)
      self.generateTrees()

      self.spawnShroom()
      if self.validMap():
        self.mapElement = Elements.Map(0, 0, config.ui['uiWidth'], config.ui['uiHeight'], self.map)

        self.view.addElement(self.mapElement)
        self.mapElement.center(self.focusX, self.focusY)

        self.removeHandler('gen')
        return True

  def validMap(self):
    return True

  def generateTrees(self):
    caTreeDensity = 0.666
    caNeighboursSpawn = 7
    caNeighboursStarve = 4
    caIterations = 6

    w = config.world['mapWidth']
    h = config.world['mapHeight']
    
    treeCount = int(w * h * caTreeDensity)
    treeMap = [False for c in range(w + h * w)]

    while treeCount > 0:
      x = config.randint(w - 1)
      y = random.randrange(h - 1)
      try :
        tree = treeMap[x + y * w]
      except IndexError:
        continue

      if not tree:
        treeCount -= 1
        treeMap[x + y * w] = True

    for i in range(caIterations):

      neighbours = [None for _i in range(w + h * w)]
      for y in range(h) :
        for x in range(w) :
          neighbours[x + y * w] = self.countTreeNeighbours(x, y,treeMap)

      for y in range(h) :
        for x in range(w) :
          hasTree = treeMap[x + y * w]

          n = neighbours[x + y * w]
          if not hasTree:
            if n >= caNeighboursSpawn:
              treeMap[x + y * w] = True
          else:
            if n <= caNeighboursStarve:
              treeMap[x + y * w] = False
    self.setTrees(treeMap)

  def spawnShroom(self):
    maxX = config.world['mapWidth'] / 6
    minX = config.world['mapWidth'] / 2 - maxX / 2
    maxY = config.world['mapHeight'] / 6
    minY = config.world['mapHeight'] / 2 - maxY / 2

    x = minX + config.randint(maxX)
    y = minY + config.randint(maxY)

    if self.map.getCell(x, y).type == 'grass':
      shroom = Shroom('Shroom', chars.shroom, Colors.white, cfg.shroom)
      shroom.spawn(self.map, x, y, cfg.shroom['hp'])
      self.map.shroom = shroom
    else:
      self.spawnShroom()


  def setTrees(self, treeMap):
    for y in range(config.world['mapHeight']):
      for x in range(config.world['mapWidth']):
        c = self.map.getCell(x,y)
        if treeMap[x + y * config.world['mapWidth']] and c.type == 'grass':
          c.setType('tree')

  @staticmethod
  def countTreeNeighbours(x, y, treeMap) :
    t = 0
    for _x in range ( -1, 2 ):
      for _y in range ( -1, 2 ):
        if not _x and not _y:
          continue
        try:
          if treeMap[(x+_x) + (y+_y) * config.world['mapWidth']]:
            t += 1
        except IndexError:
          pass
    return t

  def play(self):
    self.manager.getState('play')\
      .setMap(self.map)
    self.manager.setNextState('play')
