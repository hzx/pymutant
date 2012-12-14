import unittest
from mutant.compiler2 import Compiler
from mutant import common
from mutant import matches
import os.path


data_path = os.path.join(os.path.dirname(__file__), 'data/compiler')

class CompilerTest(unittest.TestCase):

  def setUp(self):
    self.compiler = Compiler()
    self.paths = data_path

  def testImport(self):
    source = """
    import rb.tasker as tasker;
    """
    pass

  def testDefine(self):
    self.fail('not implemented')

  def testVariable(self):
    module = self.compiler.compile(self.paths, 'variableint')
    self.assertEqual(len(module.variables), 1)
    self.assertEqual(len(module.functions), 0)
    self.assertEqual(len(module.enums), 0)
    self.assertEqual(len(module.structs), 0)
    self.assertEqual(len(module.classes), 0)
    var = module.variables['num']
    self.assertEqual(var.nodetype, 'variable')
    self.assertEqual(matches.tokensToString(var.decltype), 'int')
    self.assertEqual(var.name, 'num')
    self.assertIsNone(var.body)

  def testVariableBody(self):
    module = self.compiler.compile(self.paths, 'varbody')
    var = module.variables['num']
    self.assertIsNotNone(var.body)

  def testFunction(self):
    module = self.compiler.compile(self.paths, 'emptyfunction')
    self.assertEqual(len(module.variables), 0)
    self.assertEqual(len(module.functions), 1)
    self.assertEqual(len(module.enums), 0)
    self.assertEqual(len(module.structs), 0)
    self.assertEqual(len(module.classes), 0)
    func = module.functions['foo']
    self.assertEqual(func.nodetype, 'function')
    self.assertEqual(matches.tokensToString(func.decltype), 'void')
    self.assertEqual(func.name, 'foo')
    self.assertEqual(len(func.params), 0)

  def testFunctionParams(self):
    # self.fail('not implemented')
    module = self.compiler.compile(self.paths, 'funcparams')
    self.assertEqual(len(module.variables), 0)
    self.assertEqual(len(module.functions), 1)
    self.assertEqual(len(module.enums), 0)
    self.assertEqual(len(module.structs), 0)
    self.assertEqual(len(module.classes), 0)
    func = module.functions['foo']
    self.assertEqual(len(func.params), 2)

  def testFunctionBody(self):
    self.fail('not implemented')

  def testEnum(self):
    module = self.compiler.compile(self.paths, 'emptyenum')
    self.assertEqual(len(module.variables), 0)
    self.assertEqual(len(module.functions), 0)
    self.assertEqual(len(module.enums), 1)
    self.assertEqual(len(module.structs), 0)
    self.assertEqual(len(module.classes), 0)
    en = module.enums['KIND']
    self.assertEqual(en.nodetype, 'enum')
    self.assertEqual(en.name, 'KIND')
    self.assertEqual(len(en.members), 0)

  def testEnumBody(self):
    self.fail('not implemented')

  def testStruct(self):
    module = self.compiler.compile(self.paths, 'emptystruct')
    self.assertEqual(len(module.variables), 0)
    self.assertEqual(len(module.functions), 0)
    self.assertEqual(len(module.enums), 0)
    self.assertEqual(len(module.structs), 1)
    self.assertEqual(len(module.classes), 0)
    st = module.structs['User']
    self.assertEqual(st.nodetype, 'struct')
    self.assertEqual(st.name, 'User')
    self.assertIsNone(st.baseName)
    self.assertEqual(len(st.variables), 0)
    self.assertEqual(len(st.functions), 0)

  def testStructBody(self):
    self.fail('not implemented')

  def testClass(self):
    module = self.compiler.compile(self.paths, 'emptyclass')
    self.assertEqual(len(module.variables), 0)
    self.assertEqual(len(module.functions), 0)
    self.assertEqual(len(module.enums), 0)
    self.assertEqual(len(module.structs), 0)
    self.assertEqual(len(module.classes), 1)
    cl = module.classes['App']
    self.assertEqual(cl.nodetype, 'class')
    self.assertEqual(cl.name, 'App')
    self.assertIsNone(cl.baseName)
    self.assertEqual(len(cl.variables), 0)
    self.assertEqual(len(cl.functions), 0)

  def testClassBase(self):
    self.fail('not implemented')

  def testClassConstructor(self):
    self.fail('not implemented')

  def testClassBody(self):
    self.fail('not implemented')
