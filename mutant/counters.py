from mutant.matches import Match
from mutant.common import getTokensRange


class BracketCounter(object):

  def _resetCounters(self):
    self.roundCount = 0
    self.squareCount = 0
    self.curlyCount = 0

    self.bracketMap = {'(':')', '[':']', '{':'}'}

  def _calculateCounters(self, word):
    if word == '(':
      self.roundCount = self.roundCount + 1
      return
    if word == ')':
      self.roundCount = self.roundCount - 1
      return
    if word == '[':
      self.squareCount = self.squareCount + 1
      return
    if word == ']':
      self.squareCount = self.squareCount - 1
      return
    if word == '{':
      self.curlyCount = self.curlyCount + 1
      return
    if word == '}':
      self.curlyCount = self.curlyCount - 1
      return

  def _checkCounters(self):
    # counters must be 0
    if self.roundCount != 0:
      raise errors.RoundBracketError(self.source.filename)
    if self.squareCount != 0:
      raise errors.SquareBracketError(self.source.filename)
    if self.curlyCount != 0:
      raise errors.CurlyBracketError(self.source.filename)

  def _checkZero(self):
    return self.roundCount == 0 and self.squareCount == 0 and self.curlyCount == 0

  def _getCloseBracket(self, openBracket):
    return self.bracketMap[openBracket]

  def check(self, leftIndex, rightIndex, source):
    self.source = source
    self._resetCounters()
    for num, token in getTokensRange(leftIndex, rightIndex, source.tokens):
      self._calculateCounters(token.word)
    self._checkCounters()

  def findPair(self, leftIndex, rightIndex, source):
    """
    tokens[leftIndex] must be opened bracket
    """
    self._resetCounters()
    # open bracket
    openBracket = source.tokens[leftIndex].word
    closeBracket = self._getCloseBracket(openBracket)
    # find closeBracket and check counters must be zero
    for num, token in getTokensRange(leftIndex, rightIndex, source.tokens):
      self._calculateCounters(token.word)
      # found close bracket
      if token.word == closeBracket and self._checkZero():
        return num

    return None

class TagBracketCounter(object):

  def __init__(self):
    self.resetCounter()
    self.openBrackets = ['<', '</']
    self.closeBrackets = ['>', '/>']

  def resetCounter(self):
    self.count = 0

  def calculateCounter(self, word):
    if word in self.openBrackets: 
      self.count = self.count + 1
    if word in self.closeBrackets:
      self.count = self.count - 1

  def check(self, leftIndex, rightIndex, source):
    self.resetCounter()
    for num, token in getTokensRange(leftIndex, rightIndex, source.tokens):
      self.calculateCounter(token.word)
    if self.count != 0:
      raise Exception('tag open/closed brackets error, linenum "%d", source "%s"' % (source.tokens[leftIndex].linenum, source.filename))

  def checkZero(self):
    return self.count == 0

  def findPair(self, leftIndex, rightIndex, source):
    self.resetCounter()
    for num, token in getTokensRange(leftIndex, rightIndex, source.tokens):
      self.calculateCounter(token.word)
      if token.word in self.closeBrackets and self.checkZero():
        return num
    return -1
