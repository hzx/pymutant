import re
from mutant import grammar


def getTokensRange(leftIndex, rightIndex, tokens):
  return enumerate(tokens[leftIndex:rightIndex+1], leftIndex)


dotre = re.compile('\.')

def isClassName(module, name):
  """
  Find name among struct and class names, and aliased modules
  """
  # search in classes
  if module.classes.has_key(name) or module.structs.has_key(name):
    return True
  # check if name consistent
  res = dotre.split(name)
  if len(res) > 1:
    moduleName = res[0]
    className = res[1]
    # search in modules
    if module.modules.has_key(moduleName):
      mod = module.modules[moduleName]
      # search in module classes
      if mod.classes.has_key(className) or mod.structs.has_key(className):
        return True
  return False


def isStructName(module, name):
  # search in structs
  if module.structs.has_key(name):
    return True
  # check if name consistent
  res = dotre.split(name)
  if len(res) > 1:
    moduleName = res[0]
    structName = res[1]
    # search in modules
    if module.modules.has_key(moduleName):
      mod = module.modules[moduleName]
      # search in module structs
      if mod.structs.has_key(structName):
        return True
  return False


def isStructValueName(module, name):
  """
  Search first name and check it must be world
  """
  res = dore.split(name)
  if len(res) == 1:
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

    self.modules = {}
    # self.aliasModules = {}
    self.variables = {}
    self.functions = {}
    self.enums = {}
    self.structs = {}
    self.classes = {}


