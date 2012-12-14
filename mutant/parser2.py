from mutant import core2 as core
from mutant import grammar2 as grammar
from mutant.counters import BracketCounter, TagBracketCounter
from mutant.common import getTokensRange
from mutant.matches import Match, mergeMatches, matchNodes, tokensToString, findWordIndex


class Parser(object):
  
  def __init__(self):
    self.bracketCounter = BracketCounter()

    self.bindHandlers()

    self.moduleNodeMap = {
        'variable': self.addModuleVariable,
        'function': self.addModuleFunction,
        'enum': self.addModuleEnum,
        'struct': self.addModuleStruct,
        'class': self.addModuleClass
        }

  def parse(self, module):
    """
    Parse one module at time.
    """
    # set current module for parse
    self.module = module

    # parse every source in module
    for source in module.sources:
      self.parseSource(source)

  def addModuleNodes(self, nodes, module):
    for node in nodes:
      func = self.moduleNodeMap[node.nodetype]
      func(module, node)

  def addModuleVariable(self, module, var):
    module.variables[var.name] = var
  def addModuleFunction(self, module, func):
    module.functions[func.name] = func
  def addModuleEnum(self, module, en):
    module.enums[en.name] = en
  def addModuleStruct(self, module, st):
    module.structs[st.name] = st
  def addModuleClass(self, module, cl):
    module.classes[cl.name] = cl

  def parseSource(self, source):
    """
    Parse source with global rules.
    """
    leftIndex = 0
    rightIndex = len(source.tokens)-1

    self.bracketCounter.check(leftIndex, rightIndex, source)

    # parse with global grammar rules
    nodes = self.parseByRules(grammar.global_rules, leftIndex, rightIndex, source)

    self.addModuleNodes(nodes, self.module)

    # TODO(dem) check source fully parsed

  def parseByRules(self, ruleNames, leftIndex, rightIndex, source):
    """
    Parse tokens by rules.
    Call handler with match.
    Return Match object if match rules, else - None.
    Parse from left to right direction, move cursor from leftIndex
      to rightIndex.
    """
    cursor = leftIndex
    # raise Exception('leftIndex = %d, rightIndex = %d' % (leftIndex, rightIndex))
    nodes = []
    while True:
      ruleFound = False
      for ruleName in ruleNames:
        rule = grammar.getRule(ruleName)
        match = matchNodes(rule, cursor, rightIndex, source)
        if match:
          # handler name = global rule name
          handler = grammar.getHandler(ruleName)
          node = handler(match, source)
          nodes.append(node)
          cursor = match.rightIndex + 1
          ruleFound = True
          break
      # check if all tokens parsed
      if cursor > rightIndex: return nodes
      if ruleFound: continue
      raise Exception('No rule found in "%s" source' % (source.filename))

  def bindHandlers(self):
    """
    Bind grammar.handlers map to self.handle*.
    """
    # bind global handlers
    grammar.setHandler('define', self.handleDefine)
    grammar.setHandler('variable', self.handleVariable)
    grammar.setHandler('function', self.handleFunction)
    grammar.setHandler('enum', self.handleEnum)
    grammar.setHandler('struct', self.handleStruct)
    grammar.setHandler('class', self.handleClass)

    grammar.setHandler('expression_body', self.handleExpression)
    grammar.setHandler('expression', self.parseExpression)

    grammar.setHandler('variable_body', self.handleVariableBody)

    grammar.setHandler('function_params', self.handleFunctionParams)
    grammar.setHandler('function_body', self.handleFunctionBody)

    grammar.setHandler('enum_body', self.handleEnumBody)

    grammar.setHandler('struct_body', self.handleStructBody)

    grammar.setHandler('class_body', self.handleClassBody)

    grammar.setHandler('tag', self.handleTag)

    # bind parsers
    grammar.setHandler('parseVariableBody', self.parseVariableBody)
    grammar.setHandler('parseFunctionParams', self.parseFunctionParams)
    grammar.setHandler('parseFunctionBody', self.parseFunctionBody)
    grammar.setHandler('parseEnumBody', self.parseEnumBody)
    grammar.setHandler('parseStructBody', self.parseStructBody)
    grammar.setHandler('parseClassBody', self.parseClassBody)
    grammar.setHandler('parseTag', self.parseTag)

  def runHandlers(self, obj, handlers, source):
    for handlerName, handlerMatch in handlers.items():
      handler = grammar.getHandler(handlerName)
      handler(obj, handlerMatch.leftIndex, handlerMatch.rightIndex, source)

  # Grammar handlers

  def handleImport(self, match, source):
    """
    FOR NOW NOT USED, IMPORT PROCESS BY LOADER.
    Import module.
    """
    raise Exception('handleImport not implemented')

  def handleDefine(self, match, source):
    """
    Add type alias.
    """
    raise Exception('handleDefine not implemented')

  def handleVariable(self, match, source):
    """
    Create core.VariableNode.
    """
    name = match.params['name'][0].word
    decltype = match.params['type']
    var = core.VariableNode(decltype, name)
    
    self.runHandlers(var, match.handlers, source)

    return var

  def handleFunction(self, match, source):
    """
    Create core.FunctionNode.
    """
    name = match.params['name'][0].word
    decltype = match.params['type']
    func = core.FunctionNode(decltype, name)

    self.runHandlers(func, match.handlers, source)

    return func

  def handleEnum(self, match, source):
    """
    Create core.EnumNode.
    """
    name = match.params['name'][0].word
    en = core.EnumNode(name)

    self.runHandlers(en, match.handlers, source)
  
    return en

  def handleStruct(self, match, source):
    """
    Create core.StructNode.
    """
    name = match.params['name'][0].word
    baseName = match.params.get('base_name', None)
    st = core.StructNode(name, baseName)

    self.runHandlers(st, match.handlers, source)

    return st

  def handleClass(self, match, source):
    """
    Create core.ClassNode.
    """
    name = match.params['name'][0].word
    baseName = match.params.get('base_name', None)
    cl = core.ClassNode(name, baseName)

    self.runHandlers(cl, match.handlers, source)

    return cl

  # OTHER RULES

  def handleSelectFrom(self, match, source):
    """
    Create core.SelectFromNode.
    """
    raise Exception('handleSelectFrom not implemented')

  def handleSelectConcat(self, match, source):
    """
    Create core.SelectConcatNode.
    """
    raise Exception('handleSelectConcat not implemented')

  def handleTag(self, match, source):
    """
    Create core.TagNode.
    """
    raise Exception('handleTag not implemented')

  def handleVariableBody(self, leftIndex, rightIndex, source):
    """
    Search ; and if found any symbol before = return None.
    """
    equalFound = False
    for num, token in getTokensRange(leftIndex, rightIndex, source.tokens):
      if token.word == ';':
        match = Match(leftIndex, num)
        match.handlers['parseVariableBody'] = Match(match.leftIndex, match.rightIndex)
        return match
      if token.word == '=':
        equalFound = True
        continue
      if not equalFound:
        return None
    return None

  def handleFunctionParams(self, leftIndex, rightIndex, source):
    if source.tokens[leftIndex].word == '(':
      bracketCounter = BracketCounter()
      match = bracketCounter.findPair(leftIndex, rightIndex, source)
      match.handlers['parseFunctionParams'] = Match(match.leftIndex, match.rightIndex)
      return match
    return None

  def handleFunctionBody(self, leftIndex, rightIndex, source):
    if source.tokens[leftIndex].word == '{':
      bracketCounter = BracketCounter()
      match = bracketCounter.findPair(leftIndex, rightIndex, source)
      match.handlers['parseFunctionBody'] = Match(match.leftIndex, match.rightIndex)
      return match
    return None

  def handleEnumBody(self, leftIndex, rightIndex, source):
    if source.tokens[leftIndex].word == '{':
      bracketCounter = BracketCounter()
      match = bracketCounter.findPair(leftIndex, rightIndex, source)
      match.handlers['parseEnumBody'] = Match(match.leftIndex+1, match.rightIndex-1)
      return match
    return None

  def handleStructBody(self, leftIndex, rightIndex, source):
    if source.tokens[leftIndex].word == '{':
      bracketCounter = BracketCounter()
      match = bracketCounter.findPair(leftIndex, rightIndex, source)
      match.handlers['parseStructBody'] = Match(match.leftIndex+1, match.rightIndex-1)
      return match
    return None

  def handleClassBody(self, leftIndex, rightIndex, source):
    if source.tokens[leftIndex].word == '{':
      bracketCounter = BracketCounter()
      match = bracketCounter.findPair(leftIndex, rightIndex, source)
      match.handlers['parseClassBody'] = Match(match.leftIndex+1, match.rightIndex-1)
      return match
    return None

  def handleConstructorInit(self, leftIndex, rightIndex, source):
    if source.tokens[leftIndex].word == '{':
      # find ;
      semicolonIndex = findWordIndex(';', leftIndex, rightIndex, source)
      if semicolonIndex >= 0:
        match = Match(leftIndex, semicolonIndex)
        # left = '{' + 1, right = '}' ';' - 2
        match.handlers['parseConstructorInit'] = Match(leftIndex+1, semicolonIndex-2)
        return match
    return None

  def handleTag(self, leftIndex, rightIndex, source):
    # check first bymbol < and last symbol /> or >
    cursorRight = rightIndex
    if source.tokens[leftIndex].word == '<':
      if source.tokens[cursorRight].word == ';':
        cursorRight = rightIndex - 1
      if source.tokens[cursorRight].word in ['/>', '>']:
        match = Match(leftIndex, rightIndex)
        match.handlers['parseTag'] = Match(leftIndex, cursorRight)
        return match
    return None

  def handleExpression(self, match, source):
    rightCursor = match.rightIndex

    # tokens may contain ; search new rightCursor
    semicolonIndex = findWordIndex(';', match.leftIndex, match.rightIndex, source.tokens)
    if semicolonIndex >= 0: rightCursor = semicolonIndex - 1

    node = self.parseExpression(match.leftIndex, rightCursor, source)

    return node

  # PARSE

  def parseExpression(self, leftIndex, rightIndex, source):
    """
    Create tree.
    Return rootNode. 
    """
    # raise Exception('parseExpression not implemented')


    funcCallRule = grammar.getRule('function_call')
    
    # set nodes weights

    # set nodes weights with brackets

    # create tree
    return Match(leftIndex, rightIndex)

  def parseVariableBody(self, var, leftIndex, rightIndex, source):
    rightCursor = rightIndex
    # if end with ; then move to left
    if source.tokens[rightIndex].word == ';': rightCursor = rightIndex - 1

    nodes = self.parseByRules(grammar.variable_body_rules, leftIndex, rightIndex, source)

    if len(nodes) > 1: raise Exception('parse error: variable body must have one or zero body node')

    if len(nodes) == 1:
      var.setBody(nodes[0])

  def parseFunctionParams(self, func, leftIndex, rightIndex, source):
    # check if hot have params
    if (rightIndex - leftIndex) == 1: return

    # move leftIndex to right from (
    cursor = leftIndex + 1
    # move rightIndex to left from )
    rightCursor = rightIndex - 1
    paramRule = grammar.getRule('function_param')
    while True:
      # parse by param rule
      match = matchNodes(paramRule, cursor, rightCursor, source)
      if match == None:
        raise Exception('not parse function params, source "%s", linenum "%d"' % (source.filename, source.tokens[leftIndex].linenum))
      # move cursor from match.rightIndex to next and after comma
      cursor = match.rightIndex + 2
      # add parameter to function
      paramName = match.params['name'][0].word
      paramType = match.params['type']
      func.addParameter(paramName, paramType)
      # check if tokens ended
      if cursor > rightCursor: break

  def parseFunctionBody(self, func, leftIndex, rightIndex, source):
    # raise Exception('parseFunctionBody not implemented')

    if (rightIndex - leftIndex) == 1: return

    # bodyRule = grammar.getRule('function_body')
    nodes = self.parseByRules(grammar.function_body_rules, leftIndex, rightIndex, source)

    for node in nodes:
      func.addBodyNode(node)

  def parseEnumBody(self, en, leftIndex, rightIndex, source):
    cursor = leftIndex
    enumVarRule = grammar.getRule('enum_var')
    while cursor <= rightIndex:
      match = matchNodes(enumVarRule)
      if match == None: break
      # add enum member
      name = match.params['name'][0].word
      value = match.params['value'][0].word
      en.addMember(name, value)
      # move cursor to next
      cursor = match.rightIndex + 1

  def parseStructBody(self, st, leftIndex, rightIndex, source):
    # raise Exception('parseStructBody not implemented')

    nodes = self.parseByRules(grammar.struct_body_rules, leftIndex, rightIndex, source)

    for node in nodes:
      st.addVariable(node)

  def parseClassBody(self, cl, leftIndex, rightIndex, source):
    nodes = self.parseByRules(grammar.class_body_rules, leftIndex, rightIndex, source)
    for node in nodes:
      if node.nodetype == 'function':
        if node.name == None:
          cl.setConstructor(node)
        else:
          cl.addFunction(node)
      if node.nodetype == 'variable':
        cl.addVariable(node)

  def parseConstructorInit(self, con, leftIndex, rightIndex, source):
    raise Exception('parseConstructorInit not implemented')

  def parseTag(self, leftIndex, rightIndex, source):
    raise Exception('parseTag not implemented')

    # check open-close brackets
    bracketCounter = TagBracketCounter()
    bracketCounter.check(leftIndex, rightIndex, source)

    leftCursor = leftIndex
    rightCursor = rightIndex
    while leftCursor <= rightCursor:
      # search open bracket, we have tag begin
      if source.tokens[leftCursor] == '<':
        pass
