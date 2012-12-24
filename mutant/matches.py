from abc import abstractmethod
from mutant.common import getTokensRange
from mutant import grammar


def mergeMatches(leftIndex, rightIndex, matches):
  merged = Match(rightIndex, leftIndex)
  for match in matches:
    # merge leftIndex, rightIndex, params, handlers
    if match.leftIndex >= 0 and merged.leftIndex > match.leftIndex:
      merged.leftIndex = match.leftIndex
    if match.rightIndex >= 0 and merged.rightIndex < match.rightIndex:
      merged.rightIndex = match.rightIndex
    copyParamsHandlers(merged, match)
  return merged

def copyParamsHandlers(dest, src):
  for key, value in src.params.items():
    dest.params[key] = value
  for key, value in src.handlers.items():
    dest.handlers[key] = value

def extractTokens(leftIndex, rightIndex, tokens):
  return tokens[leftIndex:rightIndex+1]

def findWordIndex(word, leftIndex, rightIndex, tokens):
  for num, token in getTokensRange(leftIndex, rightIndex, tokens):
    if token.word == word:
      return num
  return -1

def findCommaIndex(leftIndex, rightIndex, tokens):
  """
  Find "," symbol and check it not into function params.
  """
  cursor = leftIndex
  while cursor <= rightIndex:
    # skip round brackets
    if tokens[cursor].word == '(':
      closedIndex = findWordIndex(')', cursor+1, rightIndex, tokens)
      # if found brackets then move cursor after brackets
      if closedIndex >= 0:
        cursor = closedIndex + 1
        continue
    if tokens[cursor].word == ',':
      return cursor
    cursor = cursor + 1
  return -1

def tokensToString(tokens):
  buf = []
  for token in tokens:
    buf.append(token.word)
  return ' '.join(buf)

def tokensToArray(tokens):
  return [token.word for token in tokens]

def matchNodes(nodes, leftIndex, rightIndex, source):
    matches = []
    cursor = leftIndex
    for node in nodes:
      match = node.match(cursor, rightIndex, source)
      if match:
        if match.rightIndex >= 0: cursor = match.rightIndex + 1
        matches.append(match)
        if cursor > rightIndex: break
      else:
        return None

    if len(matches) == 0: return None

    merged = mergeMatches(leftIndex, rightIndex, matches)

    return merged

def extractTag(leftIndex, rightIndex, source):
  """
  Return tag
  """
  pass

class Match(object):

  def __init__(self, leftIndex, rightIndex):
    self.leftIndex = leftIndex
    self.rightIndex = rightIndex
    self.params = {}
    self.handlers = {}


class Node(object):

  def __init__(self):
    self.childs = []

  @abstractmethod
  def match(self, leftIndex, rightIndex, source): pass


class QuantNode(Node):

  def __init__(self, nums):
    Node.__init__(self)
    self.delim = None
    self.nums = nums

  def match(self, leftIndex, rightIndex, source):
    """
    Match or not match.
    """
    match = matchNodes(self.childs, leftIndex, rightIndex, source)
    # raise Exception(match.params)
    if match:
      return match
    return Match(-1, -1)

class AltNode(Node):
  
  def __init__(self):
    Node.__init__(self)

  def match(self, leftIndex, rightIndex, source):
    """
    Match one of childs.
    """
    for child in self.childs:
      match = child.match(leftIndex, rightIndex, source)
      if match:
        return match
    return None

class ParamNode(Node):

  def __init__(self, name):
    Node.__init__(self)
    self.name = name

  def match(self, leftIndex, rightIndex, source):
    match = matchNodes(self.childs, leftIndex, rightIndex, source)
    if match:
      match.params[self.name] = extractTokens(match.leftIndex, match.rightIndex, source.tokens)
    return match


class HandleNode(Node):

  def __init__(self, name):
    Node.__init__(self)
    self.name = name

  def match(self, leftIndex, rightIndex, source):
    """
    Handler only find tokens range for further parsing.
    Take indexes for parser function.
    """
    handler = grammar.handlers[self.name]
    if handler == None:
      raise Exception('handler "%s" not found' % self.name)
    return handler(leftIndex, rightIndex, source)

class NamedNode(Node):

  def __init__(self, name):
    Node.__init__(self)
    self.name = name

  def match(self, leftIndex, rightIndex, source):
    """
    Take named rule.
    """
    nodes = grammar.getRule(self.name)
    return matchNodes(nodes, leftIndex, rightIndex, source)


class ValueNode(Node):

  def __init__(self, value):
    Node.__init__(self)
    self.value = value

  def match(self, leftIndex, rightIndex, source):
    if source.tokens[leftIndex].wordtype == self.value:
      return Match(leftIndex, leftIndex)
    return None

