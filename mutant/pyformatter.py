

class PyFormatter(object):

  def __init__(self):
    self.indent = 0
    # cache formatted modules code
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

    self.functionNames = {
        'is': '==',
        'isnot': '!='
      }

  def generate(self, module):
    """
    Generate module code and all imported.
    """
    return self.genModule(module)

  def incIndent(self):
    self.indent = self.indent + 2

  def decIndent(self):
    self.indent = self.indent - 2

  def getIndent(self):
    return ''.rjust(self.indent, ' ')

  def genModule(self, module):
    """
    Generate module code and all imported modules.
    """
    if self.cache.has_key(module.name):
      return self.cache[module.name]

    self.module = module

    code = ''

    raise Exception('not implemented')

    # generate classes
    classesCode = self.processClasses(module)

    # generate functions
    functionsCode = self.processFunctions(module)

    # generate variables
    variablesCode = self.processVariables(module)

    # gen imported modules
    modules = []
    for name, mod in module.modules.items():
      if mod == None: continue
      modules.append(self.genModule(mod))

    # add modules code before to beginning
    code = ''.join(modules) + classesCode + functionsCode + variablesCode

    return code

  def processClasses(self, module):
    buf = []
    for name, cl in module.classes.items():
      code = self.genClass(cl)
      buf.append(code)
    return ''.join(buf)

  def processFunctions(self, module):
    buf = []
    for name, fn in module.functions.items():
      code = self.genFunction(fn, None)
      buf.append(code)
    return ''.join(buf)

  def processVariables(self, module):
    buf = []
    for name, va in module.variables.items():
      code = self.genVariable(va)
      buf.append(code)
    return ''.join(buf)

  def genClass(self, cl):
    self.incIndent()

    # variables
    vabuf = []
    for vname, va in cl.variables.items():
      code = self.genVariable(va)
      vabuf.append(code)

    # functions
    fnbuf = []
    for fname, fn in cl.functions.items():
      code = self.genFunction(fn)
      fnbuf.append(code)

    self.decIndent()

    return ''.join(vabuf) + ''.join(fnbuf)

  def genFunction(self, fn, cl):
    raise Exception('not implemented')
    
    params = []
    if cl: params.append('self')
    for name, decltype in fn.params:
      params.append(name)
    decl = '%sdef %s(%s):\n' % (self.getIndent(), fn.name, ', '.join(params))

    body = self.genFunctionBody(fn.bodyNodes)

    return decl + body

  def genFunctionBody(self, nodes):
    self.incIndent()

    buf = []
    for node in nodes:
      gen = self.nodetypeToGen(node.nodetype)
      buf.append(gen(node))

    self.decIndent()

    return ''.join(buf)

  def genVariable(self, va):
    buf = [self.getIndent(), va.name, self.genVarBody(va.body), '\n']
    return ''.join(buf)

  def genValue(self, va):
    return 'None' if va.value == 'none' else va.value

  def genVarBody(self, body):
    gen = self.nodetypeToGen(body.nodetype)
    return gen(body)

  def genIf(self, ifn):
    buf = [self.getIndent(), 'if ', self.genExpr(ifn.expr), ':\n', self.genFunctionBody(ifn.body)]
    if ifn.elseBody: buf = buf + ['else:\n', self.genFunctionBody(ifn.elseBody)]
    return ''.join(buf)

  def genFor(self, forn):
    buf = [self.getIndent(), 'for ', forn.itemName, ' in ', forn.collName, ':\n', self.genFunctionBody(forn.body)]
    return ''.join(buf)

  def genArrayBody(self, ab):
    buf = [self.genExpr(item) for item in ab.items]
    return '[%s]' % ', '.join(buf)

  def genArrayValue(self, av):
    return '%s[%s]' % (av.value, str(av.index))

  def genDictBody(self, node):
    buf = []
    for name, item in node.items.items():
      buf.append('%s: %s' % (name, self.genExpr(item)))
    return '{%s}' % ', '.join(buf)

  def genReturn(self, ret):
    buf = [self.getIndent(), 'return ', self.genVarBody(ret.body)]
    return ''.join(buf)

  def genFunctionCall(self, fc):
    if fc.name in grammar.unaryFunctions:
      return '(%s %s)' % (fc.name, self.genExpr(fc.params[0]))

    if fc.name in grammar.binaryFunctions:
      fname = self.functionNames.get(fc.name, None) or fc.name
      return '(%s %s %s)' % (self.genExpr(fc.params[0]), fname, self.genExpr(fc.params[1]))

    # functioncall
    prefix = 'new ' if ic.isConstructorCall else ''
    params = []
    for param in fc.params:
      params.append(self.genExpr(param))
    return '%s%s(%s)' % (prefix, fc.name, ', '.join(params))

  def genExpr(self, node):
    gen = self.nodetypeToGen(node.nodetype)
    return gen(node)

