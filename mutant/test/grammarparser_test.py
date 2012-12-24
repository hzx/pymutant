import unittest
from mutant.grammarparser import GrammarParser
from mutant import grammar
from mutant import matches as mt


class GrammarParserTest(unittest.TestCase):

  def setUp(self):
    self.parser = GrammarParser()
    self.parser.compileGrammar()

  def equalNodes(self, left, right):
    if len(left) != len(right):
      return False

    return True

  def testImport(self):
    importNode = mt.ValueNode('import')
    paramNode = mt.ParamNode('module')
    paramNode.childs = [mt.NamedNode('namespace_name')]
    asNode = mt.ValueNode('as')
    aliasNode = mt.ParamNode('alias')
    aliasNode.childs = [mt.ValueNode('name')]
    endNode = mt.ValueNode(';')

    expected = [importNode, paramNode, asNode, aliasNode, endNode]
    actual = grammar.compiled['import']
    
    self.assertEquals(True, self.equalNodes(actual, expected))
    self.assertEquals(0, len(actual[0].childs))
    self.assertEquals(1, len(actual[1].childs))
    self.assertEquals('as', actual[2].value)

  def testVariable(self):
    actual = grammar.getRule('variable')

    self.assertIsNotNone(actual)
    self.assertEqual(len(actual), 3)

    typeNode = actual[0]
    nameNode = actual[1]
    handleNode = actual[2]

    self.assertEqual(typeNode.name, 'type')
    self.assertEqual(len(typeNode.childs), 1)
    altNode = typeNode.childs[0]
    self.assertEqual(len(altNode.childs), 2)
    self.assertEqual(altNode.childs[0].value, 'var')
    self.assertEqual(altNode.childs[1].name, 'type')

    self.assertEqual(nameNode.name, 'name')
    self.assertEqual(len(nameNode.childs), 1)
    self.assertEqual(nameNode.childs[0].value, 'name')

  def testType(self):
    expected = mt.ParamNode('type')

    altNode = mt.AltNode()
    altNode.childs.append(mt.NamedNode('array_type'))
    altNode.childs.append(mt.NamedNode('simple_type'))

    expected.childs.append(altNode)

    actual = grammar.getRule('type')

    self.assertIsNotNone(actual)
    self.assertEqual(len(actual), 1)
    typeNode = actual[0]
    self.assertEqual(len(typeNode.childs), 2)
    self.assertEqual(typeNode.childs[0].name, 'array_type')
    self.assertEqual(typeNode.childs[1].name, 'simple_type')

    # simpleTypeNode = mt.AltNode()
    # simpleTypeNode.childs.append(mt.ValueNode('bool'))
    # simpleTypeNode.childs.append(mt.ValueNode('int'))
    # simpleTypeNode.childs.append(mt.ValueNode('float'))
    # simpleTypeNode.childs.append(mt.ValueNode('string'))
    # simpleTypeNode.childs.append(mt.ValueNode('datetime'))
    # simpleTypeNode.childs.append(mt.ValueNode('tag'))
    # simpleTypeNode.childs.append(mt.ValueNode('event'))
    # simpleTypeNode.childs.append(mt.ValueNode('name'))

    # arrayTypeNode = [mt.NamedNode('array_type'), mt.ValueNode('['), mt.ValueNode(']')]

    # simpleTypeNode.childs.append(mt.ValueNode(''))
