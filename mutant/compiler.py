from mutant.grammarparser import GrammarParser
from mutant.loader import Loader
from mutant.lexer import Lexer
from mutant.parser import Parser
from mutant.checker import Checker
from mutant.generators import GenFactory


class Compiler(object):

  def __init__(self):
    self.grammarParser = GrammarParser()
    self.loader = Loader()
    self.lexer = Lexer()
    self.parser = Parser()
    self.checker = Checker()

    self.genFactory = GenFactory()

    # compile grammar rules
    self.grammarParser.compileGrammar()

  def compile(self, srcPaths, moduleName):
    """
    Create mutant lang source code tree.
    Load module and all referenced modules.
    Tokenize and parse source code.
    Always cache modules by moduleName (import name).
    output:
      module - common.Module instance.
    """
    self.loader.setPaths(srcPaths)

    # loader, lexer and parser all change module object
    mainModule = self.loader.loadModule(moduleName)

    # parse each module in lexer.modules cache
    for name, module in self.loader.modules.items():
      self.lexer.parse(module)
      self.parser.parse(module)

    for module in self.loader.modules:
      self.checker.check(module)

    return mainModule

  def mutate(self, module, destPath, genName):
    """
    Translate module and referenced modules to genName
    language modules.
    Create generated module sources formatted.
    Save generated sources to disk.
    """
    gen = self.genFactory.createGen(genName)

  def save(self, filename, lines):
    with open(filename, 'w') as f:
      f.writelines(lines)
