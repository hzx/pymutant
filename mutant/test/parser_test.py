import unittest
from mutant.common import Source, Token
from mutant import errors
from mutant.parser import Parser, BracketChecker


class BraceCheckerTest(unittest.TestCase):
  
  def setUp(self):
    self.source = Source('test.mut', [], [])
    self.checker = BracketChecker()

  def _getTokens(self, words):
    return [Token(self.source, 0, word) for word in words]

  def testRoundMatch(self):
    words = ['(', 'a', '+', 'b', ')']
    self.checker.check(self._getTokens(words))

  def testRoundMatchError(self):
    words = ['(', 'a', '+', 'b']
    self.assertRaises(errors.RoundBracketError, self.checker.check, self._getTokens(words))

  def testSquareMatch(self):
    words = ['foo', '[', 'a', ']', ';']
    self.checker.check(self._getTokens(words))

  def testSquareMatchError(self):
    words = ['foo', '[', 'a', ';']
    self.assertRaises(errors.SquareBracketError, self.checker.check, self._getTokens(words))

  def testCurlyMatch(self):
    words = ['foo', '{', 'a', '}', ';']
    self.checker.check(self._getTokens(words))

  def testCurlyMatchError(self):
    words = ['foo', '{', 'a', ';']
    self.assertRaises(errors.CurlyBracketError, self.checker.check, self._getTokens(words))

class ParserTest(unittest.TestCase):

  def setUp(self):
    self.parser = Parser()

  def testIntLiteral(self):
    pass
