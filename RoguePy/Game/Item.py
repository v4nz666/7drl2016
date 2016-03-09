from ..UI import Colors

class Item:
  def __init__(self, name, ch, fg):
    self.name = name
    self.ch = ch
    self.fg = fg

  def spawn(self, map, x, y):
    if map.addItem(self, x, y):
      self.map = map
      self.x = x
      self.y = y
      return True
    return False
