'''
Grammar consist of words, alternatives, sentences
'''


import re
from mutant import grammar as gr
from abc import abstractmethod

NT_VALUE = 'value'
NT_ALT = 'alt'
NT_QUANT = 'quant'
NT_HANDLE = 'handle'
NT_NAMED = 'named'

class Node(object):

  def __init__(self):
    pass

  @abstractmethod
  def matchTokens(self, tokens, left, right):
    """
    Match tokens in array tokens from left to right indexes.
    Return matched left and right indexes or None.
    """
    pass

  @abstractmethod
  def addChild(self, node):
    """
    """
    pass

class ValueNode(Node):
  """value"""

  def __init__(self, value):
    selt.nodetype = NT_VALUE
    self.value = value

  def matchTokens(self, tokens, left, right):
    pass

class AltNode(Node):
  """|"""

  def __init__(self, values):
    self.nodetype = NT_ALT
    self.values = values

  def matchTokens(self, tokens, left, right):
    pass

class QuantNode(Node):
  """? or * or + sentences"""

  def __init__(self):
    self.nodetype = NT_QUANT

  def matchTokens(self, tokens, left, right):
    pass

class HandleNode(Node):
  """{name}!"""

  def __init__(self):
    self.nodetype = NT_HANDLE

class NamedNode(Node):
  """{name}"""

  def __init__(self):
    self.nodetype = NT_NAMED

ALL_RE = '\([^()]+\)(?:[!?*+]|{[0-9,]+})'

QUANT_RE = '\([^()]+\)(?:[!?*+])'
ALTVALUE_RE = '(?:[^|\s]+[|]?)+'
HANDLE_RE = '\{(?:%s)\}\!' % gr.NAME_RE
NAMED_RE = '\{(?:%s)\}' % gr.NAME_RE

SYMBOLS_RE = '\(|\)|\[|\]|\{|\}|\=|\;|\*|</|/>|<|>'

QUANT_CURLY_RE = '\([^()]+\)\{[\d,]+\}'

class GrammarParser(object):
  """
  Parse grammar and create corresponding parsing classes.
  """

  def __init__(self):
    # tokens re parse by tokens
    self.tokens_re = re.compile(
        '|'.join([ALL_RE, ALTVALUE_RE, HANDLE_RE, NAMED_RE]))

    # type detection and extract parameters
    self.quant_re = re.compile(QUANT_RE)
    self.alt_re = re.compile('|')
    self.handle_re = re.compile(HANDLE_RE)
    self.named_re = re.compile(NAMED_RE)

    # quant for detect quantifier and extract data
    self.quant_quest_re = re.compile('\([^()]+\)\?')
    self.quant_star_re = re.compile('\([^()]+\)\*')
    self.quant_plus_re = re.compile('\([^()]+\)\+')
    self.quant_curly_re = re.compile('\([^()]+\)\{[\d,]+\}')

    # 
    
    # parsed grammar map by name
    self.rules = {}

    # map rules names and handles
    self.handleMap = {}

    # self.tokens_re = re.compile(TOKENS_RE)

  def compileRules(self):
    pass

  def checkGrammar(self):
    pass

  def parseGrammar(self, grammar):
    # parse grammar rule
    pass

  def parseSource(self, source):
    return self.tokens_re.findall(source)

  def parseToken(self, token):
    # check quant node
    if self.quant_re.match(token) != None:
      return self.createQuantNode(token)
    # check alt node - just split by |
    if self.alt_re.match(token) != None:
      return self.createAltNode(token)
    # check handle node
    if self.handle_re.match(token) != None:
      return self.createHandleNode(token)
    # check named node
    if self.named_re.match(token) != None:
      return self.createNamedNode(token)
    return self.createValueNode(token)

  def createQuantNode(self, token):
    return token

  def createAltNode(self, token):
    return self.alt_re.split(token)

  def createHandleNode(self, token):
    pass

  def createNamedNode(self, token):
    pass

  def createValueNode(self, token):
    pass
