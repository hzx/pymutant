import tornado.options
from tornado.options import options

from mutant.preprocess import Preprocessor
from mutant.lexer import Lexer
from mutant.parser import Parser
from mutant.generators import GENERATORS

VAR_INDEX = 0

"""
To compiler give main filename
preprocess - create source file table
tokenize - create token table, ignore comments here
parse - analyze grammar, create tree
translate - generate destination level sources
"""
class Compiler:
  preprocessor = Preprocessor()
  lexer = Lexer()
  parser = Parser()

  # tokens index map - for faster analyze
  tokenMap = {}
  
  def __init__(self):
    # generate tokenMap
    for index in range(0,  len(TOKENS)):
      tokenMap[TOKENS[index]] = index

  def initialize(self, filename):
    filenamePath = os.path.abspath(os.path.normpath(filename))

  # remove comments
  def preprocess(self, lines):
    for line in lines:


  def tokenize(self, filename):
    lines = readlines(filename)

    # find lexemes and create lexemes array
    # parse lexemes array and set token type (from table)

  def parse(self):
    # need identifiers table
    # from lexemes and its token type create lexems tree

if __name__ == "__main__":
  tornado.options.parse_command_line()
  parser = Parser()
  parser.tokenize(options.mut)
