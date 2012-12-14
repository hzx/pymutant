from mutant import core
from mutant import common
from mutant import errors
from mutant.counters import BracketChecker


class NameContext(object):

  def __init__(self, context):
    pass


class Parser(object):

  def __init__(self):
    self.bracketChecker = BracketChecker()

    self.firstOperators = ['+', '-']
    self.secondOperators = ['*', '/']
    self.thirdOperators = ['not']

    # compile rules

  def parse(self, tokens):
    self.bracketChecker.check(tokens)

  def handleVariable(self):
    # self.variables.append()
    pass

  def handleFunction(self):
    #self.functions.append()
    pass

  def handleEnum(self):
    # self.enums.append()
    pass

  def handleStruct(self):
    # self.structs.append()
    pass

  def handleClass(self):
    # self.classes.append()
    pass

  def handleSelectFrom(self):
    pass

  def handleSelectConcat(self):
    pass

  def handleTag(self):
    pass
