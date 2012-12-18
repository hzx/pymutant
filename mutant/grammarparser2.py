from mutant import grammar2 as grammar
from mutant import core
from mutant import matches
import re


class GrammarParser(object):

  def __init__(self):
    # for first stage - split source by tokens
    self.tokenfind_re = re.compile('\([^()]+\)(?:[?*+]|{[0-9,]+})|<[a-zA-Z_0-9]+>\([^()]+\)|(?:[^|\s]+[|]?)+|{[a-zA-Z_0-9]+}!?|[a-zA-Z_0-9]+|[()\[\]{};\:]')
    # check and extract data regexes from token
    self.quant_check_re = re.compile('\([^()]+\)(?:[?*+])')
    self.quant_quest_extract_re = re.compile('\(([^()]+)\)\?')
    self.quant_star_extract_re = re.compile('\(([^()`]+)(\`[^\`]+\`)?\)\*')
    self.quant_plus_extract_re = re.compile('\(([^()`]+)(\`[^\`]+\`)?\)\+')
    self.quant_curly_extract_re = re.compile('\(([^()`]+)(\`[^\`]+\`)?\)\{([0-9,]+)\}')
    self.quant_nums_extract_re = re.compile('([0-9]+)\,')
    self.alt_check_split_re = re.compile('\|')
    name_re = '[_a-zA-Z][_a-zA-Z]*'
    self.param_extract_re = re.compile('\<([_a-zA-Z0-9][_a-zA-Z0-9]*)\>\(([^()]+)\)')
    self.handle_check_extract_re = re.compile('\{(%s)\}\!' % name_re)
    self.named_check_extract_re = re.compile('\{(%s)\}' % name_re)
    self.value_check_re = re.compile('(%s)|([\(\)\[\]\{\}\<\>\=\:\;])|(\/\>)' % name_re)
    self.delim_extract_re = re.compile('\`([^`]+)\`')

  def compileGrammar(self):
    # store to this map compiled grammar
    grammar.compiled = {}

    for name, source in grammar.rules.items():
      grammar.compiled[name] = self.compileSource(source)

  def parseSource(self, source):
    return self.tokenfind_re.findall(source)

  def compileSource(self, source):
    # find tokens
    tokens = self.parseSource(source)
    # detect token type and create node
    return [self.createNode(token) for token in tokens]

  def createNode(self, token):
    # check param token
    match = self.param_extract_re.match(token)
    if match:
      name, value = match.groups()
      return self.createParamNode(name, value)

    # check quantify token
    if self.quant_check_re.match(token):
      return self.createQuantNode(token)
    
    # check alternate token
    result = self.alt_check_split_re.split(token)
    if len(result) > 1:
      return self.createAltNode(result)

    # check handled token
    match = self.handle_check_extract_re.match(token)
    if match:
      name = match.groups()[0]
      return self.createHandleNode(name)

    # check named token
    match = self.named_check_extract_re.match(token)
    if match:
      name = match.groups()[0]
      return self.createNamedNode(name)

    # value token
    match = self.value_check_re.match(token)
    if match:
      return self.createValueNode(token)

    raise Exception('unknown token type "%s"' % token)

  def createQuantNode(self, token):
    # check and extract quantify nodes types

    result = self.quant_quest_extract_re.match(token)
    if result:
      source = result.groups()[0]
      node = matches.QuantNode([0, 1])
      node.childs = self.compileSource(source)
      return node

    result = self.quant_star_extract_re.match(token)
    if result:
      source, litdelim = result.groups()
      node = matches.QuantNode([0])
      delimres = self.delim_extract_re.match(litdelim)
      if delimres:
        node.delim = delimres.groups()[0]
      node.childs = self.compileSource(source)
      return node
    
    result = self.quant_plus_extract_re.match(token)
    if result:
      source, litdelim = result.groups()
      node = matches.QuantNode([1])
      delimres = self.delim_extract_re.match(litdelim)
      if delimres:
        node.delim = delimres.groups()[0]
      node.childs = self.compileSource(source)
      return node

    result = self.quant_curly_extract_re.match(token)
    if result:
      source, litdelim, numstring = result.groups()
      # parse numstring
      numresult = self.quant_nums_extract_re.match(numstring)
      mincount = numresult.groups()[0]
      node = matches.QuantNode([mincount])
      delimres = self.delim_extract_re.match(litdelim)
      if delimres:
        node.delim = delimres.groups()[0]
      node.childs = self.compileSource(source)
      return node

    raise Exception('unknown quant token "%s"' % token)

  def createAltNode(self, sources):
    node = matches.AltNode()
    childs = []
    for source in sources:
      nodes = self.compileSource(source)
      childs.append(nodes[0])
    node.childs = childs
    return node

  def createParamNode(self, name, source):
    node = matches.ParamNode(name)
    node.childs = self.compileSource(source)
    return node

  def createHandleNode(self, name):
    node = matches.HandleNode(name)
    return node

  def createNamedNode(self, name):
    node = matches.NamedNode(name)
    return node

  def createValueNode(self, value):
    node = matches.ValueNode(value)
    return node
