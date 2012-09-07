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

class GenError(Error):
  """Generator base error."""
  pass
