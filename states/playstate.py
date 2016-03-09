import RoguePy
from RoguePy.Game.Item import Item
import chars
from entities import Shroom
import uielements

__author__ = 'jripley'

import sys

import config as cfg
from RoguePy.Input import Keys
from RoguePy.UI import Elements
from RoguePy.UI import Colors
from RoguePy.State import GameState, TickHandler
from RoguePy.libtcod import libtcod
class PlayState(GameState):

  def init(self):
    self.waves = []
    self.setupHandlers()

  def setupHandlers(self):

    self.addHandler('hudRefresh', 1, self.hudRefresh)
    self.turnHandlers = []

  def setupView(self):

    # Map
    self.mapElement = uielements.GameMap(0, 0, cfg.ui['uiWidth'] - cfg.ui['msgW'], cfg.ui['uiHeight'], self.map)
    self.view.addElement(self.mapElement)

    # HUD
    self.fps = Elements.Label(1, 1, "FPS: ".ljust(8))\
      .setDefaultForeground(Colors.magenta)
    self.fps.bgOpacity = 0
    self.view.addElement(self.fps)

    self.waveTimerLabel = Elements.Label(cfg.ui['msgX'], 1, "Next Wave: ".ljust(cfg.ui['msgW']))
    self.waveTimerLabel.bgOpacity = 0
    self.waveTimerLabel.setDefaultForeground(Colors.dark_fuchsia)
    self.waveTimerLabel.hide()
    self.view.addElement(self.waveTimerLabel)

    self.waveEnemyLabel = Elements.Label(cfg.ui['msgX'], 2, "Enemies: ".ljust(cfg.ui['msgW']))
    self.waveEnemyLabel.bgOpacity = 0
    self.waveEnemyLabel.setDefaultForeground(Colors.dark_fuchsia)
    self.waveEnemyLabel.hide()
    self.view.addElement(self.waveEnemyLabel)

    # Messages
    self.messageList = Elements.MessageScroller(cfg.ui['msgX'],cfg.ui['msgY'],cfg.ui['msgW'],cfg.ui['msgH'])
    self.messageList.bgOpacity = 0
    self.view.addElement(self.messageList)



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
      x, y = self.player.x, self.player.y
      self.mapElement.center(x, y)
      self.mapElement.calculateFovMap()
      self.mapElement.setDirty()
      c = self.map.getCell(x, y)
      if c.item is not None:
        i = self.map.removeItem(c.item, x, y)
        if i:
          self.messageList.message("%s got a %s" % (self.player.name,i.name))
          self.map.trigger('item_interact', self.player, i)
    self.doTurn()

  def itemInteract(self, e, i):
    e.pickup(i)

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
    print "Player not placed!"

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
    self.map.on('item_interact', self.itemInteract)
  def entityInteract(self, src, target):
    if src == self.player:
      self.messageList.message("Player hit %s" % target.name)
      if target.name == "Shroom" and not target.active:
        self.activateShroom(target)
        self.setupWaves()


  def doTurn(self):
    for h in self.turnHandlers:
      h()

  def activateShroom(self, shroom):
    self.messageList.message("As you approach the mushroom, your vision swirls.")
    shroom.activate(self.player)

  def terrainCollide(self, src, dest):
    self.messageList.message("stepped on %s" % (dest.type))

  def setupWaves(self):
    self.waves = []
    for wp in Wave.All():
      self.waves.append(Wave(*wp))
    self.initNextWave(first=True)
    self.turnHandlers.append(self.waveUpdate)

  def waveUpdate(self):
    wave = self.waves[0]
    if wave.timer > 0:
      wave.timer -= 1
      return
    else:
      self.activateWave()

    if len(wave.enemies):
      pass #updateEnemies
    else:
      self.messageList.message("wave complete")
      self.initNextWave()

    if len(self.waves) == 0:
      self.messageList.message("you win!!!!")
      self.turnHandlers.remove(self.waveUpdate)

  # The enemies have arrived
  def activateWave(self):
    self.waves[0].active = True

  # Start the timer, and deliver the items for the next wave
  def initNextWave(self, first=False):
    if not first:
      self.waves.pop(0)
    else:
      self.waveTimerLabel.show()
      self.waveEnemyLabel.show()


    items = self.waves[0].items
    for i in range(len(items)):
      spawned = False
      while not spawned:

        x = self.map.shroom.x + cfg.randint(12, -12)
        y = self.map.shroom.y + cfg.randint(12, -12)
        if not x and not y:
          continue

        if items[i].spawn(self.map, x, y):
          self.mapElement.setDirty()
          spawned = True

  def hudRefresh(self):
    self.fps.setLabel("FPS: %r" % (libtcod.sys_get_fps()))

    if len(self.waves):
      self.waveTimerLabel.setLabel("Next Wave: %s" % self.waves[0].timer)
      self.waveEnemyLabel.setLabel("Enemies: %s" % len(self.waves[0].enemies))


class Wave():
  def __init__(self, timer, items, enemies):
    self.active = False
    self.timer = timer
    self.items = items
    self.enemies = enemies

  def __repr__(self):
    return "Timer: %d\nenemies[%d]" % (self.timer, len(self.enemies))

  @staticmethod
  def All():
    return [
      [
        100, # timer
        [    # items
          Item("Spore",chars.spore,Colors.white),
          Item("Spore",chars.spore,Colors.white)
        ],
        ['a', 2, 'd']  # enemies
      ],[
        100, # timer
        [],  # items
        [1, 2, 3]  # enemies
      ]
    ]
