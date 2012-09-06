import unittest

class PreprocessorTest(unittest.TestCase):
  def setUp(self):
    self.value = True

  def test_equal(self):
    self.assertEqual(self.value, True)
