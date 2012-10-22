'''
Grammar consist of words, alternatives, sentences
'''


import re
from mutant import grammar as gr
from abc import abstractmethod

NT_VALUE = 'value'
NT_ALT = 'alt'
NT_QUANT = 'quant'

class NodeParser(object):

  def __init__(self):
    pass

  @abstractmethod
  def matchTokens(self, tokens, left, right):
    """
    Match tokens in array tokens from left to right indexes.
    Return matched left and right indexes.
    """
    pass

class ValueNodeParser(NodeParser):
  """value"""

  def __init__(self, value):
    selt.nodetype = NT_VALUE
    self.value = value

  def matchTokens(self, tokens, left, right):
    pass

class AltNodeParser(NodeParser):
  """|"""

  def __init__(self, values):
    self.nodetype = NT_ALT
    self.values = values

  def matchTokens(self, tokens, left, right):
    pass

class QuantNodeParser(NodeParser):
  """? or * or + sentences"""

  def __init__(self):
    self.nodetype = NT_QUANT

  def matchTokens(self, tokens, left, right):
    pass

CONTAINS_RE = '\s*\('
QUANT_RE = '\([^()]+\)(?:[!?*+]|{[0-9,]+})'
ALTVALUE_RE = '(?:[^|\s]+[|]?)+'

QUANT_QUEST_RE = '\([^()]+\)\?'
QUANT_STAR_RE = '\([^()]+\)\*'
QUANT_PLUS_RE = '\([^()]+\)\+'
QUANT_CURLY_RE = '\([^()]+\)\{[\d,]+\}'
NAMED_RE = '\{(%s)\}' % gr.NAME_RE
NAMED_HANDLE_RE = '\{(%s)\}\!' % gr.NAME_RE
SYMBOLS_RE = '\(|\)|\[|\]|\{|\}|\=|\;|\*|</|/>|<|>'

class GrammarParser(object):
  """
  Parse grammar and create corresponding parsing classes.
  """

  def __init__(self):
    # tokens re parse by tokens
    self.tokens_re = re.compile(
        '|'.join([QUANT_RE, ALTVALUE_RE]))

    # type detection and extract parameters
    self.quant_re = re.compile(QUANT_RE)
    self.alt_re = re.compile('|')
    self.named_re = re.compile(NAMED_RE)

    # create source grammar map by name
    self.sourceRules = {
        # main grammar rules
        gr.VARIABLE_NAME: gr.VARIABLE,
        gr.FUNCTION_NAME: gr.FUNCTION,
        gr.ENUM_NAME: gr.ENUM,
        gr.STRUCT_NAME: gr.STRUCT,
        gr.CLASS_NAME: gr.CLASS,
        gr.SELECTFROM_NAME: gr.SELECTFROM,
        gr.SELECTCONCAT_NAME: gr.SELECTCONCAT,
        gr.TAG_NAME: gr.TAG,
        gr.SINGLETAG_NAME: gr.SINGLETAG,
        # subgrammar rules
        gr.SIMPLETYPE_NAME: gr.SIMPLETYPE,
        gr.ARRAYTYPE_NAME: gr.ARRAYTYPE,
        gr.MAPTYPE_NAME: gr.MAPTYPE,
        gr.TYPE_NAME: gr.TYPE,
        gr.IFELSE_NAME: gr.IFELSE,
        gr.ELSE_NAME: gr.ELSE,
        gr.VARLOCAL_NAME: gr.VARLOCAL,
        gr.FUNCCALL_NAME: gr.FUNCCALL,
        }

    # parsed grammar map by name
    self.rules = {}

    # self.tokens_re = re.compile(TOKENS_RE)

  def parse(self):
    # parse every grammar rule
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
    # check names node
    if self.named_re.match(token) != None:
      return self.createNamedNode(token)
    return self.createValueNode(token)

  def createQuantNode(self, source):
    pass

  def createAltNode(self, source):
    pass

  def createNamedNode(self, source):
    pass

  def createValueNode(self, source):
    pass
