import unittest
from mutant.lexer import *
from mutant.common import Source
from mutant.test.features import *

# TODO(dem) refactor tests - refactored Lexer

class LexerTestCase(unittest.TestCase):
  def setUp(self):
    self.lex = Lexer()

  def parseCodeHelper(self, code):
    skiplines = []
    source = Source("source.mut", code.split("\n"), skiplines)
    self.lex.parse([source])

  def assertResultsHelper(self, expected):
    actual = [token.word for token in self.lex.tokens]
    self.assertListEqual(actual, expected)

class LexerTest(LexerTestCase):
  """
  Test parse language constructions tokens.
  """

  def testIntLiteral(self):
    """Int literal."""
    self.parseCodeHelper(INT_LITERAL_CODE)
    self.assertResultsHelper(INT_LITERAL_TOKENS)
    
  def testFloatLiteral(self):
    """Float literal."""
    self.parseCodeHelper(FLOAT_LITERAL_CODE)
    self.assertResultsHelper(FLOAT_LITERAL_TOKENS)

  def testStringLiteral(self):
    """String literal."""
    self.parseCodeHelper(STRING_LITERAL_CODE)
    self.assertResultsHelper(STRING_LITERAL_TOKENS)

  def testBoolVar(self):
    """Bool literal."""
    self.parseCodeHelper(BOOL_VAR_CODE)
    self.assertResultsHelper(BOOL_VAR_TOKENS)

  def testIntVar(self):
    self.parseCodeHelper(INT_VAR_CODE)
    self.assertResultsHelper(INT_VAR_TOKENS)
    
  def testFloatVar(self):
    self.parseCodeHelper(FLOAT_VAR_CODE)
    self.assertResultsHelper(FLOAT_VAR_TOKENS)

  def testStringVar(self):
    self.parseCodeHelper(STRING_VAR_CODE)
    self.assertResultsHelper(STRING_VAR_TOKENS)

  def testBoolArrayVar(self):
    self.parseCodeHelper(BOOL_ARRAY_VAR_CODE)
    self.assertResultsHelper(BOOL_ARRAY_VAR_TOKENS)

  def testIntArrayVar(self):
    self.parseCodeHelper(INT_ARRAY_VAR_CODE)
    self.assertResultsHelper(INT_ARRAY_VAR_TOKENS)
    
  def testFloatArrayVar(self):
    self.parseCodeHelper(FLOAT_ARRAY_VAR_CODE)
    self.assertResultsHelper(FLOAT_ARRAY_VAR_TOKENS)

  def testStringArrayVar(self):
    self.parseCodeHelper(STRING_ARRAY_VAR_CODE)
    self.assertResultsHelper(STRING_ARRAY_VAR_TOKENS)

  def testIdentifierArrayVarCode(self):
    self.parseCodeHelper(IDENTIFIER_ARRAY_VAR_CODE)
    self.assertResultsHelper(IDENTIFIER_ARRAY_VAR_TOKENS)
    
  def testAnonFunction(self):
    self.parseCodeHelper(ANON_FUNCTION_CODE)
    self.assertResultsHelper(ANON_FUNCITON_TOKENS)

  def testAnonFunctionParams(self):
    self.parseCodeHelper(ANON_FUNCTION_PARAMS_CODE)
    self.assertResultsHelper(ANON_FUNCTION_PARAMS_TOKENS)

  def testFunction(self):
    self.parseCodeHelper(FUNCTION_CODE)
    self.assertResultsHelper(FUNCTION_TOKENS)

  def testFunctionParams(self):
    self.parseCodeHelper(FUNCTION_PARAMS_CODE)
    self.assertResultsHelper(FUNCTION_PARAMS_TOKENS)

  def testEnum(self):
    self.parseCodeHelper(ENUM_CODE)
    self.assertResultsHelper(ENUM_TOKENS)

  def testStruct(self):
    self.parseCodeHelper(STRUCT_CODE)
    self.assertResultsHelper(STRUCT_TOKENS)

  def testClass(self):
    self.parseCodeHelper(CLASS_CODE)
    self.assertResultsHelper(CLASS_TOKENS)

  def testXmlTagSingle(self):
    self.parseCodeHelper(XML_TAG_SINGLE_CODE)
    self.assertResultsHelper(XML_TAG_SINGLE_TOKENS)

  def testXmlTag(self):
    self.parseCodeHelper(XML_TAG_CODE)
    self.assertResultsHelper(XML_TAG_TOKENS)

  def testSelectFrom(self):
    self.parseCodeHelper(SELECT_FROM_CODE)
    self.assertResultsHelper(SELECT_FROM_TOKENS)

  def testSelectConcat(self):
    self.parseCodeHelper(SELECT_CONCAT_CODE)
    self.assertResultsHelper(SELECT_CONCAT_TOKENS)
