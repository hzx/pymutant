from exceptions import Exception


class Error(Exception):
  """Mutant base error."""
  pass

class LexerError(Error):
  """Lexer base error."""
  pass

class UnknownSymbol(LexerError):
  pass

class UnknownToken(LexerError):
  pass

class ParserError(Error):
  """Parser base error."""
  pass

class RoundBracketError(ParserError):
  '''Match pair round bracket'''

  def __init__(self, filename):
    Exception.__init__(self, 'round bracket not match, "%s"' % filename)

class SquareBracketError(ParserError):
  '''Match pair square bracket'''

  def __init__(self, filename):
    Exception.__init__(self, 'square bracket not match "%s"' % filename)

class CurlyBracketError(ParserError):
  '''Match pair curly bracket'''

  def __init__(self, filename):
    Exception.__init__(self, 'curly bracket not match "%s"' % filename)

class GenError(Error):
  """Generator base error."""
  pass
