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
