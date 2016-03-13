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
    
    creditString = 'Jeff Ripley - 7DRL 2016'
    creditX = (config.ui['uiWidth'] - len(creditString)) / 2
    creditY = config.ui['uiHeight'] / 2 - 2
    credit = Elements.Label(creditX, creditY, creditString)\
      .setDefaultForeground(Colors.dark_grey)
    self.view.addElement(credit)
    
    pressKeyString = 'Press any key'
    pressKeyX = (config.ui['uiWidth'] - len(pressKeyString)) / 2
    pressKeyY = config.ui['uiHeight'] / 2
    pressKey = Elements.Label(pressKeyX, pressKeyY, pressKeyString)\
      .setDefaultForeground(Colors.darker_grey)
    self.view.addElement(pressKey)
    


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
