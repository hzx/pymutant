

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
    self.variables = {}
    self.functions = {}
    self.enums = {}
    self.structs = {}
    self.classes = {}

"""
Language semantic elements.
"""

class Variable(object):

  def __init__(self, identifier, value=None):
    self.identifier = identifier
    self.value = value

class Function(object):

  def __init__(self):
    pass

  def addParameter(self, param):
    pass

class Enum(object):

  def __init__(self):
    pass

  def addMember(self):
    pass

class Struct(object):

  def __init__(self):
    pass

class Class(object):

  def __init__(self):
    self.members = {}
    self.methods = {}

  def addMember(self):
    pass

  def addMethod(self):
    pass

class SelectFrom(object):

  def __init__(self):
    pass

class SelectConcat(object):

  def __init__(self):
    pass
