

def getTokensRange(leftIndex, rightIndex, tokens):
  return enumerate(tokens[leftIndex:rightIndex+1], leftIndex)


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
    self.name = name
    self.sources = sources

    self.modules = {}
    self.aliasModules = {}
    self.variables = {}
    self.functions = {}
    self.enums = {}
    self.structs = {}
    self.classes = {}
