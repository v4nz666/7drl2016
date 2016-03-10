from ..UI import Colors

class Item:
  def __init__(self, name, ch, fg):
    self.name = name
    self.ch = ch
    self.fg = fg

    self.desc = ""



  def use(self, x, y):
    print self.name, " used"
    pass
