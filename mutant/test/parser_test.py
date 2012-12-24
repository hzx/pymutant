import unittest
from mutant.parser import Parser
from mutant.lexer import Lexer
from mutant import core


class ParserTest(unittest.TestCase):

  def setUp(self):
    self.lexer = Lexer()
    self.parser = Parser()

  def testParseClass(self):
    source = """
      class QuestionDialog extends Dialog {
      }
      """
    # actual = self.parser.

