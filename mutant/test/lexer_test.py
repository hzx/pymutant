import unittest
from mutant.lexer import Lexer
from mutant.common import Source, Module
from mutant import grammar as gr
import re


class LexerTest(unittest.TestCase):

  def setUp(self):
    self.lexer = Lexer()
    self.lines_re = re.compile('\n')

  def tokensToWords(self, tokens):
    return [token.word for token in tokens]

  def tokensToWordtypes(self, tokens):
    return [token.wordtype for token in tokens]

  def checkWordsWordtypes(self, code, expectedWords, expectedWordtypes):
    lines = self.lines_re.split(code)
    source = Source('test.mut', lines, [])
    self.assertEqual(source.tokens, None)

    self.lexer.parseSource(source)

    actualWords = self.tokensToWords(source.tokens)
    actualWordtypes = self.tokensToWordtypes(source.tokens)

    self.assertListEqual(actualWords, expectedWords)
    self.assertListEqual(actualWordtypes, expectedWordtypes)

  def testParseSource(self):
    data = [
          # Variable
          [
              """
              bool flag = true;
              """,
              ['bool', 'flag', '=', 'true', ';'],
              ['bool', 'name', '=', 'true', ';'],
              ],
          [
              """
              int num = 32;
              """,
              ['int', 'num', '=', '32', ';'],
              ['int', 'name', '=', 'litint', ';'],
              ],
          [
              """
              float num = 32.54;
              """,
              ['float', 'num', '=', '32.54', ';'],
              ['float', 'name', '=', 'litfloat', ';'],
              ],
          [
              """
              string label = 'User label';
              """,
              ['string', 'label', '=', "'User label'", ';'],
              ['string', 'name', '=', 'litstring', ';'],
              ],
          [
              """
              App app = App();
              """,
              ['App', 'app', '=', 'App', '(', ')', ';'],
              ['name', 'name', '=', 'name', '(', ')', ';'],
              ],
          [
              """
              tasker.App app = App();
              """,
              ['tasker', '.', 'App', 'app', '=', 'App', '(', ')', ';'],
              ['name', '.', 'name', 'name', '=', 'name', '(', ')', ';'],
              ],
          # Select from
          [
              """
              var openMessages = select from messages where status is TaskStatus.OPEN;
              """,
              ['var', 'openMessages', '=', 'select', 'from', 'messages',
                  'where', 'status', 'is', 'TaskStatus', '.', 'OPEN', ';'],
              ['var', 'name', '=', 'select', 'from', 'name', 'where', 'name',
                  'is', 'name', '.', 'name', ';'],
              ],
          # Select concat
          [
              """
              var messages = select concat newMessages, openMessages;
              """,
              ['var', 'messages', '=', 'select', 'concat', 'newMessages', ',',
                  'openMessages', ';'],
              ['var', 'name', '=', 'select', 'concat', 'name', ',', 'name', ';'],
              ],
          # Tag
          [
              """
              tag content = <div class=['item', 'foo']></div>;
              """,
              ['tag', 'content', '=', '<', 'div', 'class', '=', '[', "'item'",
              ',', "'foo'", ']', '>', '</', 'div', '>', ';'],
              ['tag', 'name', '=', '<', 'name', 'class', '=', '[', 'litstring', ',',
                  'litstring', ']', '>', '</', 'name', '>', ';'],
              ],
          # Function
          [
              """
              int main() {
                return 0;
              }
              """,
              ['int', 'main', '(', ')', '{', 'return', '0', ';', '}'],
              ['int', 'name', '(', ')', '{', 'return', 'litint', ';', '}'],
              ],
          [
              """
              (string[] messages) {
                map(messages, renderMessage);
              }
              """,
              ['(', 'string', '[', ']', 'messages', ')', '{', 'map', '(',
                  'messages', ',', 'renderMessage', ')', ';', '}'],
              ['(', 'string', '[', ']', 'name', ')', '{', 'map', '(', 'name', ',',
                  'name', ')', ';', '}'],
              ],
          # Enum
          [
              """
              enum TaskStatus {
                NEW = 1;
                OPEN = 2;
              }
              """,
              ['enum', 'TaskStatus', '{', 'NEW', '=', '1', ';', 'OPEN', '=',
                  '2', ';', '}'],
              ['enum', 'name', '{', 'name', '=', 'litint', ';', 'name', '=',
                  'litint', ';', '}'],
              ],
          # Struct
          [
              """
              struct Task {
                string id;
                string name;
              }
              """,
              ['struct', 'Task', '{', 'string', 'id', ';', 'string', 'name',
                  ';', '}'],
              ['struct', 'name', '{', 'string', 'name', ';', 'string', 'name',
                  ';', '}'],
              ],
          # Class
          [
              """
              class App {
                () {
                }
              }
              """,
              ['class', 'App', '{', '(', ')', '{', '}', '}'],
              ['class', 'name', '{', '(', ')', '{', '}', '}'],
              ],
        ]

    for code, expectedWords, expectedWordtypes in data:
      self.checkWordsWordtypes(code, expectedWords, expectedWordtypes)
