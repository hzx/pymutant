from mutant import core
from mutant import common
from mutant.generators import GenFactory


class Parser(object):

  def __init__(self):
    self.genFactory = GenFactory()

    self.vars = []
    self.functions = []
    self.enums = []
    self.structs = []
    self.classes = []

  def parse(self, tokens):
    pass
