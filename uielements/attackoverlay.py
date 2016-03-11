__author__ = 'jripley'

from RoguePy.UI import Colors
from RoguePy.libtcod import libtcod
from RoguePy.UI.Elements import Element


class AttackOverlay(Element):
  def __init__(self, x, y, w, h):
    print "attack overlay created"
    super(AttackOverlay, self).__init__(x, y, w, h)
    self.bgOpacity = 0;
    self.explConsole = libtcod.console_new(w, h)


  def draw(self):
    # we never set ourselves to dirty, so the overlay is always cleared
    map = self.parent.map
    for a in map.attacks:
      x, y = self.parent.onScreen(a.x, a.y)
      if not 0 <= x < self.width or not 0 <= y < self.height:
        continue
      if not a.explosion:
        libtcod.console_put_char_ex(self.console, x, y, a.ch, Colors.crimson, Colors.black)
        self.parent.setDirty()
      else:
        self.drawExplosion(a)
        self.parent.setDirty()

  def drawExplosion(self, a):
    print "Drawing Explosion at", a.x, a.y
    for _x, _y in a.explosion.coords:
      x, y = self.parent.onScreen(_x, _y)
      if not 0 <= x < self.width or not 0 <= y < self.height:
        continue
      libtcod.console_put_char_ex(
        self.console, x, y, a.explosion.ch, Colors.white, Colors.black)
    self.parent.map.removeAttack(a)



