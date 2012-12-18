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

  # def testDefine(self):
  #   self.fail('not implemented')

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
    self.assertIsNotNone(var.body)
    self.assertEqual(var.body.nodetype, 'value')
    self.assertEqual(var.body.value.word, '4')

  def testVariableBody(self):
    module = self.compiler.compile(self.paths, 'varbody')
    var = module.variables['num']
    vb = var.body
    self.assertIsNotNone(vb)
    self.assertEqual(vb.nodetype, 'value')
    self.assertEqual(vb.value.word, '4')
    self.assertEqual(vb.value.wordtype, 'litint')

  # def testVariableBodyFunctionParams(self):
  #   self.fail('not implemented')

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
    module = self.compiler.compile(self.paths, 'function')
    func = module.functions['getModerated']
    self.assertEqual(len(func.bodyNodes), 2)
    vn = func.bodyNodes[0]
    rn = func.bodyNodes[1]
    self.assertEqual(vn.nodetype, 'variable')
    self.assertIsNotNone(vn.body)
    self.assertEqual(rn.nodetype, 'return')
    self.assertIsNotNone(rn.body)

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

  # def testEnumBody(self):
  #   self.fail('not implemented')

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

  # def testStructBody(self):
  #   self.fail('not implemented')

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

  # def testClassBase(self):
  #   self.fail('not implemented')

  # def testClassConstructor(self):
  #   self.fail('not implemented')

  # def testClassBody(self):
  #   self.fail('not implemented')

  def testFunctionReturnSingleTag(self):
    module = self.compiler.compile(self.paths, 'singletag')
    self.assertEqual(len(module.functions), 1)

    func = module.functions['renderTemplate']
    self.assertEqual(len(func.bodyNodes), 1)

    rn = func.bodyNodes[0]
    self.assertIsNotNone(rn.body)
    self.assertEqual(rn.nodetype, 'return')

    tn = rn.body
    self.assertEqual(tn.nodetype, 'tag')
    self.assertEqual(tn.name, 'img')

  def testFeatures(self):
    module = self.compiler.compile(self.paths, 'features')

    # test variables

    varTemplate = module.variables.get('template', None)
    self.assertIsNotNone(varTemplate)
    self.assertEqual(varTemplate.name, 'template')

    varTemplateTag = varTemplate.body
    self.assertIsNotNone(varTemplateTag)

    self.assertEqual(varTemplateTag.nodetype, 'tag')
    self.assertEqual(len(varTemplateTag.childs), 3)
    self.assertEqual(len(varTemplateTag.attributes), 1)

    varTemplateId = varTemplateTag.attributes.get('id', None)
    self.assertIsNotNone(varTemplateId)
    self.assertEqual(varTemplateId.nodetype, 'value')

    arrayChildAttr = varTemplateTag.childs[1]
    self.assertIsNotNone(arrayChildAttr)
    self.assertEqual(len(arrayChildAttr.attributes), 2)

    classAttr = arrayChildAttr.attributes.get('class', None)
    self.assertIsNotNone(classAttr)
    self.assertEqual(classAttr.nodetype, 'array_body')
    self.assertEqual(len(classAttr.items), 2)
    self.assertEqual(classAttr.items[0].nodetype, 'value')
    self.assertEqual(classAttr.items[0].value.wordtype, 'litstring')
    self.assertEqual(classAttr.items[0].value.word, "'common-content'")
    self.assertEqual(classAttr.items[1].nodetype, 'value')
    self.assertEqual(classAttr.items[1].value.wordtype, 'litstring')
    self.assertEqual(classAttr.items[1].value.word, "'main-content'")

    # test functions

    # test enums

    # test structs

    # test classes
