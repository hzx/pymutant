import unittest
from mutant.preprocessor import Preprocessor


class PreprocessorTest(unittest.TestCase):

  def setUp(self):
    self.preprocessor = Preprocessor()

  def testPkgToFilename(self):
    actual = self.preprocessor.pkgToFilename('tracker.admin')
    expected = 'tracker/admin.mut'
    self.assertEqual(actual, expected)
