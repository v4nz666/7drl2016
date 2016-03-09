from RoguePy.libtcod import libtcod

__author__ = 'jripley'

import sys

import config
from RoguePy.Input import Keys
from RoguePy.UI import Elements
from RoguePy.UI import Colors
from RoguePy.State import GameState

class SplashState(GameState):
  def init(self):

    self.setupView()
    self.setupInputs()

  def setupView(self):
    titleString = 'Sporaculous'
    titleX = (config.ui['uiWidth'] - len(titleString)) / 2
    titleY = config.ui['uiHeight'] / 2 - 3
    title = Elements.Label(titleX, titleY, titleString)\
      .setDefaultForeground(Colors.dark_crimson)
    self.view.addElement(title)

    # ### Ascii mapping test
    # con = self.view.console
    # for j in range(16):
    #   y = j * 2
    #   for i in range(16):
    #     x = (i*6)
    #     h = i + (j * 16)
    #
    #     print h
    #     libtcod.console_print(con,x, y, "%d:".ljust(4) % h)
    #     libtcod.console_put_char(con, x + 4, y, h)
    # libtcod.console_blit(con,0, 0, self.view.width, self.view.height, 0, 0, 0)
    # libtcod.console_flush()
    # libtcod.console_wait_for_keypress(True)




  def setupInputs(self):
    def toGenerate():
      self.manager.setNextState('generate')

    # Inputs. =================================================================================
    self.view.setInputs({
      'quit' : {
        'key' : Keys.Escape,
        'ch'  : None,
        'fn'  : sys.exit
      },
      'next' : {
        'key' : 'any',
        'ch'  : None,
        'fn'  : toGenerate
      }
    })
