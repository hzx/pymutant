from mutant import common
from mutant import grammar as gr
from mutant import errors
import re
import sys

class Lexer(object):
  """
  Lexer create token table.
  """

  def __init__(self):
    # compose and compile tokens regex
    tokens_re = [gr.LITSTRING_RE, gr.NAME_RE, gr.LITFLOAT_RE, gr.LITINT_RE] \
        + [re.escape(token) for token in gr.SYMBOL_TOKENS]
    self.tokens_re = re.compile('|'.join(tokens_re))

    # compile alphabet regex
    self.alpha_re = re.compile(gr.ALPHA_RE)

    # parsed results
    self.tokens = []

  def parse(self, module):
    """
    module - main module
    """
    # parse words in sources
    for source in module.sources:
      self.parseSource(source)

  def parseSource(self, source):
    tokens = []

    for linenum, line in enumerate(source.lines):
      if linenum in source.skiplines: continue

      # check alphabet
      for c in line:
        if self.alpha_re.search(c) == None:
          raise errors.UnknownSymbol('unknown symbol "%s" in file "%s", linenum "%d".' % (c, source.filename, linenum))

      # tokenize
      result = self.tokens_re.findall(line)
      if len(result) == 0: continue

      # add tokens
      for word in result:
        tokens.append(common.Token(linenum, word, self.detectWordType(word)))

    source.tokens = tokens

  def detectWordType(self, word):
    # check system symbols
    if word in gr.SYMBOL_TOKENS:
      return word
    # check system tokens
    if word in gr.SYSTEM_TOKENS:
      return word
    # check string literal
    if re.match(gr.LITSTRING_RE, word) != None:
      return gr.LITSTRING_TYPE
    # check name
    if re.match(gr.NAME_RE, word) != None:
      return gr.NAME_TYPE
    # check float literal
    if re.match(gr.LITFLOAT_RE, word) != None:
      return gr.LITFLOAT_TYPE
    # check int literal
    if re.match(gr.LITINT_RE, word) != None:
      return gr.LITINT_TYPE
    raise errors.UnknownToken('unknown token "%s"' % word)
