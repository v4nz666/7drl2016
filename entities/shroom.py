from RoguePy.Game import Entity

__author__ = 'jripley'

class Shroom(Entity):
  active = False

  def activate(self, player):
    self.player = player

    self.active = True