from mutant import core
from mutant import common


class CoffeeGen(object):

  def __init__(self):
    # cache generated modules
    self.cache = {}

    # self.nodetypeToGen = {
    #     'value': self.genValue,
    #     'variable': self.genVariable,
    #     'if': self.genIf,
    #     'for': self.genFor,
    #     'array_body': self.genArrayBody,
    #     'array_value': self.genArrayValue,
    #     'dict_body': self.genDictBody,
    #     'return': self.genReturn,
    #     'functioncall': self.genFunctionCall,
    #   }

  def generate(self, module):
    self.generateModule(module)

  def generateModule(self, module):
    # add to cache
    if module.name in self.cache:
      return
    self.cache[module.name] = module

    self.module = module

    # NEW
    """

    # process classes
    self.processClasses(module)

    # process functions
    self.processFunctions(module)

    # process variables
    self.processVariables(module)

    # process enums
    self.processEnums(module)

    # process imported modules
    for name, mod in module.modules.items():
      if mod: self.generateModule(mod)

    """
    # NEW END

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

    # MOVED TO FORMATTER
    # add imported modules to window
    # for name, mod in module.modules.items():
    #   va = core.VariableNode([common.Token(0, 'var', 'var')], name)
    #   va.body = core.ValueNode('window.' + mod.name)
    #   module.variables[va.name] = va

    # generate imported modules
    for name, mod in module.modules.items():
      # extern module have name and mod == None, skip it
      if mod == None: continue
      self.generateModule(mod)

  # NEW
  """

  def processClasses(self, module):
    pass

  def processFunctions(self, module):
    pass

  def processVariables(self, module):
    pass

  def processEnums(self, module):
    pass

  # generators

  def genValue(self, val, cl=None):
    pass

  def genVariable(self, va, cl=None):
    pass

  def genIf(self, ifn):
    pass

  def genFor(self, forn, cl=None):
    pass

  def genArrayBody(self, ab, cl=None):
    pass

  def genArrayValue(self, av, cl=None):
    pass

  def genDictBody(self, db, cl=None):
    pass

  def genReturn(self, ret, cl=None):
    pass

  def genFunctionCall(self, fc, cl=None):
    pass

  # custom generators

  def genClass(self, cl):
    pass

  def genFunctionBody(self, nodes, cl=None):
    return [self.genByNodetype(node, cl) for node in nodes]

  def genByNodetype(self, node, cl=None):
    gen = self.nodetypeToGen(node.nodetype)
    return gen(node, cl)

  # process names

  def processValueFuncName(self, name):
    #Replace enum.name by enum_name.
    parts = self.dotre.split(name)
    count = len(parts)
    first = parts[0]

    if first == 'this':
      return name

    if count > 1:
      buf = []
      # search module name first
      if first in self.module.modules: 
        module = self.module.modules[first]
        # append module name to buf
        buf.append(first)
        # found enum name
        if parts[1] in module.enums:
          buf.append('%s_%s' % (parts[1], parts[2]))
        return '.'.join(buf)
      else:
        if first in self.module.enums:
          return '%s_%s' % (first, parts[1])

    return name

  def processSupercallName(self, name, cl):
    parts = self.dotre.split(fc.name)
    count = len(parts)
    first = parts[0]

    # TODO(dem) need convert super.enterDocument to coffee equivalent
    # if first == 'super':
    #   if count == 1:
    #     return '%s.__init__' % cl.baseName
    #   parts[0] = cl.baseName
    #   return '.'.join(parts)

    return name
  """

  # NEW END


  def moveVariablesToConstructor(self, cl):
    # search function with name None
    found = None

    if cl.constructor == None:
      cl.constructor = core.FunctionNode(None, None)

    con = cl.constructor

    # move variables to constructor in the beginning
    for vn, va in cl.variables.items():
      val = core.ValueNode('this.' + va.name)
      val.body = va.body
      pos = 0
      if len(con.bodyNodes) >= 1:
        first = con.bodyNodes[0]
        if first.nodetype == 'functioncall' and first.name == 'super':
          pos = 1
      con.bodyNodes.insert(1, val)

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

