import unittest
from mutant.parser import Parser


class ParserTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = Parser()

class ParserTest(ParserTestCase):

  def testIntLiteral(self):
    pass
