from mutant import core
from mutant import common


class CoffeeGen(object):

  def __init__(self):
    pass

  def generate(self, module):
    self.generateModule(module)

  def generateModule(self, module):
    # convert all enums to variables
    for name, en in module.enums.items():
      va = core.VariableNode([common.Token(0, 'var', 'var')], en.name)

      body = core.DictBodyNode()
      for key, val in en.members.items():
        body.addItem(key, core.ValueNode(val))

      va.body = body
      module.variables[va.name] = va

    self.addNamespaces(module)

    # add imported modules
    for alias, mod in module.aliasModules.items():
      va = core.VariableNode([common.Token(0, 'var', 'var')], alias)
      va.body = core.ValueNode(mod.name)
      module.variables[va.name] = va

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

