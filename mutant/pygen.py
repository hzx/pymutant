

class PyGen(object):

  def __init__(self):
    # cache generated modules
    self.cache = {}

  def generate(self, module):
    self.generateModule(module)

  def createModuleStructure(self, dest, name):
    """
    Create in 'dest' path folder 'name' and __init__.py file.
    """
    pass

  def generateModule(self, module):
    # add to cache
    if self.cache.has_key(module.name):
      return
    self.cache[module.name] = module

    # process enums

    # process classes

    # process variables 

    # process functions
