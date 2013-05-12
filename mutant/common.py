import re
from mutant import grammar


def getTokensRange(leftIndex, rightIndex, tokens):
  return enumerate(tokens[leftIndex:rightIndex+1], leftIndex)

def searchFunctionParamType(name, func):
  for paramName, paramType in func.params:
    if paramName == name:
      return paramType
  return None


dotre = re.compile('\.')

def isClassName(module, name):
  """
  Find name among struct and class names, and aliased modules
  """
  # search in classes
  if name in module.classes or name in module.structs:
    return True
  # check if name consistent
  res = dotre.split(name)
  if len(res) > 1:
    moduleName = res[0]
    className = res[1]
    # search in modules
    if moduleName in module.modules:
      mod = module.modules[moduleName]
      # search in module classes
      if className in mod.classes or className in mod.structs:
        return True
  return False


def isStructName(module, name):
  if name in ['robject']:
    return True
  # search in structs
  if name in module.structs:
    return True
  # check if name consistent
  res = dotre.split(name)
  if len(res) > 1:
    moduleName = res[0]
    structName = res[1]
    # search in modules
    if moduleName in module.modules:
      mod = module.modules[moduleName]
      # search in module structs
      if structName in mod.structs:
        return True
  return False

def getStruct(module, name):
  if name in module.structs:
    return True
  res = dotre.split(name)
  if len(res) > 1:
    moduleName = res[0]
    structName = res[1]
    if moduleName in module.modules:
      mod = module.modules[moduleName]
      if structName in mod.structs:
        st = mod.structs[structName]
        return st
  return None


def isStructValueName(module, name):
  """
  Search first name and check it must be world
  """
  parts = dore.split(name)
  if len(parts) == 1:
    return False

  moduleName = res[0]
  if moduleName != 'world':
    return False


def getOnlyName(name):
  res = dotre.split(name)
  return res[len(res) - 1]


class Token(object):
  """
  Language word.
  """

  def __init__(self, linenum, word, wordtype = None):
    self.linenum = linenum
    self.word = word
    self.wordtype = wordtype
    
class Source(object):
  """
  Source - represent source file,
  skiplines - line numbers with import and comments skip for parsing.
  """

  def __init__(self, filename, lines, skiplines, tokens = None):
    self.filename = filename
    self.lines = lines
    self.skiplines = skiplines
    self.tokens = tokens

class Module(object):

  def __init__(self, name, sources):
    self.path = ''
    self.name = name
    self.sources = sources

    self.rawimports = []
    # module name and alias
    self.imports = []
    self.modules = {}
    # self.aliasModules = {}
    self.variables = {}
    self.variables_order = []
    self.functions = {}
    self.functions_order = []
    self.enums = {}
    self.structs = {}
    self.classes = {}
    self.classes_order = []

  def addVariable(self, node):
    self.checkName(node.name)
    self.variables[node.name] = node

  def addFunction(self, node):
    self.checkName(node.name)
    self.functions[node.name] = node

  def addEnum(self, node):
    self.checkName(node.name)
    self.enums[node.name] = node

  def addStruct(self, node):
    self.checkName(node.name)
    self.structs[node.name] = node

  def addClass(self, node):
    self.checkName(node.name)
    self.classes[node.name] = node

  def checkName(self, name):
    if name in self.variables:
      raise Exception('module "%s" already have variable "%s"' % (self.name, name))
    if name in self.functions:
      raise Exception('module "%s" already have function "%s"' % (self.name, name))
    if name in self.enums:
      raise Exception('module "%s" already have enum "%s"' % (self.name, name))
    if name in self.structs:
      raise Exception('module "%s" already have struct "%s"' % (self.name, name))
    if name in self.classes:
      raise Exception('module "%s" already have class "%s"' % (self.name, name))

