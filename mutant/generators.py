from mutant.coffeegen import CoffeeGen
from mutant.coffeeformatter import CoffeeFormatter
from mutant.pygen import PyGen
from mutant.pyformatter import PyFormatter


class GenFactory(object):

  def createGen(self, name):
    if name == 'py':
      return PyGen()
    if name == 'coffee':
      return CoffeeGen()
    raise Exception('unkdown generator name "%s"' % name)

  def createFormatter(self, name):
    if name == 'py':
      return PyFormatter()
    if name == 'coffee':
      return CoffeeFormatter()
    raise Exception('unkdown formatter name "%s"' % name)
