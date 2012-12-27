

# Language semantic nodes.

class Node(object):

  def __init__(self):
    pass

class VariableNode(Node):

  def __init__(self, name):
    self.nodetype = 'variable'
    self.name = name
    self.body = None

class FunctionNode(Node):

  def __init__(self, name):
    self.nodetype = 'function'
    self.name = name
    self.params = {}
    self.bodyNodes = []

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
