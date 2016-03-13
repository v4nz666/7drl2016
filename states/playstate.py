import RoguePy
from RoguePy.Game.Item import Item
from attack import Attack
from buildsite import BuildSite
import chars
from enemies import *
from entities import Shroom, Node, Enemy
from entities import Construct
import items
import uielements

__author__ = 'jripley'

import sys

import config as cfg
from RoguePy.Input import Keys
from RoguePy.UI import Elements
from RoguePy.UI import Colors
from RoguePy.State import GameState
from RoguePy.libtcod import libtcod
class PlayState(GameState):

  def init(self):
    self.waves = []
    self.mana = 0

  def beforeUnload(self):
    self.messageList.messages = []
    self.messageList.clear()
    self.view.setDirty()

  def setupHandlers(self):

    self.addHandler('hudRefresh', 1, self.hudRefresh)
    self.addHandler('loseCheck', 1, self.loseCheck)
    self.addHandler('attackAnim', 2, self.mapElement.updateAttacks)
    self.addHandler('buildAnim', 2, self.mapElement.updateBuildAnimation)
    self.turnHandlers = [self.buildSiteUpdate]

  def setupView(self):

    # Map
    self.mapElement = uielements.GameMap(0, 0, cfg.ui['msgX'], cfg.ui['uiHeight'], self.map)
    self.view.addElement(self.mapElement)

    #Magix
    self.magicOverlay = self.view.addElement(Elements.Element(0, 0, cfg.ui['msgX'], cfg.ui['uiHeight']))
    self.magicOverlay.bgOpacity = 0
    self.magicOverlay.hide()

    def drawMagicOverlay():
      con = self.magicOverlay.console
      onscreenX, onscreenY = self.mapElement.onScreen(self.focusX, self.focusY)
      libtcod.console_put_char(con, onscreenX, onscreenY, '+')
    self.magicOverlay.draw = drawMagicOverlay
    # HUD
    self.fps = Elements.Label(1, 1, "FPS: ".ljust(8))\
      .setDefaultForeground(Colors.magenta)
    self.fps.bgOpacity = 0
    self.view.addElement(self.fps)

    self.waveEnemyLabel = Elements.Label(cfg.ui['msgX'], 2, "Enemies: ".ljust(cfg.ui['msgW']))
    self.waveEnemyLabel.bgOpacity = 0
    self.waveEnemyLabel.setDefaultForeground(Colors.dark_fuchsia)
    self.waveEnemyLabel.hide()
    self.view.addElement(self.waveEnemyLabel)

    self.waveTimerLabel = Elements.Label(cfg.ui['msgX'], 1, "Next Wave: ".ljust(cfg.ui['msgW']))
    self.waveTimerLabel.bgOpacity = 0
    self.waveTimerLabel.setDefaultForeground(Colors.dark_fuchsia)
    self.waveTimerLabel.hide()
    self.view.addElement(self.waveTimerLabel)

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

    # Help
    mapW = cfg.ui['uiWidth'] - cfg.ui['msgW']
    helpW = mapW / 2
    helpX = (mapW - helpW)/ 2
    helpY = cfg.ui['uiHeight'] / 4 - 2

    helpH = (cfg.ui['uiHeight'] - helpY) / 2 + 3
    self.helpDialog = Elements.Frame(helpX, helpY, helpW, helpH, "Help!")

    self.helpText = Elements.List(1,1, self.helpDialog.width - 2, self.helpDialog.height - 2)
    self.helpText.setItems([
      "   Movement         Ranged Attack ",
      "    WASD             Tab - Toggle ",
      "    NUMPAD      Movement - Aim    ",
      "    VI               Spc - Fire   ",
      "Drop spores with Space to increase",
      "the size of your  mycelial network",
      "                                  ",
      "Your strength increases  with  the",
      "number of nodes  in  the  network ",
      "                                  ",
      "The size of the network determines",
      "the rate of mana collection       ",
      "                                  ",
      "Attack with the magic you've  been",
      "given or get up close and personal",
      "                                  ",
      "Fend off all the waves to win     ",
      "                                  ",
      "You  lose  if  you  or the Magical",
      "Mushroom are killed               ",
      "                                  ",
      "Terrain type affects movement cost",
      "                                  ",
      "Use the terrain to your advantage "
    ])
    self.helpDialog.addElement(self.helpText)
    self.mapElement.addElement(self.helpDialog).hide()
    helpLabel = Elements.Label(5, self.mapElement.height - 1, "? - Help")
    helpLabel.bgOpacity = 0
    self.mapElement.addElement(helpLabel)\
      .setDefaultForeground(Colors.gold)


  def toggleHelp(self):
    if self.helpDialog.visible:
      self.helpDialog.hide()
      self.mapElement.setDirty()
      self.setFocus(self.mapElement)
    else:
      self.helpDialog.show()
      self.setFocus(self.helpDialog)

  def setupInputs(self):
    # Inputs. =================================================================================

    self.view.setInputs({
      'slash': {
        'key' : None,
        'ch': '/',
        'fn': self.toggleHelp
      },
      '?': {
        'key' : None,
        'ch': '?',
        'fn': self.toggleHelp
      },
      'hideHelp' : {
        'key' : Keys.Escape,
        'ch'  : None,
        'fn'  : self.toggleHelp
      }
    })

    self.mapElement.setInputs({
      'use': {
        'key' : Keys.Space,
        'ch': None,
        'fn': self.useItem
      },
      'magic': {
        'key' : Keys.Tab,
        'ch': None,
        'fn': self.enableMagic
      },
      'quit' : {
        'key' : Keys.Escape,
        'ch'  : None,
        'fn'  : sys.exit
      }
    })

    self.magicOverlay.setInputs({
      'escape': {
        'key' : Keys.Escape,
        'ch': None,
        'fn': self.disableMagic
      },
      'tab': {
        'key' : Keys.Tab,
        'ch': None,
        'fn': self.disableMagic
      },
      'fire!': {
        'key' : Keys.Space,
        'ch': None,
        'fn': self.fireMagic
      }
    })

    self.magicOverlay.setDirectionalInputHandler(self.moveMagic)
    self.mapElement.setDirectionalInputHandler(self.movePlayer)
    self.setFocus(self.mapElement)

