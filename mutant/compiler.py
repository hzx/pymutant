from mutant.grammarparser import GrammarParser
from mutant.loader import Loader
from mutant.lexer import Lexer
from mutant.parser import Parser
from mutant.checker import Checker
from mutant.generators import GenFactory
import re


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

    self.dotre = re.compile('\.')

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

    # check and set functioncall as constructor
    for name, module in self.loader.modules.items():
      self.markConstructors(module)

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

  def markConstructors(self, module):
    """
    Find and mark constructor among functioncall nodes
    """
    # find in variables body
    for name, va in module.variables.items():
      self.markConstructorInVariable(module, va)

    # find in functions
    for name, fn in module.functions.items():
      self.markConstructorInNodes(module, fn.bodyNodes)

    for cn, cl in module.classes.items():
      # find in class variables body
      for name, va in cl.variables.items():
        self.markConstructorInVariable(module, va)

      # find in class functions variables body
      for name, fn in cl.functions.items():
        self.markConstructorInNodes(module, fn.bodyNodes)

  def markConstructorInVariable(self, module, va):
    if va.body and (va.body.nodetype == 'functioncall'):
      self.markConstructorFunctioncall(module, va.body)

  def markConstructorFunctioncall(self, module, fc):
    if self.isClassName(module, fc.name):
      fc.isConstructorCall = True
    # mark constructor in params
    for node in fc.params:
      if node.nodetype == 'functioncall':
        self.markConstructorFunctioncall(module, node)

  def markConstructorInNodes(self, module, nodes):
    for node in nodes:
      if (node.nodetype == 'variable') and node.body:
        if node.body.nodetype == 'functioncall':
          self.markConstructorFunctioncall(module, node.body)
      elif (node.nodetype == 'value') and node.body and (node.body.nodetype == 'functioncall'):
        self.markConstructorFunctioncall(module, node.body)
      elif node.nodetype == 'return':
        if node.body.nodetype == 'functioncall':
          self.markConstructorFunctioncall(module, node.body)
      elif node.nodetype == 'if':
        if node.body: self.markConstructorInNodes(module, node.body)
        if node.elseBody: self.markConstructorInNodes(node.elseBody)

  def isClassName(self, module, name):
    """
    Find name among struct and class names, and aliased modules
    """
    # search in classes
    if module.classes.has_key(name):
      return True
    # check if name consistent
    res = self.dotre.split(name)
    if len(res) > 1:
      moduleName = res[0]
      className = res[1]
      # search in modules
      if module.modules.has_key(moduleName):
        mod = module.modules[moduleName]
        # search in module classes
        # debug - search in module structs
        if mod.structs.has_key(className):
          return True
        if mod.classes.has_key(className):
          return True
    return False
