import unittest
from mutant.lexer import Lexer
from mutant.common import Source
from mutant.test.features import *

# TODO(dem) refactor tests - refactored Lexer

class LexerTestCase(unittest.TestCase):
  def setUp(self):
    self.lex = Lexer()

  def assertData(self, code, tokens):
    skiplines = []
    source = Source("source.mut", code.split("\n"), skiplines)
    self.lex.parse([source])

    actual = [token.word for token in self.lex.tokens]
    self.assertListEqual(actual, tokens)

class LexerTest(LexerTestCase):
  """
  Test parse language constructions tokens.
  """

  def testIntLiteral(self):
    self.assertData(INT_LITERAL_CODE, INT_LITERAL_TOKENS)
    
  def testFloatLiteral(self):
    self.assertData(FLOAT_LITERAL_CODE, FLOAT_LITERAL_TOKENS)

  def testStringLiteral(self):
    self.assertData(STRING_LITERAL_CODE, STRING_LITERAL_TOKENS)

  def testBoolVar(self):
    self.assertData(BOOL_VAR_CODE, BOOL_VAR_TOKENS)

  def testIntVar(self):
    self.assertData(INT_VAR_CODE, INT_VAR_TOKENS)
    
  def testFloatVar(self):
    self.assertData(FLOAT_VAR_CODE, FLOAT_VAR_TOKENS)

  def testStringVar(self):
    self.assertData(STRING_VAR_CODE, STRING_VAR_TOKENS)

  def testBoolArrayVar(self):
    self.assertData(BOOL_ARRAY_VAR_CODE, BOOL_ARRAY_VAR_TOKENS)

  def testIntArrayVar(self):
    self.assertData(INT_ARRAY_VAR_CODE, INT_ARRAY_VAR_TOKENS)
    
  def testFloatArrayVar(self):
    self.assertData(FLOAT_ARRAY_VAR_CODE, FLOAT_ARRAY_VAR_TOKENS)

  def testStringArrayVar(self):
    self.assertData(STRING_ARRAY_VAR_CODE, STRING_ARRAY_VAR_TOKENS)

  def testIdentifierArrayVarCode(self):
    self.assertData(IDENTIFIER_ARRAY_VAR_CODE, IDENTIFIER_ARRAY_VAR_TOKENS)
    
  def testAnonFunction(self):
    self.assertData(ANON_FUNCTION_CODE, ANON_FUNCITON_TOKENS)

  def testAnonFunctionParams(self):
    self.assertData(ANON_FUNCTION_PARAMS_CODE, ANON_FUNCTION_PARAMS_TOKENS)

  def testFunction(self):
    self.assertData(FUNCTION_CODE, FUNCTION_TOKENS)

  def testFunctionParams(self):
    self.assertData(FUNCTION_PARAMS_CODE, FUNCTION_PARAMS_TOKENS)

  def testEnum(self):
    self.assertData(ENUM_CODE, ENUM_TOKENS)

  def testStruct(self):
    self.assertData(STRUCT_CODE, STRUCT_TOKENS)

  def testClass(self):
    self.assertData(CLASS_CODE, CLASS_TOKENS)

  def testXmlTagSingle(self):
    self.assertData(XML_TAG_SINGLE_CODE, XML_TAG_SINGLE_TOKENS)

  def testXmlTag(self):
    self.assertData(XML_TAG_CODE, XML_TAG_TOKENS)

  def testSelectFrom(self):
    self.assertData(SELECT_FROM_CODE, SELECT_FROM_TOKENS)

  def testSelectConcat(self):
    self.assertData(SELECT_CONCAT_CODE, SELECT_CONCAT_TOKENS)
