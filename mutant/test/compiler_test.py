import unittest
from mutant.compiler import Compiler
import os.path


data_path = os.path.join(os.path.dirname(__file__), 'data/compiler')

class CompilerTest(unittest.TestCase):

  def setUp(self):
    self.compiler = Compiler()
