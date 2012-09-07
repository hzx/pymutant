import unittest
from mutant.grammarparser import *


class GrammarParserTest(unittest.TestCase):

  def setUp(self):
    self.parser = GrammarParser()

  def testBoolDeclaration(self):
    code = " isChecked ;"
    grammar = self.parser.parse(code)
