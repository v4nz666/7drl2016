from entities import Node
from sporenetwork import SporeNetwork

__author__ = 'jripley'

class Shroom(Node):
  active = False
  netRadius = 12

  def activate(self, player):
    self.active = True
    self.player = player
    self.initNetwork()

  def initNetwork(self):
    self.net = SporeNetwork(self.map)

  def inNetwork(self, x, y):
    return self.net.field[x + y * self.map.width]

  @property
  def netSize(self):
    return self.net.size
