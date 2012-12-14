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

  def setBody(self, node):
    self.body = node

class FunctionNode(Node):

  def __init__(self, decltype, name):
    self.nodetype = 'function'
    self.decltype = decltype
    self.name = name
    self.params = {}
    self.bodyNodes = []

  def addParameter(self, name, decltype):
    """
    params:
      param - Param type
    """
    self.params[name] = decltype

  def addBodyNode(self, node):
    self.bodyNodes.append(node)

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

  def __init__(self, collection):
    self.nodetype = 'select_from'
    self.collection = collection

  def addWhere(self, where):
    self.where = where

  def addOrder(self, order_field):
    self.orderField = order_field


class SelectConcatNode(Node):
  
  def __init__(self):
    self.nodetype = 'select_concat'
    self.collections = []

  def addCollections(self, collections):
    self.collections = collections


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
