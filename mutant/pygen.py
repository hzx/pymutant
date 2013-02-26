from mutant import core
from mutant import common
import re


class PyGen(object):

  def __init__(self):
    # cache generated modules
    self.cache = {}

    self.nodetypeToGen = {
        'value': self.genValue,
        'variable': self.genVariable,
        'if': self.genIf,
        'for': self.genFor,
        'array_body': self.genArrayBody,
        'array_value': self.genArrayValue,
        'dict_body': self.genDictBody,
        'return': self.genReturn,
        'functioncall': self.genFunctionCall,
      }

    self.dotre = re.compile('\.')

  def generate(self, module):
    self.generateModule(module)

  def generateModule(self, module):
    # add to cache
    if self.cache.has_key(module.name):
      return
    self.cache[module.name] = module

    self.module = module

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

  def processEnums(self, module):
    """
    Convert enums to variables with name_valuename.
    Replace all enum right value from name.valuename to name_valuename
    """
    # create variables from enums
    for ename, en in module.enums.items():
      for name, value in en.members.items():
        va = core.VariableNode(
          [common.Token(0, 'int', 'int')],
          '%s_%s' % (en.name, name)
          )
        va.body = core.ValueNode(value)
        module.addVariable(va)

  def processVariables(self, module):
    """
    Make generations in variables.
    """
    for vname, va in module.variables.items():
      module.variables[va.name] = self.genVariable(va)

  def processFunctions(self, module):
    """
    Make generations in functions.
    """
    for fname, fn in module.functions.items():
      module.functions[fn.name] = self.genFunction(fn)

  def processClasses(self, module):
    """
    Make generations in classes.
    Convert constructor - anonymous function to __init__
    """
    for cname, cl in module.classes.items():
      module.classes[cl.name] = self.genClass(cl)

  def genVariable(self, va, cl=None):
    """
    Change variable or create new.
    return variable.
    """
    if va.body:
      va.body = self.genByNodetype(va.body, cl)
    return va

  def genFunction(self, fn, cl=None):
    """
    Change function or create new and return it.
    For class methods add first self param.
    Convert super call to python method.
    Replace this by self in body nodes.
    return function.
    """
    if cl:
      # add self to params
      fn.insert(['self', [common.Token(0, cl.name, grammar.NAME_TYPE)]])

    fn.bodyNodes = self.genFunctionBody(fn.bodyNodes, cl)

    return fn

  def genConstructor(self, fn, cl):
    """
    Give it name __init__.
    """
    fn.name = '__init__'
    return self.genFunction(fn, cl)

  def genClass(self, cl):
    """
    Change class or create new and return it.
    Process members.
    return class.
    """
    # gen variables
    for vname, va in cl.variables.items():
      cl.variables[vname] = self.genVariable(va, cl)
    # gen functions
    for fname, fn in cl.functions.items():
      cl.functions[fname] = self.genFunction(fn, cl)
    # gen constructor
    if cl.constructor:
      cl.constructor = self.genConstructor(cl.constructor, cl)
    return cl

  def genIf(self, ifn, cl=None):
    ifn.expr = self.genByNodetype(ifn.expr, cl)
    ifn.body = self.genByNodetype(ifn.body, cl)
    ifn.elseBody = self.genByNodeType(ifn.elseBody, cl)

    return ifn

  def genFor(self, forn, cl=None):
    forn.collName = self.processValueFuncName(forn.collName)
    forn.body = self.genFunctionBody(forn.body, cl)

    return forn

  def genValue(self, va, cl=None):
    """
    Replace in the value this by self and enum.value to enum_value.
    """
    va.value = self.processValueFuncName(va.value)
    if va.body: va.body = self.genByNodetype(va.body, cl)

    return va

  def genArrayBody(self, ab, cl=None):
    ab.items = [self.genByNodetype(item, cl) for item in ab.items]

    return ab

  def genArrayValue(self, av, cl=None):
    av.value = self.processValueFuncName(av.value, cl)
    return av

  def genDictBody(self, db, cl=None):
    for name, expr in db.items.items():
      db.items[name] = self.genByNodetype(expr, cl)
    return db

  def genReturn(self, ret, cl=None):
    ret.body = self.genByNodetype(ret.body, cl)
    return ret

  def genFunctionCall(self, fc, cl=None):
    raise Exception('not implemented')
    # convert supercall
    if cl:
      fc.name = self.processSupercallName(fc.name, cl)
  
    fc.name = self.processValueFuncName(fc.name, cl)

    # convert params
    fc.params = [self.genByNodetype(param) for param in fc.params]

    return fc

  def genFunctionBody(self, nodes, cl=None):
    buf = []
    for node in nodes:
      buf.append(genByNodetype(node, cl))
    return buf

  def genByNodetype(self, node, cl=None):
    gen = self.nodetypeToGen(node.nodetype)
    return gen(node, cl)
    
  def processValueFuncName(self, name):
    """
    Replace this by self.
    Replace enum.name by enum_name.
    """
    parts = self.dotre.split(name)
    count = len(parts)
    first = parts[0]

    if first == 'this':
      parts[0] = 'self'
      return '.'.join(parts)

    if count > 1:
      buf = []
      # search module name first
      if self.module.modules.has_key(first): 
        module = self.module.modules[first]
        # append module name to buf
        buf.append(first)
        # found enum name
        if module.enums.has_key(parts[1]):
          buf.append('%s_%s' % (parts[1], parts[2]))
        return '.'.join(buf)
      else:
        if self.module.enums.has_key(first):
          return '%s_%s' % (first, parts[1])

    return name

  def processSupercallName(self, name, cl):
    parts = self.dotre.split(fc.name)
    count = len(parts)
    first = parts[0]
    if first == 'super':
      if count == 1:
        return '%s.__init__' % cl.baseName
      parts[0] = cl.baseName
      return '.'.join(parts)

    return name
