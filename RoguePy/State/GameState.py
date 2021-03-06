'''
GameState
'''
from RoguePy import Input
from RoguePy.UI import View
from TickHandler import TickHandler


class GameState(object):
  def __init__(self, name, manager = None):
    self.name = name
    self.manager = manager
    self.inputHandler = Input.KeyboardHandler()

    self.tickHandlers = {}
    self.handlerQueue = []
    
    self.focused = None

  def init(self):
    pass

  # Clear all existing views, and create one covering the entire ui
  def initView(self, ui):
    self.__views = [View(ui.width, ui.height)]

  # Add a view onto the stack
  def addView(self, view):
    self.__views.append(view)
    return view
  # Pop a view off the stack
  def removeView(self):
    if not len(self.__views) > 1 :
      raise IndexError("Tried to close last View on stack")
    self.__views.pop()

  @property
  def name(self):
    return self.__name
  @name.setter
  def name(self,name):
    self.__name = name
  
  @property
  def manager(self):
    return self.__manager
  @manager.setter
  def manager(self,manager):
    self.__manager = manager
  
  @property
  def inputHandler(self):
    return self.__inputHandler
  @inputHandler.setter
  def inputHandler(self, h):
    if isinstance(h, Input.InputHandler):
      self.__inputHandler = h

  @property
  def view(self):
    return self.__views[-1]

  def addHandler(self, name, interval, handler):
    if not name in self.tickHandlers:
      self.tickHandlers[name] = TickHandler(interval, handler)
  def removeHandler(self, name):
    self.handlerQueue.append(name)

  def purgeHandlers(self):
    for name in self.handlerQueue:
      if name in self.tickHandlers:
        del self.tickHandlers[name]
    self.handlerQueue = []

  def processInput(self):
    inputs = {}
    if self.view.inputsEnabled:
      inputs.update(self.view.getInputs())
    if self.focused is not None:
      inputs.update(self.focused.getInputs())
    self.inputHandler.setInputs(inputs)
    self.inputHandler.handleInput()

  def setFocus(self, el):
    self.focused = el

  def blur(self):
    self.focused = None

  def beforeLoad(self):
    pass
  def beforeUnload(self):
    pass
