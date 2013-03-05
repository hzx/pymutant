import shutil
import os.path
import os
from mutant import grammar


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

  def generate(self, dest, prefix, module):
    """
    Generate module code and all imported.
    prefix - string, prefix to all imported modules if is mutant type.
    module - entry point module, app.
    """
    self.genModule(dest, prefix, module)

  def genModule(self, dest, prefix, module):
    """
    Generate module code and all imported modules.
    """
    if module.name in self.cache:
      return self.cache[module.name]

    self.module = module

    # generate classes
    classesCode = self.processClasses(module)

    # generate functions
    functionsCode = self.processFunctions(module)

    # generate variables
    variablesCode = self.processVariables(module)

    # generate imports
    importsCode = self.processImports(prefix, module)

    # add modules code before to beginning
    code = importsCode + '\n' + classesCode + functionsCode + variablesCode

    # generate imported modules
    self.processModules(dest, prefix, module)

    # save code
    self.saveModuleCode(dest, prefix, module.name, code)

  def incIndent(self):
    self.indent = self.indent + 2

  def decIndent(self):
    self.indent = self.indent - 2

  def getIndent(self):
    return ''.rjust(self.indent, ' ')

  def processImports(self, prefix, module):
    buf = []
    for name, mod in module.modules.items():
      if mod: buf.append('import %s.%s as %s\n' % (prefix, mod.name, name))
      else: buf.append('import %s\n' % name)
    return '\n'.join(module.rawimports) + '\n' + ''.join(buf)

  def processModules(self, dest, prefix, module):
    # gen imported modules
    for name, mod in module.modules.items():
      if mod:
        # skip model module
        if len(mod.structs) > 0: continue
        self.genModule(dest, prefix, mod)

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

    decl = 'class %s(%s):\n' % (cl.name, cl.baseName) if cl.baseName else 'class %s:\n' % cl.name

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

    return decl + ''.join(vabuf) + ''.join(fnbuf)

  def genFunction(self, fn, cl=None):
    params = []
    if cl: params.append('self')
    for name, decltype in fn.params:
      params.append(name)
    decl = '%s%s%sdef %s(%s):\n' % (self.getIndent(), fn.attributes, self.getIndent(), fn.name, ', '.join(params))

    body = self.genFunctionBody(fn.bodyNodes)

    return decl + body + '\n'

  def genFunctionBody(self, nodes):
    self.incIndent()

    buf = []
    for node in nodes:
      gen = self.nodetypeToGen[node.nodetype]
      buf.append(gen(node))

    self.decIndent()

    return ''.join(buf)

  def genVariable(self, va):
    buf = [self.getIndent(), va.name, ' = ', self.genVarBody(va.body), '\n\n']
    return ''.join(buf)

  def genValue(self, va):
    return 'None' if va.value == 'none' else va.value

  def genVarBody(self, body):
    gen = self.nodetypeToGen[body.nodetype]
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
    buf = [self.getIndent(), 'return ', self.genVarBody(ret.body), '\n']
    return ''.join(buf)

  def genFunctionCall(self, fc):
    if fc.name in grammar.unaryFunctions:
      return '(%s %s)' % (fc.name, self.genExpr(fc.params[0]))

    if fc.name in grammar.binaryFunctions:
      fname = self.functionNames.get(fc.name, None) or fc.name
      return '(%s %s %s)' % (self.genExpr(fc.params[0]), fname, self.genExpr(fc.params[1]))

    # functioncall
    prefix = 'new ' if fc.isConstructorCall else ''
    params = []
    for param in fc.params:
      params.append(self.genExpr(param))
    return '%s%s(%s)' % (prefix, fc.name, ', '.join(params))

  def genExpr(self, node):
    gen = self.nodetypeToGen[node.nodetype]
    return gen(node)

  def saveModuleCode(self, dest, prefix, name, code):
    nspath = os.path.join(dest, prefix)
    initname = os.path.join(nspath, '__init__.py')
    modfile = os.path.join(nspath, name + '.py')

    header = '# -*- coding: utf-8 -*-\n'
    code = header + code

    # create namespace dest+prefix path
    if not os.path.exists(nspath):
      os.mkdir(nspath)

    # create __init__.py file
    if not os.path.exists(initname):
      open(os.path.join(nspath, '__init__.py'), 'a').close()

    # write code to modfile
    with open(modfile, 'w') as f:
      f.write(code)

