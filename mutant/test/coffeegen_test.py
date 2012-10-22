import unittest
from mutant.coffeegen import CoffeeGen


class CoffeeGenTest(unittest.TestCase):

  def setUp(self):
    self.gen = CoffeeGen()
