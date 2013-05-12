from mutant import core
from mutant import common


class CoffeeGen(object):

  def __init__(self):
    # cache generated modules
    self.cache = {}

    self.nodetypeToGen = {
        'value': self.genValue,
        'variable': self.genVariable,
        'if': self.genIf,
        'for': self.genFor,
        'while': self.genWhile,
        'array_body': self.genArrayBody,
        'array_value': self.genArrayValue,
        'dict_body': self.genDictBody,
        'dict_value': self.genDictValue,
        'return': self.genReturn,
        'functioncall': self.genFunctionCall,
      }

  def generate(self, module):
    self.generateModule(module)

  def generateModule(self, module):
    # add to cache
    if module.name in self.cache:
      return
    self.cache[module.name] = module

    self.module = module

    # process classes
    self.processClasses(module)
        
    # process enums
    self.processEnums(module)

    # process functions
    self.processFunctions(module)

    # process variables
    self.processVariables(module)

    # self.addNamespaces(module)

    # MOVED TO FORMATTER
    # add imported modules to window
    # for name, mod in module.modules.items():
    #   va = core.VariableNode([common.Token(0, 'var', 'var')], name)
    #   va.body = core.ValueNode('window.' + mod.name)
    #   module.variables[va.name] = va

    # process imported modules
    for name, mod in module.modules.items():
      # extern module have name and mod == None, skip it
      if mod == None: continue
      self.generateModule(mod)

  def processClasses(self, module):
    # move all class variables in constructor
    for cn, cl in module.classes.items():
      self.moveVariablesToConstructor(cl)
      # for vn, va in cl.variables.items():

  def processFunctions(self, module):
    # module functions
    for fname, fn in module.functions.items():
      if len(fn.bodyNodes) == 0:
        print('len(fn.bodyNodes) == 0')
      fn.bodyNodes = self.genFunctionBody(fn.bodyNodes)

    # module classes functions
    for cn, cl in module.classes.items():
      for fname, fn in cl.functions.items():
        if len(fn.bodyNodes) == 0:
          print('len(fn.bodyNodes) == 0')
        fn.bodyNodes = self.genFunctionBody(fn.bodyNodes, cl)

  def processVariables(self, module):
    pass

  def processEnums(self, module):
    # convert all enums to variables
    for name, en in module.enums.items():
      va = core.VariableNode([common.Token(0, 'var', 'var')], en.name)

      body = core.DictBodyNode()
      for key, val in en.members.items():
        body.addItem(key, core.ValueNode(val))

      va.body = body
      module.variables[va.name] = va

  # generators

  def genValue(self, val, cl=None):
    return val

  def genVariable(self, va, cl=None):
    return va

  def genIf(self, ifn, cl=None):
    ifn.body = self.genFunctionBody(ifn.body, cl)
    ifn.elseBody = self.genFunctionBody(ifn.elseBody, cl)
    return ifn

  def genFor(self, forn, cl=None):
    forn.body = self.genFunctionBody(forn.body, cl)
    return forn

  def genWhile(self, wh, cl=None):
    wh.body = self.genFunctionBody(wh.body, cl)
    return wh

  def genArrayBody(self, ab, cl=None):
    return ab

  def genArrayValue(self, av, cl=None):
    return av

  def genDictBody(self, db, cl=None):
    return db

  def genDictValue(self, dv, cl=None):
    return dv

  def genReturn(self, ret, cl=None):
    return ret

  def genFunctionCall(self, fc, cl=None):
    return fc

  # custom generators

  def genClass(self, cl):
    pass

  def genFunctionBody(self, nodes, cl=None):
    # return [self.genByNodetype(node, cl) for node in nodes]
    buf = []
    # if len(nodes) == 0:
    #   print('genFunctionBody len(nodes) == 0')
    #   print(repr(nodes))
    for node in nodes:
      buf.append(self.genByNodetype(node, cl))
      # add constructor inits as values assign to buf
      if node.nodetype in ['variable', 'value'] and \
          node.body and node.body.nodetype == 'functioncall' and \
          len(node.body.inits) > 0:
        for name, expr in node.body.inits.items():
          val = core.ValueNode(node.name + '.' + name)
          val.body = expr
          buf.append(val)
    return buf

  def genByNodetype(self, node, cl=None):
    gen = self.nodetypeToGen.get(node.nodetype, None)
    if not gen:
      raise Exception('unknown nodetype "%s" in nodetypeToGen map' % node.nodetype)
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

  def processFunction(self, fn):
    for node in fn.bodyNodes:
      pass

  def expandConstructorCall(self, fc):
    if len(fc.inits) == 0:
      return

    # create constructor call
    # create properties init

