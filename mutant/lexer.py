from mutant import common
from mutant import grammar
from mutant import errors
import logging
import re
import sys

"""
Lexer create token table.
"""
class Lexer(object):
  def __init__(self):
    # compose and compile tokens regex
    tokens_re = [grammar.STRING_RE, grammar.IDENT_RE, grammar.FLOAT_RE, grammar.INT_RE] \
        + [re.escape(token) for token in grammar.SYMBOL_TOKENS]
    self.tokens_re = re.compile('|'.join(tokens_re))

    # compile alphabet regex
    self.alpha_re = re.compile(grammar.ALPHA_RE)

    # parsed results
    self.tokens = []

  def parse(self, sources):
    """
    sources is common.Source objects
    """
    # parse words in sources
    #for source in self.sources:
    #  self.parseSource(source)
    tokens = reduce(lambda x, y: x+y, map(self.parseSource, sources))

    # detect words type
    for token in self.tokens:
      token.wordtype = self.detectTokenType(token.word)
    #reduce(lambda x, y: x, map(self.detectTokenType, rawTokens))

    self.tokens = tokens

  def parseSource(self, source):
    tokens = []
    for linenum, line in enumerate(source.lines):
      if linenum in source.skiplines: continue
      # check alphabet
      for c in line:
        if self.alpha_re.search(c) == None:
          raise errors.UnknownSymbol('unknown symbol %s in file "%s", linenum "%d".' % (c, source.filename, linenum))

      # tokenize
      result = self.tokens_re.findall(line)
      if len(result) == 0: continue

      # add tokens
      for word in result:
        tokens.append(common.Token(source, linenum, word))

    return tokens

  def detectWordType(self, word):
    # check system symbols
    if word in grammar.SYMBOL_TOKENS:
      return word
    # check system tokens
    if word in grammar.SYSTEM_TOKENS:
      return word
    # check string
    if re.match(grammar.STRING_RE, word) != None:
      return grammar.STRING_TYPE
    # check identifier
    if re.match(grammar.IDENT_RE, word) != None:
      return grammar.IDENT_TYPE
    # check float
    if re.match(grammar.FLOAT_RE, word) != None:
      return grammar.FLOAT_TYPE
    # check int
    if re.match(grammar.INT_RE, word) != None:
      return grammar.INT_TYPE
    raise errors.UnknownToken('unknown token "%s"' % word)

if __name__ == "__main__":
  s1 = """
  class Application {
    (router, browser) {
    }

    port = 8000;

    render = () {
      var item := this.port;
      var wtf = "TODO(dem): need render reactive DOM";
      return <div style={ fontSize: "12px", backgroundColor: "#e7e7e7" }>
          <h1> "Hello HTML" </h1>
        </div>;
    }
  }
  """
  sources = [common.Source('test.mut', s1.split('\n'), [])]
  lexer = Lexer()
  lexer.parse(sources)
  for token in lexer.tokens:
    print "word: %s, wordtype: %s" % (token.word, token.wordtype)
