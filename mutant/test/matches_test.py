from mutant import matches
from mutant import common
from mutant import grammar
import unittest


class MatchesTest(unittest.TestCase):

  def testQuantNode(self):
    pass

  def testAltNode(self):
    tokens = [common.Token(0, 'int', wordtype = 'int')]
    altNode = matches.AltNode()
    altNode.childs.append(matches.ValueNode('bool'))
    altNode.childs.append(matches.ValueNode('int'))
    altNode.childs.append(matches.ValueNode('string'))
    match = altNode.match(0, 0, common.Source('test.mut', 1, [], tokens))
    self.assertIsNotNone(match)
    self.assertEqual(match.leftIndex, 0)
    self.assertEqual(match.rightIndex, 0)

  def testParamNode(self):
    tokens = [common.Token(0, 'App', wordtype = 'name')]
    paramNode = matches.ParamNode('name')
    # raise Exception(paramNode.childs[0])
    self.assertEqual(len(paramNode.childs), 0)
    paramNode.childs.append(matches.ValueNode('name'))
    self.assertEqual(len(paramNode.childs), 1)
    match = paramNode.match(0, 0, common.Source('test.mut', 1, [], tokens))
    self.assertIsNotNone(match)
    self.assertEqual(match.leftIndex, 0)
    self.assertEqual(match.rightIndex, 0)
    self.assertEqual(len(match.params), 1)
    self.assertIn('name', match.params)
    namedToken = match.params['name'][0]
    self.assertEqual(namedToken.word, 'App')

  def testHandleNode(self):
    grammar.handlers['test_handler'] = self.handlerTest
    tokens = [common.Token(0, 'var', wordtype = 'var')]
    handleNode = matches.HandleNode('test_handler')
    match = handleNode.match(0, 0, common.Source('test.mut', 1, [], tokens))
    self.assertIsNotNone(match)
    self.assertEqual(match.leftIndex, 0)
    self.assertEqual(match.rightIndex, 0)
  def handlerTest(self, leftIndex, rightIndex, source):
    return matches.Match(leftIndex, rightIndex)

  def testNamedNode(self):
    tokens = [common.Token(0, 'int', wordtype = 'int')]
    namedNode = matches.NamedNode('simple_type')
    match = namedNode.match(0, 0, common.Source('test.mut', 1, [], tokens))
    self.assertIsNotNone(match)
    self.assertEqual(match.leftIndex, 0)
    self.assertEqual(match.rightIndex, 0)

  def testValueNode(self):
    tokens = [common.Token(0, 'value', wordtype = 'name')]
    valueNode = matches.ValueNode('name')
    match = valueNode.match(0, 0, common.Source('test.mut', 1, [], tokens))
    self.assertIsNotNone(match)
    self.assertEqual(match.leftIndex, 0)
    self.assertEqual(match.rightIndex, 0)
