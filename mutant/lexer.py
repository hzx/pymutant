from mutant import common
from mutant import grammar
import re
from exceptions import Exception

"""
Lexer create token table.
"""
class Lexer:
  def __init__(self):
    tokens_re = [grammar.STRING_RE, grammar.IDENT_RE, grammar.DIGIT_RE] \
        + [re.escape(token) for token in grammar.SYMBOL_TOKENS]
    self.tokens_re = re.compile('|'.join(tokens_re))
    self.tokens = []

  def parse(self, sources):
    """
    sources is common.Source objects
    """
    for source in sources:
      for linenum, line in enumerate(source.lines):
        if linenum in source.skiplines: continue
        # check alphabet
        for c in line:
          if grammar.ALPHA_RE.search(c) == None:
            raise Exception('Lexer: unknown symbol %s in file "%s", linenum "%d".' % (c, source.filename, linenum))

        # tokenize
        result = self.tokens_re.findall(line)
        if len(result) == 0: continue

        # add tokens
        for word in result:
          self.tokens.append(common.Token(source, linenum, word))

    # detect tokens type
    for token in self.tokens:
      # check system symbols
      if token.word in grammar.SYMBOL_TOKENS:
        token.wordtype = token.word
        continue
      # check system tokens
      if token.word in grammar.SYSTEM_TOKENS:
        token.wordtype = token.word
        continue
      # check string
      if re.match(grammar.STRING_RE, token.word) != None:
        token.wordtype = grammar.STRING_TYPE
        continue
      # check identifier
      if re.match(grammar.IDENT_RE, token.word) != None:
        token.wordtype = grammar.IDENT_TYPE
        continue
      # check digit
      if re.match(grammar.DIGIT_RE, token.word) != None:
        token.wordtype = grammar.DIGIT_TYPE
        continue
      raise Exception('unknown token "%s"' % token.word)

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
