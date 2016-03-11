import chars

__author__ = 'jripley'

class Explosion():


  def __init__(self, a):
    self.attack = a
    self.coords = []
    self.ch = chars.smoke

    for y in range(a.y - a.radius, a.y + a.radius + 1):
      for x in range(a.x - a.radius, a.x + a.radius + 1):
        dx = abs(a.x - x)
        dy = abs(a.y - y)
        if (dx**2 + dy**2 <= a.radius**2):
          self.coords.append((x, y))


