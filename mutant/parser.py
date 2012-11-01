from mutant import core
from mutant import common
from mutant import errors


class BracketChecker(object):

  def _resetCounters(self):
    self.roundCount = 0
    self.squareCount = 0
    self.curlyCount = 0

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

  def check(self, tokens):
    self._resetCounters()
    for token in tokens:
      self._calculateCounters(token.word)
    self._checkCounters()

class Parser(object):

  def __init__(self):
    self.bracketChecker = BracketChecker()

    self.firstOperators = ['+', '-']
    self.secondOperators = ['*', '/']
    self.thirdOperators = ['not']

    # compile rules


  def parse(self, tokens):
    self.bracketChecker.check(tokens)

  def handleVariable(self):
    # self.variables.append()
    pass

  def handleFunction(self):
    #self.functions.append()
    pass

  def handleEnum(self):
    # self.enums.append()
    pass

  def handleStruct(self):
    # self.structs.append()
    pass

  def handleClass(self):
    # self.classes.append()
    pass

  def handleSelectFrom(self):
    pass

  def handleSelectConcat(self):
    pass

  def handleTag(self):
    pass
