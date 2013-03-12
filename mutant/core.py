from abc import abstractmethod
import re


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
  """
  decltype - tokens
  name - string
  body - node
  """

  def __init__(self, decltype, name):
    self.nodetype = 'variable'
    self.decltype = decltype
    self.name = name
    self.body = None
    self.bodyReactive = False

  def setBody(self, node):
    self.body = node

  def setBodyReactive(self, isReactive):
    self.bodyReactive = isReactive

class FunctionNode(Node):
  """
  name - string
    for constructor it None
  decltype - tokens
    for constructor it None
  params - array of array of name,type
    name - string
    type - tokens
  bodyNodes - nodes
  """

  def __init__(self, decltype, name):
    self.nodetype = 'function'
    self.attributes = ''
    self.decltype = decltype
    self.name = name
    self.params = []
    self.bodyNodes = []

  def addParameter(self, name, decltype):
    """
    params:
      param - Param type
    """
    self.params.append([name, decltype])

  def addBodyNode(self, node):
    self.bodyNodes.append(node)

  def addSupercallNode(self, node):
    self.bodyNodes.insert(0, node)


class EnumNode(Node):
  """
  name - string
  members - dict of name:value
    name - string
    value - litint
  """
    
  def __init__(self, name):
    self.nodetype = 'enum'
    self.name = name
    self.members = {}

  def addMember(self, name, value):
    self.members[name] = value


class StructNode(Node):
  """
  name - string
  baseName - string or None
  variables - dict of name:variableNode
    name - string
    variableNode - StructVariableNode
  """

  def __init__(self, name, baseName):
    self.nodetype = 'struct'
    self.name = name
    self.baseName = baseName
    self.variables = {}

  def addVariable(self, variable):
    self.variables[variable.name] = variable

class StructVariableNode(Node):
  """
  decltype - tokens
  name - string
  inits - dict of name:node
    name - string
    node - node, must be ValueNode
  """

  def __init__(self, decltype, name):
    self.nodetype = 'struct_variable'
    self.decltype = decltype
    self.name = name
    # used like in class constructor, but with other semantics
    self.inits = {}

  def addInit(self, name, body):
    self.inits[name] = body

class ClassNode(Node):
  """
  name - string
  baseName - string or None
  constructor - FunctionNode or None
  variables - dict of name:variableNode
    name - string
    variableNode - VariableNode
  functions - dict of name:functionNode
    name - string
    functionNode - FunctionNode
  """

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

  def getVariablesName(self):
    return ', '.join([vname for vname, va in self.variables.items()])

class InsertNode(Node):
  """
  collName - string
  value - ValueNode
  isAfter - bool type
  isBefore - bool type
  where - expr, FunctionCallNode
  """

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

class SelectCountNode(Node):
  """
  collName - string
  """

  def __init__(self, collName):
    self.nodetype = 'select_count'
    self.collName = collName

class SelectOneNode(Node):
  """
  collName - string
  where - expr, FunctionCallNode
  """

  def __init__(self, collName):
    self.nodetype = 'select_one'
    self.collName = collName
    self.where = None

  def setWhere(self, where):
    self.where = where

class SelectFromNode(Node):
  """
  collName - string
  where - expr, FunctionCallNode
  orderField - string
  sortOrder - string, asc|desc
  """

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
  """
  collections - array of string
  """
  
  def __init__(self):
    self.nodetype = 'select_concat'
    self.collections = []

  def addCollection(self, collection):
    self.collections.append(collection)

class SelectSumNode(Node):
  """
  collName - string
  by - string
  """

  def __init__(self, collName, by):
    self.nodetype = 'select_sum'
    self.collName = collName
    self.by = by

class UpdateNode(Node):
  """
  collName - string
  items - dict of name:expr
    name - string
    expr - ValueNode
  where - FunctionCallNode
  """

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
  """
  collName - string
  where - FunctionCallNode
  """

  def __init__(self, collName):
    self.nodetype = 'delete_from'
    self.collName = collName
    self.where = None

  def setWhere(self, where):
    self.where = where

class TagNode(Node):
  """
  name - string
  attributes - dict of name:variable
    name - string
    variable - ValueNode
  childs - array of TagNode, ValueNode, FunctionCallNode
  """

  def __init__(self, name):
    self.nodetype = 'tag'
    self.name = name
    self.attributes = {}
    self.childs = []

  def addAttribute(self, name, value):
    self.attributes[name] = value

  def addChild(self, tag):
    self.childs.append(tag)

class IfNode(Node):
  """
  expr - FunctionCallNode
  body - nodes
  elseBody - nodes
  """

  def __init__(self):
    self.nodetype = 'if'
    self.expr = None
    self.body = []
    self.elseBody = []

class ForNode(Node):
  """
  collName - string
  itemName - string
  body - node
  """

  def __init__(self):
    self.nodetype = 'for'
    self.collName = None
    self.itemName = None
    self.body = []

# for calculations

class ValueNode(Node):
  """
  Contains all values - literals, variables.
  This must looks like VariableNode, because this another representation.

  value - string, variableNode.name but this may with prefix
  body - any Node from variable body rule
  isLitBool, isLitInt, isLitFloat, isLitString, isName - only one flag must be True
  """

  def __init__(self, value):
    self.nodetype = 'value'
    self.value = value
    self.body = None
    self.bodyReactive = False
    self.isLitBool = False
    self.isLitInt = False
    self.isLitFloat = False
    self.isLitString = False
    self.isName = False
    self.isTagString = False

  def setBody(self, node):
    self.body = node

  def setBodyReactive(self, isReactive):
    self.bodyReactive = isReactive

  def checkLitString(self):
    return re.match("^'.*'$", self.value) != None

class ArrayBodyNode(Node):
  """
  Contains array body ['item1', 'item2']
  items - array of nodes, any Node from variable body rule
  """

  def __init__(self):
    self.nodetype = 'array_body'
    self.items = []

  def addItem(self, node):
    self.items.append(node)

class ArrayValueNode(Node):
  """
  Represents values[index] value expression.
  value - string
  index - litint
  """

  def __init__(self, value, index):
    self.nodetype = 'array_value'
    self.value = value
    self.index = index

class DictBodyNode(Node):
  """
  Contains dict body {'key1': expr, 'key2': exp}
  items - dict of name:expr
    name - string
    expr - any Node from variable body rule
  """

  def __init__(self):
    self.nodetype = 'dict_body'
    self.items = {}

  def addItem(self, name, node):
    self.items[name] = node

class ReturnNode(Node):
  """
  Function return node
  body - any Node from variable body rule
  """

  def __init__(self):
    self.nodetype = 'return'
    self.body = None

  def setBody(self, node):
    self.body = node

class FunctionCallNode(Node):
  """
  name - string
    for constructor is class name
  params - nodes
    for constructor is empty
  inits - use for constructor only, dict of name:node
    name - string
    node - node
  """
  
  def __init__(self, name):
    self.name = name
    self.nodetype = 'functioncall'
    self.params = []
    self.inits = {}

    self.isConstructorCall = False

  def addParameter(self, node):
    self.params.append(node)

  def addInit(self, name, body):
    self.inits[name] = body


