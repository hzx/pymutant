import unittest
from mutant.compiler import Compiler


class CompilerTest(unittest.TestCase):

  def setUp(self):
    self.compiler = Compiler()
