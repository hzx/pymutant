from abc import abstractmethod


"""
Create vars, enum, struct, class table.
Program tree.
"""

class BaseParser(object):
  """
  Common parser interface.
  """

  @abstractmethod
  def parse(self, tokens):
    """Return parsed code tree."""
    pass

class VariableParser(BaseParser):

  def __init__(self):
    pass

  def parse(self, tokens):
    pass

class EnumParser(BaseParser):

  def __init__(self):
    pass

  def parse(self, tokens):
    pass


class ClassParser(BaseParser):

  def __init__(self):
    pass

  def parse(self, tokens):
    pass

class Parser(BaseParser):

  def __init__(self):
    self.vars = []
    self.enums = []
    self.structs = []
    self.classes = []

  def parse(self, tokens):
    pass