##########################
#Input callbacks
  def useItem(self):
    i = self.player.item

    if not i:
      return False

    if i.use(self.player.x, self.player.y):
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

  def moveMagic(self,dx,dy):
    if not dx and not dy:
      self.doTurn()
      return
    newX = self.focusX + dx
    newY = self.focusY + dy

    onscreenX, onscreenY = self.mapElement.onScreen(newX, newY)
    if not 0 <= onscreenX < self.magicOverlay.width or not 0 <= onscreenY < self.magicOverlay.height:
      return

    self.focusX = newX
    self.focusY = newY

    return

  def fireMagic(self):
    print "Firing"
    if self.map.shroom.inNetwork(self.focusX, self.focusY):
      if self.player.readyToAttack():
        if self.testMana(self.player.attackCost):
          self.player.attack((self.focusX, self.focusY))
        else:
          self.messageList.message("Not enough mana!")
      else:
        self.messageList.message("You need time to recover")

      self.disableMagic(True)
    else:
      self.messageList.message("You have no power, outside the network")


  def enableMagic(self):
    if not self.map.shroom.active:
      return
    if not self.map.shroom.inNetwork(self.player.x, self.player.y):
      self.messageList.message("You feel weak away from the network")
    self.focusX = self.player.x
    self.focusY = self.player.y
    self.magicOverlay.show()
    self.setFocus(self.magicOverlay)

  def disableMagic(self, turn = False):
    self.magicOverlay.hide()
    self.setFocus(self.mapElement)
    if turn:
      self.doTurn()


