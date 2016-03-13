from RoguePy.libtcod import libtcod
from RoguePy.UI.Elements import Element
from collections import namedtuple
from .. import Colors

CellView = namedtuple('CellView', ['char', 'fg', 'bg'])

class Map(Element):
  def __init__(self, x, y, w, h, map):
    super(Map, self).__init__(x, y, w, h)
    self.map = map
    self._offsetX = 0
    self._offsetY = 0
    self.halfW = self.width / 2
    self.halfH = self.height / 2

  def center(self, x, y):
    """
    Centers the view-port of the ui element around coordinates x, y of the map. If the coordinate is near the edge of
    the map, the actual center of the view-port will differ from those passed in. 
    
    See also: onScreen() - Return the onscreen coordinates of a given x, y pair accounting for centering.
    
    :param x: X coordinate to center view around
    :param y: Y coordinate to center view around
    :return: self
    """
    if x < self.halfW:
      self._offsetX = 0
    elif x < self.map.width - self.halfW:
      self._offsetX = x - self.halfW
    else:
      self._offsetX = self.map.width - self.width
    
    if y < self.halfH:
      self._offsetY = 0
    elif y < self.map.height - self.halfH:
      self._offsetY = y - self.halfH
    else:
      self._offsetY = self.map.height - self.height
    self.setDirty()
    return self


  def onScreen(self, x, y):
    """
    Return the onscreen coordinates of a given x, y pair accounting for centering.

    :param x: int   The actual map X coordinate to calculate the onscreen coordinate of.
    :param y: int   The actual map X coordinate to calculate the onscreen coordinate of.
    :return: tuple  Adjusted (x, y) coordinates
    """
    return (x - self._offsetX, y - self._offsetY)
  
  def draw(self):
    for sy in range(self.height):
      for sx in range(self.width):
        x = sx + self._offsetX
        y = sy + self._offsetY
        if (x >= 0 and x < self.map.width and y >= 0 and y < self.map.height):
          c = self.map.getCell(x, y)
          cv = self.cellToView(c)
          libtcod.console_put_char_ex(self.console, sx, sy, cv.char, cv.fg, cv.bg)

    self.setDirty(False)

  def cellToView(self, c):
    result = CellView(c.terrain.char, c.terrain.fg, c.terrain.bg)
    if c.entity is not None:
      result = CellView(c.entity.ch, c.entity.fg, result.bg)
    elif c.item:
      result = CellView(c.item.ch, c.item.fg, result.bg)
    return result

  # TODO: Does this belong here, or in View? It's a bit hackish because we only want to replace
  #   a subset of the inputs, not the whole input set.
  # TODO: If input binding is streamlined, this won't work anymore.
  def setDirectionalInputHandler(self, fn, wasd=True, vim=True):
    from RoguePy.Input import Keys
    self._inputs['move_sw'] = {
        'key' : Keys.NumPad1,
        'ch'  : None,
        'fn'  : lambda: fn(-1,1)
    }
    self._inputs['move_s'] = {
        'key' : Keys.NumPad2,
        'ch'  : None,
        'fn'  : lambda: fn(0,1)
    }
    self._inputs['move_se'] = {
        'key' : Keys.NumPad3,
        'ch'  : None,
        'fn'  : lambda: fn(1,1)
    }
    self._inputs['move_w'] = {
        'key' : Keys.NumPad4,
        'ch'  : None,
        'fn'  : lambda: fn(-1,0)
    }
    self._inputs['move_none'] = {
        'key' : Keys.NumPad5,
        'ch'  : None,
        'fn'  : lambda: fn(0,0)
    }
    self._inputs['move_e'] = {
        'key' : Keys.NumPad6,
        'ch'  : None,
        'fn'  : lambda: fn(1,0)
    }
    self._inputs['move_nw'] = {
        'key' : Keys.NumPad7,
        'ch'  : None,
        'fn'  : lambda: fn(-1,-1)
    }
    self._inputs['move_n'] = {
        'key' : Keys.NumPad8,
        'ch'  : None,
        'fn'  : lambda: fn(0,-1)
    }
    self._inputs['move_ne'] = {
        'key' : Keys.NumPad9,
        'ch'  : None,
        'fn'  : lambda: fn(1,-1)
    }
    
    if wasd:
      self._inputs['wasd_sw'] = {
          'key' : None,
          'ch'  : "z",
          'fn'  : lambda: fn(-1,1)
      }
      self._inputs['wasd_s'] = {
          'key' : None,
          'ch'  : "s",
          'fn'  : lambda: fn(0,1)
      }
      self._inputs['wasd_se'] = {
          'key' : None,
          'ch'  : "c",
          'fn'  : lambda: fn(1,1)
      }
      self._inputs['wasd_w'] = {
          'key' : None,
          'ch'  : "a",
          'fn'  : lambda: fn(-1,0)
      }
      self._inputs['wasd_none'] = {
          'key' : None,
          'ch'  : "x",
          'fn'  : lambda: fn(0,0)
      }
      self._inputs['wasd_e'] = {
          'key' : None,
          'ch'  : "d",
          'fn'  : lambda: fn(1,0)
      }
      self._inputs['wasd_nw'] = {
          'key' : None,
          'ch'  : "q",
          'fn'  : lambda: fn(-1,-1)
      }
      self._inputs['wasd_n'] = {
          'key' : None,
          'ch'  : "w",
          'fn'  : lambda: fn(0,-1)
      }
      self._inputs['wasd_ne'] = {
          'key' : None,
          'ch'  : "e",
          'fn'  : lambda: fn(1,-1)
      }
      
    if vim:
      self._inputs['vim_sw'] = {
          'key' : None,
          'ch'  : "b",
          'fn'  : lambda: fn(-1,1)
      }
      self._inputs['vim_s'] = {
          'key' : None,
          'ch'  : "j",
          'fn'  : lambda: fn(0,1)
      }
      self._inputs['vim_se'] = {
          'key' : None,
          'ch'  : "n",
          'fn'  : lambda: fn(1,1)
      }
      self._inputs['vim_w'] = {
          'key' : None,
          'ch'  : "h",
          'fn'  : lambda: fn(-1,0)
      }
      self._inputs['vim_e'] = {
          'key' : None,
          'ch'  : "l",
          'fn'  : lambda: fn(1,0)
      }
      self._inputs['vim_nw'] = {
          'key' : None,
          'ch'  : "y",
          'fn'  : lambda: fn(-1,-1)
      }
      self._inputs['vim_n'] = {
          'key' : None,
          'ch'  : "k",
          'fn'  : lambda: fn(0,-1)
      }
      self._inputs['vim_ne'] = {
          'key' : None,
          'ch'  : "u",
          'fn'  : lambda: fn(1,-1)
      }
    
