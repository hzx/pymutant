#import tornado.options
#from tornado.options import options
import sys
import os.path
from mutant.grammarparser import GrammarParser
from mutant.loader import Loader
from mutant.lexer import Lexer
from mutant.parser import Parser
from mutant.generators import GenFactory


class Compiler:
  """
  To compiler give main filename
  preprocessor - create source file table
  lexer - create token table, ignore comments here
  parser - analyze grammar, create tree
  gen and formatter - generate destination level sources
  """

  def __init__(self):
    self.grammarparser = GrammarParser()
    self.loader = Loader()
    self.lexer = Lexer()
    self.parser = Parser()
    self.genfactory = GenFactory()

  def setPaths(self, srcPaths, destPath):
    self.loader.setPaths(srcPaths)
    self.destPath = destPath

  def mutate(self, mainmodule, genname):
    rules = self.grammarparser.getRules()
    gen = self.genfactory.createGen(genname)
    formatter = self.genfactory.createFormatter(genname)

    module = self.loader.loadModule(mainmodule)
    # TODO(dem) change to module structure
    self.lexer.parse(module)
    self.parser.parse(module, rules)
    desttree = gen.convert(srctree)
    destlines = formatter.convert(desttree)

    self.save(self.destPath, destlines)

  def save(self, filename, lines):
    with open(filename, 'w') as f:
      f.writelines(lines)

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