##########################
# Item use callbacks
  def setupItems(self):
    def useSpore(x, y):
      if not self.map.shroom.inNetwork(x, y):
        self.messageList.message("Can not deploy spore outside of mycelial network")
        return False
      self.map.addBuildSite(x, y, BuildSite(5, Node("Node", chars.node, Colors.white, cfg.node)))
      self.messageList.message("You place the spore in the ground")
      return True
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
          if self.map.getCell(_x, _y).passable:
            print "Player: %d, %d" % (_x, _y)
            player = Player('Sporaculous', '@', Colors.white, cfg.player)
            player.spawn(self.map, _x, _y, cfg.player['hp'])
            return player

        except IndexError:
          pass
    print "Player not placed!"

  def setMap(self,map):
    self.map = map
    self.setupView()

    self.player = self.spawnPlayer()
    self.map.setPlayer(self.player)
    self.mapElement.setPlayer(self.player)
    self.mapElement.calculateFovMap()
    self.mapElement.center(self.player.x, self.player.y)

    self.setupHandlers()
    self.setupInputs()
    self.setupEvents()
    self.setupItems()


  def setupEvents(self):
    self.map.on('item_interact', self.itemInteract)
    self.map.on('entityAttack', self.entityAttack)
    self.map.on('entityInteract', self.entityInteract)
    self.map.on('moveWait', self.moveWait)

  def moveWait(self, s, t):
    print "move wait"
    return self.doTurn()
  def entityInteract(self, src, target):
    # Special player handling
    if src == self.player:
      # self.messageList.message("Player hit %s" % target.name)
      if target.name == "Shroom" and not target.active:
        self.activateShroom(target)
        self.setupWaves()
        return
      elif target.name == "Node":
        #ignore player-node interactions
        return
      else:
        self.player.attack(target, True)
        return
    #otherwise, just pass through to entityAttack
    self.entityAttack(src, target)

  def entityAttack(self, src, target):
    if target.isDead:
      return

    dmg = (src.damage * 0.5) + (0.5  * cfg.randint(src.damage))
    msg = "%s hit %s for [%d] damage"
    if target.takeDamage(dmg):
      msg = "%s killed %s! [%d] damage"
      target.die()
      if isinstance(target, Enemy):
        self.purgeEnemies()
    self.messageList.message(msg % (src.name, target.name, dmg))

  def doTurn(self):
    self.player.tick()
    for h in self.turnHandlers:
      h()

  def activateShroom(self, shroom):
    self.messageList.message("As you approach the mushroom, your vision swirls.")
    shroom.activate(self.player)
    self.updateNetFrame()

    self.turnHandlers.append(self.collectMana)
    self.turnHandlers.append(self.nodeUpdate)

  def setupWaves(self):
    self.waves = []
    for wp in Wave.All():
      self.waves.append(Wave(*wp))
    self.initNextWave(first=True)
    self.turnHandlers.append(self.waveUpdate)


  # Spawn enemies, and deliver the items for the next wave
  def initNextWave(self, first=False):
    if not first:
      self.waves.pop(0)
      if not len(self.waves):
        self.removeHandler('enemyPaths')
        return
    else:
      self.addHandler('enemyPaths', 120, self.repathEnemies)
      self.waveTimerLabel.show()
      self.waveEnemyLabel.show()
      self.invFrame.show()
      self.netFrame.show()
    self.spawnItems(self.waves[0].items)

  def spawnEnemies(self, waveEnemies):
    side = cfg.randint(3)
    passable = lambda x1, y1, x2, y2, blech: int(self.map.getCell(x2, y2).passable)

    enemies = []
    for e in range(len(waveEnemies)):
      attempts = 0
      while attempts < 10:
        enemy = waveEnemies[e]
        (x, y) = self.findSuitableSpawnPoint(side)
        path = libtcod.path_new_using_function(self.map.width, self.map.height, passable)
        libtcod.path_compute(path, x, y, self.map.shroom.x, self.map.shroom.y)
        s = libtcod.path_size(path)
        if s:
          enemy.spawn(self.map, x, y, enemy.hp)
          enemies.append(enemy)
          self.messageList.message("%s spawned" % enemy.name)
          libtcod.path_delete(path)
          break
        else:
          attempts += 1
      self.waves[0].enemies = enemies

  def findSuitableSpawnPoint(self, side):
    while True:
      if side == 0:
        y = 0
        x = cfg.randint(self.map.width-1)
      elif side == 1:
        x = self.map.width - 1
        y = cfg.randint(self.map.height-1)
      elif side == 2:
        y = self.map.height - 1
        x = cfg.randint(self.map.width-1)
      else:
        x = 0
        y = cfg.randint(self.map.height-1)
      c = self.map.getCell(x, y)
      if not c.passable:
        continue
      if c.entity:
        continue
      return x, y

  def spawnItems(self, items):
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

  def loseCheck(self):
    if self.map.shroom.isDead or self.player.isDead:
      self.manager.setNextState('lose')

  def hudRefresh(self):
    self.fps.setLabel("FPS: %r" % (libtcod.sys_get_fps()))
    
    if len(self.waves):
      self.waveTimerLabel.setLabel("Next Wave: %s" % self.waves[0].timer)
      self.waveEnemyLabel.setLabel("Enemies: %s" % len(self.waves[0].enemies))


  def updateNetFrame(self):
    maxMana = int(self.map.shroom.net.maxMana)
    self.netManaVal.setLabel(("%d / %d" % (int(self.mana), maxMana)).rjust(cfg.ui['netW']-2))
    self.netSizeVal.setLabel(str(self.map.shroom.netSize).rjust(cfg.ui['netW']-2))
    self.netRateVal.setLabel(str(round(self.map.shroom.netSize * cfg.manaRate, 2)).rjust(cfg.ui['netW']-2))
    self.netFrame.setDirty()


