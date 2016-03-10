from RoguePy.Game import Entity

__author__ = 'jripley'

class Construct(Entity):
  def setRequired(self, req):
    self.required = req
    return self

