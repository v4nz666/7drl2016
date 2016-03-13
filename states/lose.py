__author__ = 'jripley'
import sys
from RoguePy import State
from RoguePy.Input import Keys
from RoguePy.UI import Elements, Colors
import config


class LoseState(State.GameState):
  def init(self):
    loseString = 'You lose!'
    loseX = (config.ui['uiWidth'] - len(loseString)) / 2
    loseY = config.ui['uiHeight'] / 2 - 3
    lose = Elements.Label(loseX, loseY, loseString)\
      .setDefaultForeground(Colors.dark_crimson)
    self.view.addElement(lose)

    safeString = 'The forest is overrun.'
    safeX = (config.ui['uiWidth'] - len(safeString)) / 2
    safeY = config.ui['uiHeight'] / 2 - 2
    safe = Elements.Label(safeX, safeY, safeString)\
      .setDefaultForeground(Colors.darker_crimson)
    self.view.addElement(safe)

    pressKeyString = 'Esc - Quit'
    pressKeyX = (config.ui['uiWidth'] - len(pressKeyString)) / 2
    pressKeyY = config.ui['uiHeight'] / 2
    pressKey = Elements.Label(pressKeyX, pressKeyY, pressKeyString)\
      .setDefaultForeground(Colors.darker_grey)
    self.view.addElement(pressKey)

    self.setupInputs()

  def setupInputs(self):
    # Inputs. =================================================================================
    self.view.setInputs({
      'quit' : {
        'key' : Keys.Escape,
        'ch'  : None,
        'fn'  : sys.exit
      }
    })
