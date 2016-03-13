import sys
from RoguePy.Input import Keys
from RoguePy.UI import Elements, Colors
import config

__author__ = 'jripley'

from RoguePy import State

class WinState(State.GameState):
  def init(self):
    winString = 'You Win!'
    winX = (config.ui['uiWidth'] - len(winString)) / 2
    winY = config.ui['uiHeight'] / 2 - 3
    win = Elements.Label(winX, winY, winString)\
      .setDefaultForeground(Colors.gold)
    self.view.addElement(win)

    safeString = 'The forest is safe.'
    safeX = (config.ui['uiWidth'] - len(safeString)) / 2
    safeY = config.ui['uiHeight'] / 2 - 2
    safe = Elements.Label(safeX, safeY, safeString)\
      .setDefaultForeground(Colors.silver)
    self.view.addElement(safe)

    pressKeyString = 'Esc - Quit | Space - Play again'
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
      },
      'play': {
        'key' : Keys.Space,
        'ch'  : None,
        'fn'  : lambda: self.manager.setNextState('splash')
      }
    })
