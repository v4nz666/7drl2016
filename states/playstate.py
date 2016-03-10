import RoguePy
from RoguePy.Game.Item import Item
import chars
from entities import Shroom
from entities import Construct
import items
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
    self.mana = 0

  def setupHandlers(self):

    self.addHandler('buildAnim', 12, self.mapElement.updateBuildChar)
    self.addHandler('hudRefresh', 1, self.hudRefresh)
    self.turnHandlers = []

  def setupView(self):

    # Map
    self.mapElement = uielements.GameMap(0, 0, cfg.ui['msgX'], cfg.ui['uiHeight'], self.map)
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

    # Inventory
    self.invFrame = Elements.Frame(cfg.ui['invX'], cfg.ui['invY'], cfg.ui['invW'], cfg.ui['invH'], "Carrying")
    self.invFrame = Elements.Frame(cfg.ui['invX'], cfg.ui['invY'], cfg.ui['invW'], cfg.ui['invH'], "Carrying")
    self.invFrame.setDefaultForeground(Colors.amber)
    self.invFrame.hide()

    self.invItemChar = Elements.Element(1,1, 1,1)

    def drawItemChar():
      if self.player.item:
        ch = self.player.item.ch
      else:
        ch = " "
      libtcod.console_put_char(self.invItemChar.console, 0, 0, ch)
      self.invItemChar.setDirty(False)

    self.invItemChar.draw = drawItemChar
    self.invFrame.addElement(self.invItemChar)

    self.invItemLabel = Elements.Label(3, 1, "Nothing")
    self.invFrame.addElement(self.invItemLabel)

    self.view.addElement(self.invFrame)

    # Network
    self.netFrame = Elements.Frame(cfg.ui['netX'], cfg.ui['netY'], cfg.ui['netW'], cfg.ui['netH'], "net")
    self.netFrame.setDefaultForeground(Colors.green)
    self.netFrame.hide()
    
    self.netManaLabel = Elements.Label(1, 1, "Mana: ").setDefaultForeground(Colors.dark_magenta)
    self.netManaVal = Elements.Label(1, 1, "".rjust(cfg.ui['netW']-2)).setDefaultForeground(Colors.magenta)
    self.netManaVal.bgOpacity = 0
    
    self.netSizeLabel = Elements.Label(1, 2, "Size: ").setDefaultForeground(Colors.dark_magenta)
    self.netSizeVal = Elements.Label(1, 2, "".rjust(cfg.ui['netW']-2)).setDefaultForeground(Colors.magenta)
    self.netSizeVal.bgOpacity = 0
    
    self.netRateLabel = Elements.Label(1, 3, "Rate: ").setDefaultForeground(Colors.dark_magenta)
    self.netRateVal = Elements.Label(1, 3, "".rjust(cfg.ui['netW']-2)).setDefaultForeground(Colors.magenta)
    self.netRateVal.bgOpacity = 0
    
    self.netFrame.addElement(self.netManaLabel)
    self.netFrame.addElement(self.netManaVal)
    self.netFrame.addElement(self.netSizeLabel)
    self.netFrame.addElement(self.netSizeVal)
    self.netFrame.addElement(self.netRateLabel)
    self.netFrame.addElement(self.netRateVal)

    self.view.addElement(self.netFrame)


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

    self.mapElement.setInputs({
      'useItem': {
        'key' : Keys.Space,
        'ch': None,
        'fn': self.useItem
      }

    })

    self.mapElement.setDirectionalInputHandler(self.movePlayer)
    self.setFocus(self.mapElement)

##########################
#Input callbacks
  def useItem(self):
    i = self.player.item

    if not i:
      return False

    i.use(self.player.x, self.player.y)
    self.player.item = None
    self.updateInvFrame()


  def movePlayer(self,dx,dy):
    if self.player.tryMove(dx, dy):
      x, y = self.player.x, self.player.y
      self.mapElement.center(x, y)
      self.mapElement.calculateFovMap()
      self.mapElement.setDirty()
      c = self.map.getCell(x, y)
      if c.item is not None:
        self.map.trigger('item_interact', self.player, c.item)
    self.doTurn()


##########################
# Item use callbacks
  def setupItems(self):
    def useSpore(x, y):
      self.mapElement.addBuildSite(x, y)
      print "BAM Spore deployed"
    items.spore.use = useSpore


##########################
# Event Callbacks
  def itemInteract(self, e, i):
    if e.pickup(i):
      self.map.removeItem(i, self.player.x, self.player.y)
      self.updateInvFrame()
    else:
      self.messageList.message("Can't carry any more")

  def updateInvFrame(self):
    item = self.player.item
    if item:
      i = item.name
      self.invItemChar.setDirty()

    else:
      self.invItemChar.clear()
      i = "Nothing"


    self.invItemLabel.setLabel(i)
    self.invFrame.setDirty()

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

    self.setupHandlers()
    self.setupInputs()
    self.setupEvents()
    self.setupItems()


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
    self.updateNetFrame()

    self.turnHandlers.append(self.collectMana)

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
      if not len(self.waves):
        return
    else:
      self.waveTimerLabel.show()
      self.waveEnemyLabel.show()
      self.invFrame.show()
      self.netFrame.show()

    items = self.waves[0].items
    for i in range(len(items)):
      spawned = False
      while not spawned:

        x = self.map.shroom.x + cfg.randint(12, -12)
        y = self.map.shroom.y + cfg.randint(12, -12)
        if not x and not y:
          continue

        if self.map.addItem(items[i], x, y):
          self.mapElement.setDirty()
          spawned = True

  def hudRefresh(self):
    self.fps.setLabel("FPS: %r" % (libtcod.sys_get_fps()))
    
    if len(self.waves):
      self.waveTimerLabel.setLabel("Next Wave: %s" % self.waves[0].timer)
      self.waveEnemyLabel.setLabel("Enemies: %s" % len(self.waves[0].enemies))


  def updateNetFrame(self):
    self.netManaVal.setLabel(str(self.mana).rjust(cfg.ui['netW']-2))
    self.netSizeVal.setLabel(str(self.map.shroom.netSize).rjust(cfg.ui['netW']-2))
    self.netRateVal.setLabel(str(round(self.map.shroom.netSize * cfg.manaRate, 2)).rjust(cfg.ui['netW']-2))
    self.netFrame.setDirty()


  def collectMana(self):
    cells = self.map.shroom.netSize
    self.mana += round(cells * cfg.manaRate, 2)
    self.updateNetFrame()


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
          items.spore,
          items.spore
        ],
        []  # enemies
      ],[
        100, # timer
        [    # items
          items.spore,
          items.spore
        ],
        []  # enemies
      ]
    ]
