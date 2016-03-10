from RoguePy.UI import Colors

class Entity(object):
  def __init__(self, name, ch=" ", fg="Color.black"):
    self.name = name
    self.ch = ch
    self.fg = fg

  def setChar(self, ch):
    self.ch = ch
  def setColor(self, color):
    self.fg = color
