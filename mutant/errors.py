from exceptions import Exception


class Error(Exception):
  """Mutant base error."""
  pass

class PathNotFound(Error):

  def __init__(self, path):
    Exception.__init__(self, 'Path not found, %s', path)

class ModuleNotFound(Error):

  def __init__(self, name, referer=None):
    if referer != None:
      Exception.__init__(self, 'Module not found "%s", referer "%s"' %
          (name, referer))
    else:
      Exception.__init__(self, 'Module not found "%s"' % name)

class UnknownSymbol(Error):
  pass

class UnknownToken(Error):
  pass

class RoundBracketError(Error):
  '''Match pair round bracket'''

  def __init__(self, filename):
    Exception.__init__(self, 'round bracket not match, "%s"' % filename)

class SquareBracketError(Error):
  '''Match pair square bracket'''

  def __init__(self, filename):
    Exception.__init__(self, 'square bracket not match "%s"' % filename)

class CurlyBracketError(Error):
  '''Match pair curly bracket'''

  def __init__(self, filename):
    Exception.__init__(self, 'curly bracket not match "%s"' % filename)
