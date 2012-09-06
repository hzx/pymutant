#import tornado.options
#from tornado.options import options
import sys

from mutant.preprocessor import Preprocessor
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
  def __init__(self):
    self.preprocessor = Preprocessor()
    self.lexer = Lexer()
    self.parser = Parser()

  def mutate(self, destination, source):
    self.preprocessor.parse(source)
    #self.lexer

def main():
  #tornado.options.parse_command_line()
  if len(sys.argv) != 3:
    print "Compiler accept: destination source"
    return

  destination = sys.argv[1]
  source = sys.argv[2]

  compiler = Compiler()
  compiler.mutate(destination, source)

if __name__ == "__main__":
  main()
