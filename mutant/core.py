from mutant import grammar as gr
from abc import abstractmethod


class Node(object):
  """Base class for all nodes."""

  def __init__(self):
    pass

  # TODO(dem) deprecated
  @abstractmethod
  def convertNode(self, gen): pass

class VariableNode(Node):
  nodename = gr.VARIABLE_NAME

  def __init__(self, name):
    self.name = name

  def convertNode(self, gen):
    return gen.createVar(self)

class FunctionNode(Node):
  nodename = gr.FUNCTION_NAME

  def __init__(self, name):
    self.name = name

class EnumNode(Node):
  nodename = gr.ENUM_NAME

  def __init__(self, name):
    self.name = name

  def convertNode(self, gen):
    return gen.createEnum(self)

class StructNode(Node):
  nodename = gr.STRUCT_NAME

  def __init__(self, name):
    self.name = name

  def convertNode(self, gen):
    return gen.createStruct(self)

class ClassNode(Node):
  nodename = gr.CLASS_NAME

  def __init__(self, name):
    self.name = name

  def convertNode(self, gen):
    return gen.createClass(self)

class SelectFromNode(Node):
  nodename = gr.SELECTFROM_NAME

  def __init__(self, name):
    self.name = name

  def convertNode(self, gen):
    return gen.createSelectFrom(self)

class SelectConcatNode(Node):
  nodename = gr.SELECTCONCAT_NAME

  def __init__(self, names):
    self.names = names

  def convertNode(self, gen):
    return gen.createSelectConcat(self)

class TagNode(Node):
  nodename = gr.TAG_NAME

  def __init__(self, name):
    self.name = name

  def convertNode(self, gen):
    return gen.createTag(self)

class Gen(object):
  """Base class for all generators."""

  def __init__(self):
    pass

  @abstractmethod
  def convert(self, nodes): pass

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

class Formatter(object):

  @abstractmethod
  def format(self, nodes): pass
