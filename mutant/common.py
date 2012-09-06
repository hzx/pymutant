

class Source(object):
  """
  Source - represent source file,
  skiplines - line numbers with import and comments skip for parsing.
  """

  def __init__(self, filename, lines, skiplines):
    self.filename = filename
    self.lines = lines
    self.skiplines = skiplines

class Token(object):
  """
  Language word.
  """

  def __init__(self, source, linenum, word, wordtype = None):
    self.source = source
    self.linenum = linenum
    self.word = word
    self.wordtype = wordtype
    
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

"""
For store parsed results.
"""

class EnumTypes(object):
  """
  Enum types table.
  """

  def __init__(self):
    pass

class StructTypes(object):
  """
  Struct types table.
  """

  def __init__(self):
    pass

class ClassTypes(object):
  """
  Class types table.
  """

  def __init__(self):
    pass

