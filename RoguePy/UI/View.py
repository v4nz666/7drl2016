'''
Documentation, License etc.

@package RoguePy.UI
'''
from RoguePy.libtcod import libtcod

class View(object):

  def __init__(self, w, h, x=0, y=0 ):

    self.width = w
    self.height = h
    self.x = x
    self.y = y

    self.setDirty(True)

    self._elements = []
    self._inputs = {}
    
    self._storedEnabled = None
    
    self.console = libtcod.console_new(self.width, self.height)
    self.inputsEnabled = True
    self.fg = libtcod.white
    self.bg = libtcod.black

  def clearAll(self):

    self.clear()

    for e in self._elements:
      e.clearAll()
    self._elements = []
    self._inputs = {}

  def getElements(self):
    return self._elements
  
  def getConsole(self):
    return self.console
  
  def addElement(self, el):
    if el.x + el.width >= self.width:
      el.width = self.width - el.x
    if el.y + el.height>= self.height:
      el.height = self.height - el.y

    self._elements.append(el)
    el.setParent(self)
    return el
  def removeElement(self, el):
    if el in self._elements:
      self._elements.remove(el)
    self.setDirty()
  
  def setInputs(self, inputs):
    """
    Set the inputs to be bound to this View/Element

    :param inputs: Dictionary of input definitions. Takes the format:
      {
        'quit': {
          'key': libtcod.KEY_ESCAPE,
          'char': None,
          'fn': self.quitCallback
        },
        ...,
        'goNorth': {
          'key': libtcod.KEY_CHAR,
          'char': 'n',
          'fn': self.move
        },
        ...
      }
    """
    self._inputs = inputs
  def getInputs(self):
    return self._inputs

  def storeState(self):
    """
    Store the enabled status of all elements. This method must be called prior to calling restoreState. Use this method
      in conjunction with the disableAll method to put the view into "modal" mode, by calling them, then manually
      enabling an element.


    :return: None
    """
    self._storedEnabled = []
    index = 0
    for e in self._elements:
      if e.enabled:
        self._storedEnabled.append(index)
      index += 1
  def restoreState(self):
    """
    Restore the enabled state of all elements previously stored via storeState.

    :raise Exception: When called before a call to storeState.
    """
    if not self._storedEnabled:
      raise Exception("You must call storeState before calling restoreState.")
    for index in self._storedEnabled:
      self._elements[index].enable()
  
  def disableAll(self, disableSelf=True):
    """
    Disable all elements. Disabled elements are rendered with a low-opacity overlay of their bg color.

    :param disableSelf: Also disable the Inputs bound directly to the View? Defaults to True
    """
    for e in self._elements:
      e.disable()
    if disableSelf:
      self.disableInputs()
  
  def enableInputs(self):
    self.inputsEnabled = True
  def disableInputs(self):
    self.inputsEnabled = False

  def setDirty(self, dirty=True):
    self._dirty = dirty
    return self

  def isDirty(self):
    return self._dirty


  def setDefaultForeground(self, fg, cascade=False):
    self.fg = fg
    libtcod.console_set_default_foreground(self.console,fg)

    if cascade:
      for e in self._elements:
        e.setDefaultForeground(fg, True)

    self.setDirty()
    return self

  def setDefaultBackground(self, bg, cascade=False):
    self.bg = bg
    libtcod.console_set_default_background(self.console,bg)
    if cascade:
      for e in self._elements:
        e.setDefaultBackground(bg, True)

    self.setDirty()

  #TODO Convert fg, bg to a tuple
  def setDefaultColors(self, fg = libtcod.white, bg = libtcod.black, cascade=False):
    self.setDefaultForeground(fg, cascade)
    self.setDefaultBackground(bg, cascade)
    return self
  
  def getDefaultColors(self):
    return self.fg, self.bg

  ###
  # Drawing methods
  ###

  def clear(self):
    libtcod.console_clear(self.console)
    self.setDirty()
    return self

  def putCh(self, x, y, ch, fg, bg):
    libtcod.console_put_char_ex(self.console, x, y, ch, fg, bg)
    self.setDirty()
    
  def renderElements(self):
    for e in self._elements:
      if not e.visible:
        continue
      if e.isDirty():
        e.clear()
        e.draw()
      e.renderElements()
      if not e.enabled:
        self.renderOverlay(e)
      libtcod.console_blit(e.console, 0, 0, e.width, e.height, self.console, e.x, e.y, e.fgOpacity, e.bgOpacity)

  def getDefaultForeGround(self):
    return libtcod.console_get_default_foreground(self.console)

  @staticmethod
  def renderOverlay(el):
    if not (el.width and el.height):
      return
    con = libtcod.console_new(el.width, el.height)
    libtcod.console_set_default_background(con, el.bg)
    libtcod.console_clear(con)
    libtcod.console_blit(con, 0, 0, el.width, el.height, el.console, 0, 0, 0.0, 0.4)
    libtcod.console_delete(con)

    el.setDirty()
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
