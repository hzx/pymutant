from abc import abstractmethod


class Param(object):

  def __init__(self, decltype, name):
    self.decltype = decltype
    self.name = name


"""
Language semantic elements.
"""

class Node(object):

  def __init__(self):
    pass

class VariableNode(Node):

  def __init__(self, decltype, name):
    self.nodetype = 'variable'
    self.decltype = decltype
    self.name = name
    self.body = None
    self.bodyReactive = False

  def setBody(self, node):
    self.body = node

  def setBodyReactive(flag):
    self.bodyReactive = flag

class FunctionNode(Node):

  def __init__(self, decltype, name):
    self.nodetype = 'function'
    self.decltype = decltype
    self.name = name
    self.params = {}
    self.bodyNodes = []
    # used only for class constructor
    self.inits = {}

  def addParameter(self, name, decltype):
    """
    params:
      param - Param type
    """
    self.params[name] = decltype

  def addBodyNode(self, node):
    self.bodyNodes.append(node)

  def addInit(self, name, body):
    self.inits[name] = body


class EnumNode(Node):
    
  def __init__(self, name):
    self.nodetype = 'enum'
    self.name = name
    self.members = {}

  def addMember(self, name, value):
    self.members[name] = value


class StructNode(Node):

  def __init__(self, name, baseName):
    self.nodetype = 'struct'
    self.name = name
    self.baseName = baseName
    self.variables = {}
    self.functions = {}

  def addVariable(self, variable):
    self.variables[variable.name] = variable

  def addFunction(self, function):
    self.functions[function.name] = function


class ClassNode(Node):

  def __init__(self, name, baseName):
    self.nodetype = 'class'
    self.name = name
    self.baseName = baseName
    self.constructor = None
    self.variables = {}
    self.functions = {}

  def setConstructor(self, function):
    self.constructor = function

  def addVariable(self, variable):
    self.variables[variable.name] = variable

  def addFunction(self, function):
    self.functions[function.name] = function

class SelectFromNode(Node):

  def __init__(self, collName):
    self.nodetype = 'select_from'
    self.collName = collName
    self.where = None
    self.orderField = None
    self.sortOrder = None

  def setWhere(self, where):
    self.where = where

  def setOrderField(self, orderField, sortOrder):
    self.orderField = orderField
    self.sortOrder = sortOrder

class SelectConcatNode(Node):
  
  def __init__(self):
    self.nodetype = 'select_concat'
    self.collections = []

  def addCollection(self, collection):
    self.collections.append(collection)

class TagNode(Node):

  def __init__(self, name):
    self.nodetype = 'tag'
    self.name = name
    self.attributes = {}
    self.childs = []

  def addAttribute(self, name, value):
    self.attributes[name] = value

  def addChild(self, tag):
    self.childs.append(tag)

# for calculations

class ValueNode(Node):
  """
  Contains all values - literals, variables.
  """

  def __init__(self, value):
    self.nodetype = 'value'
    self.value = value

class ArrayBodyNode(Node):
  """
  Contains array body ['item1', 'item2']
  """

  def __init__(self):
    self.nodetype = 'array_body'
    self.items = []

  def addItem(self, node):
    self.items.append(node)

class ReturnNode(Node):
  """
  Function return node
  """

  def __init__(self):
    self.nodetype = 'return'
    self.body = None

  def setBody(self, node):
    self.body = node

class FunctionCallNode(Node):
  
  def __init__(self, name):
    self.name = name
    self.nodetype = 'functioncall'
    self.params = []

  def addParameter(self, node):
    self.params.append(node)
