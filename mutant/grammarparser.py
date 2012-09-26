'''
Grammar consist of words, alternatives, sentences
'''


import re
from mutant import grammar as gr

class NodeParser(object):

  def __init__(self):
    pass

class AltNodeParser(NodeParser):
  """|"""

  def __init__(self):
    pass

class QuantNodeParser(NodeParser):
  """"""

  def __init__(self):
    pass

IDENT_RE = ''
QUANT_RE = ''
ALT_RE = ''
TOKENS_RE = '\([^)(]+\)(?:[*?+]|{[^}]+[}])|(?:[{]?[\w\d.]+[}]?[|]?)+|\(|\)|\[|\]|\{|\}|\=|\;|\*|</|/>|<|>'

class GrammarParser(object):
  """
  Parse grammar and create corresponding parsing classes.
  """

  def __init__(self):
    # create source grammar map by name
    self.source = {
        gr.TYPE_NAME: gr.TYPE,
        gr.CALLFUNC_NAME: gr.CALLFUNC,
        gr.EXPRESSION_NAME: gr.EXPRESSION,
        gr.VARDECLARE_NAME: gr.VARDECLARE,
        gr.VARASSIGN_NAME: gr.VARASSIGN,
        gr.PARAMS_NAME: gr.PARAMS,
        gr.CALLPARAMS_NAME: gr.CALLPARAMS,
        gr.FUNCTION_NAME: gr.FUNCTION,
        gr.ENUM_NAME: gr.ENUM,
        gr.STRUCT_NAME: gr.STRUCT,
        gr.CONSTRUCTOR_NAME: gr.CONSTRUCTOR,
        gr.CLASS_NAME: gr.CLASS,
        gr.SELECTFROM_NAME: gr.SELECTFROM,
        gr.CONCATPARAMS_NAME: gr.CONCATPARAMS,
        gr.SELECTCONCAT_NAME: gr.SELECTCONCAT,
        gr.TAGATTRS_NAME: gr.TAGATTRS,
        gr.TAG_NAME: gr.TAG,
        gr.SINGLETAG_NAME: gr.SINGLETAG,
        }

    # parsed grammar map by name
    self.grammar = {}

    self.tokens_re = re.compile(TOKENS_RE)

  def parseSource(self, source):
    return self.tokens_re.findall(source)
