from abc import abstractmethod


class Node(object):
  """Base class for all nodes."""

  def __init__(self):
    pass

  @abstractmethod
  def convertNode(self, gen): pass

class VarNode(Node):

  def __init__(self, name):
    self.name = name

  def convertNode(self, gen):
    return gen.createVar(self)

class EnumNode(Node):

  def __init__(self, name):
    self.name = name

  def convertNode(self, gen):
    return gen.createEnum(self)

class StructNode(Node):

  def __init__(self, name):
    self.name = name

  def convertNode(self, gen):
    return gen.createStruct(self)

class ClassNode(Node):

  def __init__(self, name):
    self.name = name

  def convertNode(self, gen):
    return gen.createClass(self)

class SelectFromNode(Node):

  def __init__(self, name):
    self.name = name

  def convertNode(self, gen):
    return gen.createSelectFrom(self)

class SelectConcatNode(Node):

  def __init__(self, names):
    self.names = names

  def convertNode(self, gen):
    return gen.createSelectConcat(self)

class TagNode(Node):

  def __init__(self, name):
    self.name = name

  def convertNode(self, gen):
    return gen.createTag(self)

class Gen(object):
  """Base class for all generators."""

  def __init__(self):
    pass

  @abstractmethod
  def createVar(self, node): pass

  @abstractmethod
  def createFunction(self, node): pass

  @abstractmethod
  def createEnum(self, node): pass

  @abstractmethod
  def createStruct(self, node): pass

  @abstractmethod
  def createClass(self, node): pass

  @abstractmethod
  def createSelectFrom(self, node): pass

  @abstractmethod
  def createSelectConcat(self, node): pass

  @abstractmethod
  def createTag(self, node): pass
