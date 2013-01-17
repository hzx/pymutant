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

    self.compiledModules = {}

  def compile(self, srcPaths, moduleName):
    """
    Create mutant lang source code tree.
    Load module and all referenced modules.
    Tokenize and parse source code.
    Always cache modules by moduleName (import name).
    output:
      module - common.Module instance.
    """
    # check if moduleName already compiled
    if moduleName in self.compiledModules:
      return self.compiledModules[moduleName]

    self.loader.setPaths(srcPaths)

    # loader, lexer and parser all change module object
    mainModule = self.loader.loadModule(moduleName)

    # parse each module in lexer.modules cache
    for name, module in self.loader.modules.items():
      # check cache
      if name in self.compiledModules:
        continue
      self.lexer.parse(module)
      self.parser.parse(module)

    # check and add module to cache
    for name, module in self.loader.modules.items():
      self.checker.check(module)
      self.compiledModules[name] = module

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

  def clearModule(self, module):
    cleared = common.Module(module.name, [])

    # variables
    for key, node in module.variables.items():
      var = self.clearVariable(node)
      cleared.variables[var.name] = var

    # functions
    for key, node in module.functions.items():
      func = self.clearFunction(node)
      cleared.functions[func.name] = func

    # enums
    for key, node in module.enums.items():
      en = self.clearEnum(node)
      cleared.enums[en.name] = en

    # structs
    for key, node in module.classes.items():
      st = self.clearStruct(node)
      cleared.structs[st.name] = st

    # classes
    for key, node in module.classes.items():
      cl = self.clearClass(node)
      cleared.classes[cl.name] = cl


  def clearVariable(self, var):
    pass

  def clearFunction(self, func):
    pass

  def clearEnum(self, en):
    pass

  def clearStruct(self, st):
    pass

  def clearClass(self, cl):
    pass

