import unittest
from mutant import grammar as gr
from mutant.grammarparser import *


class GrammarParserTest(unittest.TestCase):

  def setUp(self):
    self.parser = GrammarParser()
