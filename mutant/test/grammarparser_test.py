import unittest
import re
from mutant import grammar as gr
from mutant import grammarparser as grp
from mutant.grammarparser import GrammarParser, ValueNodeParser, AltNodeParser, QuantNodeParser


class GrammarParserReTest(unittest.TestCase):

  def testQuantRe(self):
    sources = [
        '({type} name `,`)?',
        '({type} name `,`)*',
        '({type} name `,`)+',
        '({type} name){1}',
        ]
    quant_re = re.compile(grp.QUANT_RE)
    for source in sources:
      self.assertEqual(quant_re.findall(source), [source])

class GrammarParserTest(unittest.TestCase):

  def setUp(self):
    self.parser = GrammarParser()

  def testParseSourceHandled(self):
    source = 'int create ( {params} ) { {funcbody}! }'
    actual = self.parser.parseSource(source)
    expected = ['int', 'create', '(', '{params}', ')', '{', '{funcbody}!', '}']
    self.assertListEqual(actual, expected)

  def testParseSourceVariable(self):
    actual = self.parser.parseSource(gr.VARIABLE)
    expected = ['var|{type}', 'name', '(= {expression})?', ';']
    self.assertListEqual(actual, expected)

  def testParseSourceFunction(self):
    actual = self.parser.parseSource(gr.FUNCTION)
    expected = ['({type})?', '(name)?', '(', '{params}', ')', '{', '{funcbody}', '}']
    self.assertListEqual(actual, expected)

  def testParseSourceEnum(self):
    actual = self.parser.parseSource(gr.ENUM)
    expected = ['enum', 'name', '{', '(name = {intdigit} ;)*', '}']
    self.assertListEqual(actual, expected)

  def testParseSourceStruct(self):
    actual = self.parser.parseSource(gr.STRUCT)
    expected = ['struct', 'name', '{', '({type} name ;)*', '}']
    self.assertListEqual(actual, expected)

  def testParseSourceClass(self):
    actual = self.parser.parseSource(gr.CLASS)
    expected = ['class', 'name', '(extends name)?', '{', '{constructor}|{variable}|{function}', '}']
    self.assertListEqual(actual, expected)

  def testParseSourceSelectFrom(self):
    actual = self.parser.parseSource(gr.SELECTFROM)
    expected = ['select', 'from', 'name', 'where', '{expression}', '(order by {orderbyparams})?']
    self.assertListEqual(actual, expected)

  def testParseSourceSelectConcat(self):
    actual = self.parser.parseSource(gr.SELECTCONCAT)
    expected = ['select', 'concat', '{concatparams}']
    self.assertListEqual(actual, expected)

  def testParseSourceTag(self):
    actual = self.parser.parseSource(gr.TAG)
    expected = ['<', 'name', '{tagattrs}', '>', '({tag}|{singletag})*', '</', 'name', '>']
    self.assertListEqual(actual, expected)

  def testParseSourceSingleTag(self):
    actual = self.parser.parseSource(gr.SINGLETAG)
    expected = ['<', 'name', '{tagattrs}', '/>']
    self.assertListEqual(actual, expected)

  def testParseSourceType(self):
    actual = self.parser.parseSource(gr.TYPE)
    expected = ['{arraytype}|{maptype}|{simpletype}']
    self.assertListEqual(actual, expected)