##############################
# Turn handlers

  def waveUpdate(self):
    wave = self.waves[0]

    if wave.timer > 0:
      wave.timer -= 1
      return
    elif not wave.active:
      self.spawnEnemies(self.waves[0].enemies)
      wave.active = True
    if len(wave.enemies):
      self.updateEnemies()
    else:
      self.messageList.message("wave complete")
      self.initNextWave()

    if len(self.waves) == 0:
      self.messageList.message("you win!!!!")
      self.removeHandler('repathEnemies')
      self.turnHandlers.remove(self.collectMana)
      self.turnHandlers.remove(self.nodeUpdate)
      self.turnHandlers.remove(self.waveUpdate)

      # WIN !
      self.manager.setNextState('win')


  def updateEnemies(self):
    for e in self.waves[0].enemies:
      if e.isDead:
        continue
      e.takeTurn()

  def repathEnemies(self):
    if not len(self.waves):
      return
    print "repathing"
    for e in self.waves[0].enemies:
      if e.isDead:
        continue
      e.updateTarget()


  def purgeEnemies(self):
    print "purging"
    purge = []
    for e in self.waves[0].enemies:
      if e.isDead:
        purge.append(e)
    for e in purge:
      self.waves[0].enemies.remove(e)
    self.hudRefresh()

  def collectMana(self):
    net = self.map.shroom.net
    cells = net.size
    self.mana += round(cells * cfg.manaRate, 2)
    self.mana = min(net.maxMana, self.mana)
    self.updateNetFrame()

  def nodeUpdate(self):
    network = self.map.shroom.net
    nodes = network.nodes
    for n in nodes:
      n.tick()
      if n.isDead:
        network.removeNode(n)
        n.die()
        self.mapElement.setDirty()
        continue

      t = n.findTarget()
      if t and n.readyToAttack():
        if self.testMana(n.attackCost):
          n.attack(t)
        else:
          self.messageList.message("Node can't attack. Not enough mana")

  def testMana(self, cost):
    if self.mana >= cost:
      self.mana -= cost
      self.updateNetFrame()
      return True
    else:
      return False


  def buildSiteUpdate(self):
    for x, y in self.map.buildSites:
      site = self.map.buildSites[(x,y)]
      site.timer -= 1
      if not site.timer:
        if site.entity.spawn(self.map, x, y, cfg.node['hp']):
          self.map.shroom.net.addNode(site.entity)
          self.messageList.message("You feel your power increase")
        else:
          #Failed to add (Entity present), try again next turn
          site.timer = 1
    self.map.purgeBuildSites()


