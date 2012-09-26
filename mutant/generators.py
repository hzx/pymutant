from mutant.coffeegen import CoffeeGen
from mutant.pygen import PyGen


class GenFactory(object):

  def __init__(self):
    self.generators = {
        'py': PyGen(),
        'coffee': CoffeeGen(),
        }

  def getNamedGen(self, name):
    return self.generators[name]
