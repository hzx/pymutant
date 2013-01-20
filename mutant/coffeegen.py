from mutant import core
from mutant import common


class CoffeeGen(object):

  def __init__(self):
    # cache generated modules
    self.cache = {}

  def generate(self, module):
    self.generateModule(module)

  def generateModule(self, module):
    # add to cache
    if self.cache.has_key(module.name):
      return
    self.cache[module.name] = module

    # move all class variables in constructor
    for cn, cl in module.classes.items():
      self.moveVariablesToConstructor(cl)
      # for vn, va in cl.variables.items():
        

    # convert all enums to variables
    for name, en in module.enums.items():
      va = core.VariableNode([common.Token(0, 'var', 'var')], en.name)

      body = core.DictBodyNode()
      for key, val in en.members.items():
        body.addItem(key, core.ValueNode(val))

      va.body = body
      module.variables[va.name] = va

    # self.addNamespaces(module)

    # add imported modules
    for name, mod in module.modules.items():
      va = core.VariableNode([common.Token(0, 'var', 'var')], name)
      va.body = core.ValueNode('window.' + mod.name)
      module.variables[va.name] = va

    # generate imported modules
    for name, mod in module.modules.items():
      self.generateModule(mod)

  def moveVariablesToConstructor(self, cl):
    # search function with name None
    found = None

    if cl.constructor == None:
      cl.constructor = core.FunctionNode(None, None)

    con = cl.constructor

    # move variables to constructor
    for vn, va in cl.variables.items():
      val = core.ValueNode('this.' + va.name)
      val.body = va.body
      con.addBodyNode(val)

    # remove class variables
    cl.variables = {}

    return found

  def addNamespaces(self, module):
    # add namespaces for variables
    nsvars = []
    for name, va in module.variables.items():
      nsva = core.VariableNode([common.Token(0, 'var', 'var')], module.name + '.' + va.name)
      nsva.body = core.ValueNode(va.name)
      nsvars.append(nsva)

    # add namespaces for functions
    for name, fn in module.functions.items():
      nsva = core.VariableNode([common.Token(0, 'var', 'var')], module.name + '.' + fn.name)
      nsva.body = core.ValueNode(fn.name)
      nsvars.append(nsva)

    # add namespaces for classes
    for name, cl in module.classes.items():
      nsva = core.VariableNode([common.Token(0, 'var', 'var')], module.name + '.' + cl.name)
      nsva.body = core.ValueNode(cl.name)
      nsvars.append(nsva)

    # add all namespaced
    for nsva in nsvars:
      module.variables[nsva.name] = nsva

