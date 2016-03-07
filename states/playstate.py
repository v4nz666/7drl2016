import RoguePy
import uielements

__author__ = 'jripley'

import sys

import config
from RoguePy.Input import Keys
from RoguePy.UI import Elements
from RoguePy.UI import Colors
from RoguePy.State import GameState

class PlayState(GameState):

  def setupView(self):
    self.mapElement = uielements.GameMap(0, 0, config.ui['uiWidth'], config.ui['uiHeight'], self.map)

    self.view.addElement(self.mapElement)

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
