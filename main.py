__author__ = 'jripley'
from states import *
from RoguePy.Game import Game

# Shenanigans to get RoguePy in the search path when it's the project root.
import sys
from config import *

import RoguePy
from RoguePy.Input import Keys
from RoguePy.UI import Elements

RoguePy.setFps(30)

game = Game("Sporaculous", 96, 60, False)
game.addState(SplashState('splash'))
game.addState(GenerateState('generate'))
game.addState(PlayState('play'))

game.run('splash')
