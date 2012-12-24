import unittest
from mutant.loader import Loader
from mutant import errors
import os.path


DATA_PATH = os.path.join(os.path.dirname(__file__), 'data/loader')

class LoaderTest(unittest.TestCase):

  def setUp(self):
    self.loader = Loader()
    paths = [
        os.path.join(DATA_PATH, 'patha'),
        os.path.join(DATA_PATH, 'pathb'),
        ]
    self.loader.setPaths(':'.join(paths))

  def testConvertNameToPath(self):
    actual = self.loader.convertNameToPath('tasker.admin')
    expected = 'tasker/admin'
    self.assertEqual(actual, expected)

  def testGetModulePath(self):
    actual = self.loader.getModulePath('observable', None)
    expected = os.path.join(DATA_PATH, 'pathb/observable')
    self.assertEqual(actual, expected)

  def testGetModulePathError(self):
    self.assertRaises(errors.ModuleNotFound, self.loader.getModulePath, 'notexists', None)

  def testLoadModuleSources(self):
    module = self.loader.loadModule('site')
    self.assertEqual(module.sources[0].filename, os.path.join(DATA_PATH, 'patha/site/main.mut'))
    self.assertEqual(module.sources[1].filename, os.path.join(DATA_PATH, 'patha/site/App.mut'))
    self.assertEqual(len(module.modules), 1)

