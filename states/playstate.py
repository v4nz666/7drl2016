import RoguePy
import uielements

__author__ = 'jripley'

import sys

import config
from RoguePy.Input import Keys
from RoguePy.UI import Elements
from RoguePy.UI import Colors
from RoguePy.State import GameState
from RoguePy.libtcod import libtcod
class PlayState(GameState):

  def init(self):
    self.setupHandlers()

  def setupHandlers(self):
    self.addHandler('hudRefresh', 20, self.hudRefresh)

  def hudRefresh(self):
    self.fps.setLabel("FPS: " + str(libtcod.sys_get_fps()))




  def setupView(self):
    self.mapElement = uielements.GameMap(0, 0, config.ui['uiWidth'], config.ui['uiHeight'], self.map)
    self.view.addElement(self.mapElement)
    self.fps = self.view.addElement(Elements.Label(1, 1, "FPS: ".ljust(8)))\
      .setDefaultForeground(Colors.magenta)
    self.fps.bgOpacity = 0


  def setupInputs(self):
    # Inputs. =================================================================================
    self.view.setInputs({
      'quit' : {
        'key' : Keys.Escape,
        'ch'  : None,
        'fn'  : sys.exit
      }
    })
    self.mapElement.setDirectionalInputHandler(self.movePlayer)
    self.setFocus(self.mapElement)

  def movePlayer(self,dx,dy):
    if self.player.tryMove(dx, dy):
      self.mapElement.center(self.player.x, self.player.y)
      self.mapElement.calculateFovMap()
      self.mapElement.setDirty()

  def spawnPlayer(self):
    x = self.map.shroom.x
    y = self.map.shroom.y
    for dy in range(-1,1):
      for dx in range(-1,1):
        if not dx and not dy:
          continue
        _x = x+dx
        _y = y+dy
        try:
          if self.map.getCell(_x, _y).type == 'grass':
            print "Player: %d, %d" % (_x, _y)
            return RoguePy.Game.Entity(self.map, _x, _y, 'Sporaculous', '@', Colors.white)
        except IndexError:
          pass

  def setMap(self,map):
    self.map = map
    self.setupView()

    self.player = self.spawnPlayer()
    self.mapElement.setPlayer(self.player)
    self.mapElement.calculateFovMap()
    self.mapElement.center(self.player.x, self.player.y)

    self.setupInputs()
    self.setupEvents()


  def setupEvents(self):
    self.map.on('entity_interact', self.entityInteract)
    self.map.on('entity_collide', self.terrainCollide)
  def entityInteract(self, src, target):
    print "interact", target.name
  def terrainCollide(self, src, dest):
    print "collide", dest.type