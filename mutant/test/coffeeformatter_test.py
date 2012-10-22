import unittest
from mutant.coffeeformatter import CoffeeFormatter


class CoffeeFormatterTest(unittest.TestCase):

  def setUp(self):
    self.formatter = CoffeeFormatter()
