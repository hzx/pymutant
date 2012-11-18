import unittest
from mutant.grammarparser import GrammarParser, QuantNode, AltNode, HandleNode, \
    NamedNode, ValueNode
from mutant import grammar as gr


class GrammarParserTest(unittest.TestCase):

  def setUp(self):
    self.parser = GrammarParser()

  def testParseSourceAltQuant(self):
    source = '{this}|{ns}'
    expected = [source]
    actual = self.parser.parseSource(source)
    self.assertEqual(actual, expected)

  def testParseTokenQuantQuest(self):
    source = '({type} name `,`)?'
    expected = source
    actual = self.parser.parseToken(source)
    self.assertEqual(actual, expected)

  def testParsetSourceVarbody(self):
    source = gr.VARBODY
    expected = [source]
    actual = self.parser.parseSource(source)
    self.assertEqual(actual, expected)
