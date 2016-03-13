from RoguePy.UI import Colors
from RoguePy.libtcod import libtcod
import chars
import config as cfg

__author__ = 'jripley'

class SporeNetwork():
  def __init__(self, map):
    self.map = map

    self.nodes = [map.shroom]

    self.initField()
    self.calculateField()

  def initField(self):
    self.field = [0 for _i in range(self.map.width * self.map.height)]

  def addNode(self, node):
    if not node in self.nodes:
      self.nodes.append(node)
      self.calculateField(node)

  @property
  def maxMana(self):
    max = 0
    for n in self.nodes:
      max += n.attackCost
    return max

  def removeNode(self, node):
    if node in self.nodes:
      self.nodes.remove(node)
      self.initField()
      self.calculateField()

  def calculateField(self, node=None):
    if node is None:
      nodes = self.nodes
    else:
      nodes = [node]

    w = self.map.width
    h = self.map.height

    #TODO should probably be looping on nodes, and only checking x-rad to x+rad
    for y in range(h):
      for x in range(w):
        for node in nodes:
          if self.withinRadius(x, y, node):
            self.field[x + y * w] = 1
            self.map.getCell(x, y).discover()
            break

  @property
  def size(self):
    return self.field.count(1)

  @staticmethod
  def withinRadius(x, y, node):
    dx = abs(x-node.x)
    dy = abs(y-node.y)
    R = node.range

    if dx>R:
      return False
    if dy>R:
      return False
    if dx + dy <= R:
      return True

    if dx**2 + dy**2 <= R**2:
      return True
    else:
      return False