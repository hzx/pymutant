from abc import abstractmethod


class Param(object):

  def __init__(self, decltype, name):
    self.decltype = decltype
    self.name = name


"""
Language semantic nodes.
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

  def setBodyReactive(isReactive):
    self.bodyReactive = isReactive

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

class StructVariableNode(Node):

  def __init__(self, decltype, name):
    self.nodetype = 'struct_variable'
    self.decltype = decltype
    self.name = name
    # used like in class constructor, but with other semantics
    self.inits = {}

  def addInit(self, name, body):
    self.inits[name] = body

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

class InsertNode(Node):

  def __init__(self, collName):
    self.nodetype = 'insert'
    self.collName = collName
    self.value = None
    self.isAfter = False
    self.isBefore = False
    self.where = None

  def setValue(self, value):
    self.value = value

  def setAfter(self):
    self.isAfter = True
    self.isBefore = False

  def setBefore(self):
    self.isAfter = False
    self.isBefore = True

  def setWhere(self, where):
    self.where = where

class SelectOneNode(Node):

  def __init__(self, collName):
    self.nodetype = 'select_one'
    self.collName = collName
    self.where = None

  def setWhere(self, where):
    self.where = where

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

class UpdateNode(Node):

  def __init__(self, collName):
    self.nodetype = 'update'
    self.collName = collName
    self.items = {}
    self.where = None

  def addItem(self, name, value):
    self.items[name] = value

  def setWhere(self, where):
    self.where = where

class DeleteFromNode(Node):

  def __init__(self, collName):
    self.nodetype = 'delete_from'
    self.collName = collName
    self.where = None

  def setWhere(self, where):
    self.where = where

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
  This must looks like VariableNode, because this another representation.
  """

  def __init__(self, value):
    self.nodetype = 'value'
    self.value = value
    self.body = None
    self.bodyReactive = False

  def setBody(self, node):
    self.body = node

  def setBodyReactive(isReactive):
    self.bodyReactive = isReactive

class ArrayBodyNode(Node):
  """
  Contains array body ['item1', 'item2']
  """

  def __init__(self):
    self.nodetype = 'array_body'
    self.items = []

  def addItem(self, node):
    self.items.append(node)

class ArrayValueNode(Node):
  """
  Represents values[index] value expression.
  """

  def __init__(self, value, index):
    self.nodetype = 'array_value'
    self.value = value
    self.index = index

class DictBodyNode(Node):
  """
  Contains dict body {'key1': expr, 'key2': exp}
  """

  def __init__(self):
    self.nodetype = 'dict_body'
    self.items = {}

  def addItem(self, name, node):
    self.items[name] = node

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
