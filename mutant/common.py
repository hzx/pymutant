
"""
Source - represent source file,
skiplines - line numbers with import and comments skip for parsing.
"""
class Source:
  def __init__(self, filename, lines, skiplines):
    self.filename = filename
    self.lines = lines
    self.skiplines = skiplines

"""
Language word.
"""
class Token:
  def __init__(self, source, linenum, word, wordtype = None):
    self.source = source
    self.linenum = linenum
    self.word = word
    self.wordtype = wordtype