class Wave():
  def __init__(self, timer, items, enemies):
    self.active = False
    self.timer = timer
    self.items = items
    self.enemies = enemies

  @staticmethod
  def All():
    return [
      [ ### Wave 1
        1, #timer
        [    # items
             items.spore,
             items.spore,
        ],
        [
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*playerHunter),
          Enemy(*playerHunter)
        ]  # enemies
      ],[ ### Wave 2
        25, #timer
        [    # items
             items.spore,
             items.spore,
             items.spore,
        ],
        [
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*shroomHunter),
          Enemy(*shroomHunter),
          Enemy(*shroomHunter),
          Enemy(*playerHunter),
          Enemy(*playerHunter),
          Enemy(*playerHunter),

          ]  # enemies
      ],[ ### Wave 3
        60, #timer
        [    # items
             items.spore,
             items.spore,
             items.spore,
             items.spore,
        ],
       [
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*shroomHunter),
          Enemy(*shroomHunter),
          Enemy(*shroomHunter),
          Enemy(*shroomHunter),
          Enemy(*shroomHunter),
          Enemy(*shroomHunter),
          Enemy(*playerHunter),
          Enemy(*playerHunter),
          Enemy(*playerHunter),
          Enemy(*playerHunter),

        ]  # enemies
      ],[ ### Wave 4
        75, #timer
        [    # items
             items.spore,
             items.spore,
             items.spore,
             items.spore,
             items.spore,
        ],
        [
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*shroomHunter),
          Enemy(*shroomHunter),
          Enemy(*shroomHunter),
          Enemy(*shroomHunter),
          Enemy(*shroomHunter),
          Enemy(*shroomHunter),
          Enemy(*shroomHunter),
          Enemy(*shroomHunter),
          Enemy(*shroomHunter),
          Enemy(*playerHunter),
          Enemy(*playerHunter),
          Enemy(*playerHunter),
          Enemy(*playerHunter),
          Enemy(*playerHunter),
          Enemy(*playerHunter),
          Enemy(*playerHunter),
        ]  # enemies
      ],[ ### Wave 5
        100, #timer
        [    # items
             items.spore,
             items.spore,
             items.spore,
             items.spore,
             items.spore,
             items.spore,
        ],
        [
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*nodeHunter),
          Enemy(*shroomHunter),
          Enemy(*shroomHunter),
          Enemy(*shroomHunter),
          Enemy(*shroomHunter),
          Enemy(*shroomHunter),
          Enemy(*shroomHunter),
          Enemy(*shroomHunter),
          Enemy(*shroomHunter),
          Enemy(*shroomHunter),
          Enemy(*shroomHunter),
          Enemy(*shroomHunter),
          Enemy(*shroomHunter),
          Enemy(*shroomHunter),
          Enemy(*shroomHunter),
          Enemy(*playerHunter),
          Enemy(*playerHunter),
          Enemy(*playerHunter),
          Enemy(*playerHunter),
          Enemy(*playerHunter),
          Enemy(*playerHunter),
          Enemy(*playerHunter),
          Enemy(*playerHunter),
          Enemy(*playerHunter),
          Enemy(*playerHunter),
          Enemy(*playerHunter),
        ]  # enemies
      ]
    ]
