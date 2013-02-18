from mutant import core
from mutant import common
from mutant import grammar


class CoffeeFormatter(object):

  def __init__(self):
    self.indent = 0
    # cache formatted modules code
    self.cache = {}

  def format(self, nodes):
    pass

  def generate(self, module):
    """
    Generate module code, and all imported.
    """
    return self.genModule(module)

  def genModule(self, module):
    if self.cache.has_key(module.name):
      return self.cache[module.name]
  
    code = ''

    # add global namespace
    code = '%s = {}\nwindow.%s = %s\n' % (module.name, module.name, module.name)
    # ns = core.VariableNode([common.Token(0, 'var', 'var')], 'window.' + module.name)
    # ns.body = core.DictBodyNode()
    # code = self.genVariableCode(ns, isGlobal=True)

    # variables
    for name, va in module.variables.items():
      res = self.genVariableCode(va, isGlobal=True)
      code = code + res + '\n'

    # functions
    for name, fn in module.functions.items():
      # skip main function, write last
      if name == 'main': continue
      res = self.genFunctionCode(fn, isGlobal=True)
      code = code + res + '\n'
    # write main function
    if 'main' in module.functions:
      code = code + self.genFunctionCode(module.functions['main'], isGlobal=True)

    # TODO(dem) make more smart sort - if class use another class - move to top

    sortedClasses = self.sortClasses(module)

    # classes
    for cl in sortedClasses:
      res = self.genClassCode(cl)
      code = code + res + '\n'

    # add module code to cache
    self.cache[module.name] = code

    # gen imported modules
    modcodes = []
    for name, mod in module.modules.items():
      modcode = self.genModule(mod)
      modcodes.append(modcode)
    # add module code before, add namespaces to end
    code = ''.join(modcodes) + code + self.genNamespaces(module)

    return code

  def sortClasses(self, module):
    # super classes move to top
    superClassNames = []
    for name, cl in module.classes.items():
      if cl.baseName in module.classes:
        superClassNames.append(cl.baseName)
    superClasses = []
    otherClasses = []
    for name, cl in module.classes.items():
      if cl.name in superClassNames:
        superClasses.append(cl)
      else:
        otherClasses.append(cl)

    buf = [cl for name, cl in module.classes.items()]
    out = []

    while (len(buf) > 0):
      # searcch super classes name
      superClassNames = []
      for cl in buf:
        if cl.baseName in module.classes:
          superClassNames.append(cl.baseName)
      # divide super classes and other classes
      superClasses = []
      otherClasses = []
      for cl in buf:
        if cl.name in superClassNames:
          superClasses.append(cl)
        else:
          otherClasses.append(cl)
      # flush otherClasses to out buffer
      out = otherClasses + out
      # switch buf to superClasses
      buf = superClasses

    return out


  def genNamespaces(self, module):
    code = ''
    items = []
    # add namespaces for variables
    for name, va in module.variables.items():
      items.append('%s.%s = %s' % (module.name, va.name, va.name))
    
    # add namspaces for functions
    for name, fn in module.functions.items():
      items.append('%s.%s = %s' % (module.name, fn.name, fn.name))

    # add namespaces for classes
    for name, cl in module.classes.items():
      items.append('%s.%s = %s' % (module.name, cl.name, cl.name))

    code = '\n'.join(items) + '\n'

    return code

  def incIndent(self):
    self.indent = self.indent + 2

  def decIndent(self):
    self.indent = self.indent - 2

  def getIndent(self):
    return ''.rjust(self.indent, ' ')

  def genVarBodyCode(self, node):
    code = ''

    if node.nodetype == 'value':
      if node.value == 'none':
        code = 'null'
      else:
        code = node.value
    # todo(dem) rework with genexpr
    elif node.nodetype == 'functioncall':
      # create params code
      par = ''
      notFirst = False
      for param in node.params:
        if notFirst: par = par + ', '
        par = par + self.genVarBodyCode(param)
        notFirst = True
      code = '%s(%s)' % (node.name, par)
      if node.isConstructorCall:
        code = 'new ' + code
    elif node.nodetype == 'array_body':
      itcode = ''
      notFirst = False
      for item in node.items:
        if notFirst: itcode = itcode + ', '
        itcode = itcode + self.genVarBodyCode(item)
        notFirst = True
      code = '[%s]' % (itcode)
    elif node.nodetype == 'dict_body':
      bcode = ''
      notFirst = False
      for name, item in node.items.items():
        if notFirst: bcode = bcode + ', '
        bcode = bcode + name + ': ' + self.genVarBodyCode(item)
        notFirst = True
      code = '{%s}' % (bcode)

    return code

  def genVariableCode(self, va, isGlobal):
    code = self.getIndent() + va.name
    if va.body:
      bodycode = self.genVarBodyCode(va.body)
      if isGlobal:
        code = code + ' = ' + bodycode + '\n'
      else:
        code = code + ': ' + bodycode + '\n'

    return code

  def genFunctionCode(self, fn, isGlobal):
    code = self.getIndent()
    paramcode = ''
    notFirst = False
    for name, param in fn.params:
      if notFirst: paramcode = paramcode + ', '
      paramcode = paramcode + name
      notFirst = True

    if fn.name:
      code = code + fn.name
    else:
      code = code + 'constructor'

    arrow = '=>'
    if isGlobal or fn.name == None: arrow = '->'
    params = '(%s) %s\n' % (paramcode, arrow)
    if isGlobal:
      code = code + ' = ' + params
    else:
      code = code + ': ' + params
      
    # increment for body
    # if not isGlobal:
    self.incIndent()

    code = code + self.genFunctionBodyCode(fn.bodyNodes)

    # if not isGlobal:
    self.decIndent()
    
    return code

  def genFunctionBodyCode(self, nodes):
    code = ''

    for node in nodes:
      if node.nodetype == 'value':
        code = code + self.getIndent() + self.genValueCode(node) + '\n'
      elif node.nodetype == 'variable':
        code = code + self.genVariableCode(node, isGlobal=True) + '\n'
      elif node.nodetype == 'functioncall':
        code = code + self.getIndent() + self.genFunctionCallCode(node) + '\n'
      elif node.nodetype == 'return':
        code = code + self.getIndent() + 'return ' + self.genExprCode(node.body) + '\n'
      elif node.nodetype == 'if':
        code = code + self.genIfCode(node) + '\n'
      elif node.nodetype == 'for':
        code = code + self.genForCode(node) + '\n'

    return code

  def genClassCode(self, cl):
    code = 'class %s' % cl.name
    if cl.baseName:
      code = code + ' extends %s' % cl.baseName
    code = code + '\n'

    # add indent for members
    self.incIndent()

    # constructor

    if cl.constructor:
      const = self.genFunctionCode(cl.constructor, isGlobal=False)
      code = code + const
  
    # variables
    for name, va in cl.variables.items():
      code = code + self.genVariableCode(va, isGlobal=False)

    # functions
    for name, fn in cl.functions.items():
      code = code + self.genFunctionCode(fn, isGlobal=False)

    self.decIndent()

    return code

  def genValueCode(self, va):
    code = va.value + ' = ' + self.genVarBodyCode(va.body)
    return code

  def genFunctionCallCode(self, fc):
    # todo(dem) check func type (*, name, +, -, is, not)

    # if unary function
    if fc.name in grammar.unaryFunctions:
      return '(%s %s)' % (fc.name, self.genExprCode(fc.params[0]))

    # if bynary function
    if fc.name in grammar.binaryFunctions:
      fname = fc.name
      if fname == 'isnot': fname = 'isnt'
      return '(%s %s %s)' % (self.genExprCode(fc.params[0]), fname, self.genExprCode(fc.params[1]))

    # function call
    # create params code
    par = ''
    prefix = ''
    if fc.isConstructorCall: prefix = 'new '
    notFirst = False
    for param in fc.params:
      if notFirst: par = par + ', '
      par = par + self.genExprCode(param)
      notFirst = True
    return '%s%s(%s)' % (prefix, fc.name, par)

  def genArrayBodyCode(self, ab):
    itcode = ''
    notFirst = False
    for item in ab.items:
      if notFirst: itcode = itcode + ', '
      itcode = itcode + self.genExprCode(item)
      notFirst = True
    return '[%s]' % (itcode)

  def genDictBodyCode(self, db):
      bcode = ''
      notFirst = False
      for name, item in db.items.items():
        if notFirst: bcode = bcode + ', '
        bcode = bcode + name + ': ' + self.genExprCode(item)
        notFirst = True
      return '{%s}' % (bcode)


  def genExprCode(self, node):
    code = ''

    # debug
    if not hasattr(node, 'nodetype'):
      print "ERROR: "
      print node

    if node.nodetype == 'value':
      if node.value == 'none':
        code = 'null'
      else:
        code = node.value
    elif node.nodetype == 'functioncall':
      code = self.genFunctionCallCode(node)
    elif node.nodetype == 'array_body':
      code = self.genArrayBodyCode(node)
    elif node.nodetype == 'dict_body':
      code = self.genDictBodyCode(node)

    return code

  def genIfCode(self, ifn):
    code = self.getIndent() + 'if ' + self.genExprCode(ifn.expr) + '\n'

    self.incIndent()

    # body
    code = code + self.genFunctionBodyCode(ifn.body)

    self.decIndent()

    # else body
    if ifn.elseBody:
      code = code + self.getIndent() + 'else\n'

      self.incIndent()

      code = code + self.genFunctionBodyCode(ifn.elseBody)

      self.decIndent()

    return code

  def genForCode(self, forn):
    code =  '%sfor %s in %s\n' % (self.getIndent(), forn.itemName, forn.collName)

    self.incIndent()

    code = code + self.genFunctionBodyCode(forn.body)

    self.decIndent()

    return code
