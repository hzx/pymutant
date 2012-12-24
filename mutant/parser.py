from mutant import core as core
from mutant import grammar
from mutant.counters import BracketCounter, TagBracketCounter
from mutant.common import getTokensRange
from mutant.matches import Match, mergeMatches, matchNodes, tokensToString, findWordIndex, findCommaIndex


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

  def addModuleNodes(self, nodes, module, source):
    for node in nodes:
      func = self.moduleNodeMap[node.nodetype]
      func(module, source, node)

  def addModuleVariable(self, module, source, var):
    if var.name in module.variables:
      raise Exception('Module variable redefinition, variable name "%s", source "%s"' % (var.name, source.filename))
    module.variables[var.name] = var
  def addModuleFunction(self, module, source, func):
    if func.name in module.functions:
      raise Exception('Module function redefinition, function name "%s", source "%s"' % (func.name, source.filename))
    module.functions[func.name] = func
  def addModuleEnum(self, module, source, en):
    if en.name in module.enums:
      raise Exception('Module enum redefinition, enum name "%s", source "%s"' % (en.name, source.filename))
    module.enums[en.name] = en
  def addModuleStruct(self, module, source, st):
    if st.name in module.structs:
      raise Exception('Module struct redefinition, struct name "%s", source "%s"' % (st.name, source.filename))
    module.structs[st.name] = st
  def addModuleClass(self, module, source, cl):
    if cl.name in module.classes:
      raise Exception('Module class redefinition, class name "%s", source "%s"' % (cl.name, source.filename))
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

    self.addModuleNodes(nodes, self.module, source)

  def parseByRules(self, ruleNames, leftIndex, rightIndex, source):
    """
    Parse tokens by rules.
    Call handler with match.
    Return Match object if match rules, else - None.
    Parse from left to right direction, move cursor from leftIndex
      to rightIndex.
    """
    cursor = leftIndex
    nodes = []
    while cursor <= rightIndex:
      ruleFound = False
      # search rules match and create node
      for ruleName in ruleNames:
        rule = grammar.getRule(ruleName)
        match = matchNodes(rule, cursor, rightIndex, source)
        if match:
          # handler name = rule name
          handler = grammar.getHandler(ruleName)
          node = handler(match, source)
          nodes.append(node)
          cursor = match.rightIndex + 1
          ruleFound = True
          break
      # check if all tokens parsed
      if not ruleFound:
        tokensString = tokensToString(source.tokens[leftIndex:rightIndex+1])
        raise Exception('No rule found for parse, source "%s", tokens "%s"' % (source.filename, tokensString))
    return nodes

  def parseByRulesMulti(self, ruleNames, leftIndex, rightIndex, source):
    cursor = leftIndex
    nodes = []
    while cursor <= rightIndex:
      ruleFound = False
      for ruleName in ruleNames:
        rule = grammar.getRule(ruleName)
        match = matchNodes(rule, cursor, rightIndex, source)
        if match:
          handlersNodes = self.nodesByHandlers(match.handlers, source)
          nodes = nodes + handlersNodes
          cursor = match.rightIndex + 1
          ruleFound = True
          break
      if not ruleFound:
        raise Exception('No rule found in "%s" source' % (source.filename))
    return nodes

  def bindHandlers(self):
    """
    Bind grammar.handlers map to self.handle*.
    """
    # bind global handlers
    grammar.setHandler('define', self.createDefine)
    grammar.setHandler('variable', self.createVariable)
    grammar.setHandler('function', self.createFunction)
    grammar.setHandler('enum', self.createEnum)
    grammar.setHandler('struct', self.createStruct)
    grammar.setHandler('class', self.createClass)

    grammar.setHandler('expression', self.createExpression)
    grammar.setHandler('expression_body', self.matchExpression)

    grammar.setHandler('variable_body', self.matchVariableBody)

    grammar.setHandler('function_params', self.matchFunctionParams)
    grammar.setHandler('function_body', self.matchFunctionBody)
    grammar.setHandler('function_return', self.handleFunctionReturn)

    grammar.setHandler('enum_body', self.handleEnumBody)

    grammar.setHandler('struct_body', self.handleStructBody)

    grammar.setHandler('class_body', self.matchClassBody)
    grammar.setHandler('constructor', self.createConstructor)
    grammar.setHandler('constructor_call', self.createConstructorCall)
    grammar.setHandler('constructor_init', self.matchConstructorInit)

    grammar.setHandler('variable_assign', self.createVariableAssign)
    grammar.setHandler('match_variable_assign', self.matchVariableAssign)

    grammar.setHandler('array_value', self.createArrayValue)
    grammar.setHandler('array_body', self.createArrayBody)
    grammar.setHandler('match_array_body', self.matchArrayBody)

    grammar.setHandler('select_from', self.createSelectFrom)
    grammar.setHandler('select_concat', self.createSelectConcat)

    grammar.setHandler('selectfrom_body', self.matchSelectFromBody)
    grammar.setHandler('selectconcat_body', self.matchSelectConcatBody)

    grammar.setHandler('tag', self.createTag)
    grammar.setHandler('tag_body', self.matchTag)

    grammar.setHandler('operator', self.handleOperator)

    # bind parsers
    grammar.setHandler('parseArrayBody', self.parseArrayBody)
    grammar.setHandler('parseVariableBody', self.parseVariableBody)
    grammar.setHandler('parseFunctionParams', self.parseFunctionParams)
    grammar.setHandler('parseFunctionBody', self.parseFunctionBody)
    grammar.setHandler('parseEnumBody', self.parseEnumBody)
    grammar.setHandler('parseStructBody', self.parseStructBody)
    grammar.setHandler('parseClassBody', self.parseClassBody)
    grammar.setHandler('parseOperator', self.parseOperator)
    grammar.setHandler('parseConstructorInit', self.parseConstructorInit)
    grammar.setHandler('parseSelectFromBody', self.parseSelectFromBody)
    grammar.setHandler('parseSelectConcatBody', self.parseSelectConcatBody)

  def runHandlers(self, obj, handlers, source):
    for handlerName, handlerMatch in handlers.items():
      handler = grammar.getHandler(handlerName)
      handler(obj, handlerMatch.leftIndex, handlerMatch.rightIndex, source)

  def nodesByHandlers(self, handlers, source):
    nodes = []
    for handlerName, handlerMatch in handlers.items():
      handler = grammar.getHandler(handlerName)
      node = handler(handlerMatch.leftIndex, handlerMatch.rightIndex, source)
      nodes.append(node)
    return nodes

  # Grammar handlers

  def createImport(self, match, source):
    """
    FOR NOW NOT USED, IMPORT PROCESS BY LOADER.
    Import module.
    """
    raise Exception('createImport not implemented')

  def createDefine(self, match, source):
    """
    Add type alias.
    """
    raise Exception('createDefine not implemented')

  def createVariable(self, match, source):
    """
    Create core.VariableNode.
    """
    name = match.params['name'][0].word
    decltype = match.params['type']
    var = core.VariableNode(decltype, name)
    
    self.runHandlers(var, match.handlers, source)

    return var

  def createFunction(self, match, source):
    """
    Create core.FunctionNode.
    """
    name = match.params['name'][0].word
    decltype = match.params['type']
    func = core.FunctionNode(decltype, name)

    self.runHandlers(func, match.handlers, source)

    return func

  def createEnum(self, match, source):
    """
    Create core.EnumNode.
    """
    name = match.params['name'][0].word
    en = core.EnumNode(name)

    self.runHandlers(en, match.handlers, source)
  
    return en

  def createStruct(self, match, source):
    """
    Create core.StructNode.
    """
    name = match.params['name'][0].word
    baseName = match.params.get('base_name', None)
    st = core.StructNode(name, baseName)

    self.runHandlers(st, match.handlers, source)

    return st

  def createClass(self, match, source):
    """
    Create core.ClassNode.
    """
    name = match.params['name'][0].word
    baseName = match.params.get('base_name', None)
    cl = core.ClassNode(name, baseName)

    self.runHandlers(cl, match.handlers, source)

    return cl

  # OTHER RULES

  def createArrayValue(self, match, source):
    value = match.params['value'][0]
    index = match.params['index'][0].word
    return core.ArrayValueNode(value, index)

  def createArrayBody(self, match, source):
    nodes = self.nodesByHandlers(match.handlers, source)

    return nodes[0]

  def createSelectFrom(self, match, source):
    name = match.params['name'][0].word
    selectFrom = core.SelectFromNode(name)

    self.runHandlers(selectFrom, match.handlers, source)

    return selectFrom

  def matchSelectFromBody(self, leftIndex, rightIndex, source):
    """
    Return match.
    """
    semicolonIndex = findWordIndex(';', leftIndex, rightIndex, source.tokens)
    rightCursor = rightIndex
    rightEnd = rightIndex
    if semicolonIndex >= 0:
      rightCursor = semicolonIndex - 1
      rightEnd = semicolonIndex

    outMatch = Match(leftIndex, rightEnd)
    outMatch.handlers['parseSelectFromBody'] = Match(leftIndex, rightCursor)

    return outMatch

  def createSelectConcat(self, match, source):
    """
    Create core.SelectConcatNode.
    """
    selectConcat = core.SelectConcatNode()

    self.runHandlers(selectConcat, match.handlers, source)

    return selectConcat

  def matchSelectConcatBody(self, leftIndex, rightIndex, source):
    """
    Return match.
    """
    semicolonIndex = findWordIndex(';', leftIndex, rightIndex, source)
    if semicolonIndex < 0:
      raise Exception('select from body: not found ; in source "%s"' % source.filename)
    rightCursor = semicolonIndex - 1

    outMatch = Match(leftIndex, semicolonIndex)
    outMatch.handlers['parseSelectConcatBody'] = Match(leftIndex, rightCursor)

    return outMatch

  def createTag(self, match, source):
    """
    Check open-close brackets.
    Use for real work parseTag method.
    """
    # check open-close brackets
    bracketCounter = TagBracketCounter()
    bracketCounter.check(match.leftIndex, match.rightIndex, source)

    nodes = self.parseHtml(match.leftIndex, match.rightIndex, source)

    if len(nodes) != 1:
      raise Exception('html must contain only one root node, linenum "%d", source "%s"' % (source.tokens[match.leftIndex].linenum, source.filename))

    return nodes[0]

  def matchTag(self, leftIndex, rightIndex, source):
    """
    Match < and /> symbols
    first symbol must be <
    last symbols must be />|> ; or />|>
    """
    if source.tokens[leftIndex].word != '<': return None

    rightCursor = rightIndex

    # find ;
    semicolonIndex = findWordIndex(';', leftIndex, rightIndex, source.tokens)
    if semicolonIndex >= 0:
      rightCursor = semicolonIndex - 1

    # find > />
    if source.tokens[rightCursor].word in ['>', '/>']:
      return Match(leftIndex, rightCursor)

    raise Exception('not found close bracket ">" or "/>" for tag, linenum "%d", source "%s"' % (source.tokens[leftIndex].linenum, source.filename))

  def findCloseTag(self, name, leftIndex, rightIndex, source):
    """
    Find tag </ name > in the end.
    Return match.
    """
    leftCursor = leftIndex
    rightCursor = rightIndex

    isOpenTag = False
    isCloseTag = False
    tagCount = 0
    leftClose = -1
    while leftCursor <= rightIndex:
      token = source.tokens[leftCursor]
      word = token.word

      if word == '<':
        isOpenTag = True
      elif word == '</':
        isCloseTag = True
        leftClose = leftCursor
      elif word == '>':
        if isOpenTag:
          isOpenTag = False
          tagCount = tagCount + 1
        elif isCloseTag:
          isCloseTag = False
          tagCount = tagCount - 1
        else:
          raise Exception('parse tag error, mixed <, </, >, />, linenum "%d", source "%s"' % (token.linenum, source.filename))
      elif word == '/>':
        isOpenTag = False

      # check tagCount must be -1, because we find in remainder, without open tag
      if tagCount == -1:
        if leftClose < 0:
          raise Exception('tag parse error, not found close tag, linenum "%d", source "%s"' % (token.linenum, source.filename))
        # check open-close tag name
        nameToken = source.tokens[leftClose+1]
        if name != nameToken.word:
          raise Exception('close tag found, but with different name, linenum "%d", source "%s"' % (nameToken.linenum, source.filename))
        return Match(leftClose, leftCursor)

      # shift leftCursor to right
      leftCursor = leftCursor + 1

    # not found close tag
    return None

  def parseTagAttrs(self, tag, leftIndex, rightIndex, source):
    """
    Find tag attributes and add it to tag.
    """
    leftCursor = leftIndex
    # need for parsing current attribute body

    while leftCursor <= rightIndex:
      rightCursor = rightIndex
      nameToken = source.tokens[leftCursor]

      # check attribute token count >= 3
      indexDiff = rightIndex - leftCursor
      if indexDiff < 2:
        raise Exception('not enough tokens count "%d" for attribute, linenum "%d", source "%s"' % (indexDiff, nameToken.linenum, source.filename))

      # check attribute name
      if not (nameToken.wordtype in ['name', 'class']):
        raise Exception('tag attribute must begin from name token, linenum "%d", source "%s"' % (nameToken.linenum, source.filename))
      attrName = nameToken.word

      # find = after name token
      equalToken = source.tokens[leftCursor+1]

      # find next attribute by 'name =', and after current name = value
      nextAttrIndex = self.findNextTagAttr(leftCursor+2, rightIndex, source)
      if nextAttrIndex >= 0: rightCursor = nextAttrIndex - 1
      # if rightCursor - (leftCursor+2) > 1:
      attrBodyNode = self.parseTagAttrBody(leftCursor+2, rightCursor, source)
      # add attribute to tag
      tag.addAttribute(nameToken.word, attrBodyNode)

      # shift cursor after current attribute end
      leftCursor = rightCursor + 1

  def findNextTagAttr(self, leftIndex, rightIndex, source):
    """
    Find 'name =' in tokens.
    Return name index of tag attribute.
    Return -1 if not found.
    """
    cursor = leftIndex
    while cursor <= rightIndex:
      if rightIndex - cursor < 2: return -1
      if source.tokens[cursor].wordtype in ['name', 'class'] and source.tokens[cursor+1].wordtype == '=':
        return cursor
      cursor = cursor + 1
    return -1

  def parseTagAttrBody(self, leftIndex, rightIndex, source):
    """
    Create and return node by variable_body_rules.
    """
    nodes = self.parseByRules(grammar.variable_body_rules, leftIndex, rightIndex, source)

    leftToken = source.tokens[leftIndex]

    lenNodes = len(nodes)
    if lenNodes == 1:
      return nodes[0]
    if lenNodes > 1:
      raise Exception('tag attribute body must contain one node, lenNodes "%d", linenum "%d", source "%s"' % (lenNodes, leftToken.linenum, source.filename))

    raise Exception('not rule found for attribute body, token "%s", linenum "%d", source "%s"' % (leftToken.word, leftToken.linenum, source.filename))

  def matchVariableBody(self, leftIndex, rightIndex, source):
    """
    Search ; and if found any symbol before = return None.
    """
    firstToken = source.tokens[leftIndex]

    if firstToken.word == ';':
      return Match(leftIndex, leftIndex)
    # find equal symbol
    elif firstToken.word in ['=', ':=']:
      # find ;
      semicolonIndex = findWordIndex(';', leftIndex, rightIndex, source.tokens)
      if semicolonIndex < 0:
        raise Exception('; not found, linenum "%d", source "%s"' %(firstToken.linenum, source.filename))
      match = Match(leftIndex, semicolonIndex)
      match.handlers['parseVariableBody'] = Match(leftIndex, semicolonIndex-1)
      return match

    return None

  def matchArrayBody(self, leftIndex, rightIndex, source):
    """
    Return match to [ and ] and check ;.
    """
    rightCursor = rightIndex
    rightMatch = rightIndex

    semicolonIndex = findWordIndex(';', leftIndex, rightIndex, source.tokens)
    if semicolonIndex >= 0:
      rightCursor = semicolonIndex-1
      rightMatch = semicolonIndex

    leftToken = source.tokens[leftIndex]
    rightToken = source.tokens[rightCursor]

    if leftToken.word == '[' and rightToken.word == ']':
      match = Match(leftIndex, rightMatch)
      if (rightCursor) - (leftIndex) > 1:
        match.handlers['parseArrayBody'] = Match(leftIndex+1, rightCursor-1)
      return match

    return None


  def matchFunctionParams(self, leftIndex, rightIndex, source):
    if source.tokens[leftIndex].word == '(':
      bracketCounter = BracketCounter()
      match = bracketCounter.findPair(leftIndex, rightIndex, source)
      match.handlers['parseFunctionParams'] = Match(leftIndex+1, match.rightIndex-1)
      return match
    return None

  def matchFunctionBody(self, leftIndex, rightIndex, source):
    if source.tokens[leftIndex].word == '{':
      bracketCounter = BracketCounter()
      match = bracketCounter.findPair(leftIndex, rightIndex, source)
      match.handlers['parseFunctionBody'] = Match(match.leftIndex+1, match.rightIndex-1)
      return match
    return None

  def handleFunctionReturn(self, match, source):
    # search and create return body node
    # raise Exception('handleFunctionReturn not implemented')

    # nodes = self.nodesByHandlers(match.handlers, source)

    # think about this hardcode, above not work - return array of array (nodes of nodes)
    opMatch = match.handlers['parseOperator']
    nodes = self.parseOperator(opMatch.leftIndex, opMatch.rightIndex, source)
    
    if len(nodes) != 1:
      raise Exception('return have one body node, source "%s"', source.filename)

    returnNode = core.ReturnNode()
    returnNode.setBody(nodes[0])

    return returnNode

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

  def matchClassBody(self, leftIndex, rightIndex, source):
    """
    Match class body, left token must be { and right token must be }
    """
    if source.tokens[leftIndex].word == '{':
      bracketCounter = BracketCounter()
      match = bracketCounter.findPair(leftIndex, rightIndex, source)
      match.handlers['parseClassBody'] = Match(match.leftIndex+1, match.rightIndex-1)
      return match
    return None

  def createConstructor(self, match, source):
    """
    Create core.FunctionNode with decltype and name is None
    """
    name = None
    decltype = None
    con = core.FunctionNode(decltype, name)

    self.runHandlers(con, match.handlers, source)

    return con
    

  def createConstructorCall(self, match, source):
    """
    Create constructor (function) node.
    """
    name = match.params['name'][0].word
    con = core.FunctionNode(None, None)

    self.runHandlers(con, match.handlers, source)

    return con

  def matchConstructorInit(self, leftIndex, rightIndex, source):
    if source.tokens[leftIndex] == '{':
      bracketCounter = BracketCounter()
      match = bracketCounter.findPair(leftIndex, rightIndex, source)
      match.handlers['parseConstructorInit'] = Match(leftIndex+1, match.rightIndex-1)
      return match
    return None

  def createVariableAssign(self, match, source):
    """
    Create core.ValueNode.
    """
    nameToken = match.params['name']
    value = core.ValueNode(nameToken)

    self.runHandlers(value, match.handlers, source)

    return value


  def matchVariableAssign(self, left, right, source):
    # check count tokens >=4 : name = value ;
    if right - left < 3: return None

    nameToken = source.tokens[left]
    if nameToken.wordtype != 'name': return None

    equalToken = source.tokens[left+1]
    if not (equalToken.wordtype in ['=', ':=']): return None

    # we have variable assign

    semicolonIndex = findWordIndex(';', left, right, source.tokens)
    if semicolonIndex < 0:
      raise Exception('Not found ";", linenum "%d", source "%s"' % (nameToken.linenum, source.filename))

    match = Match(left, semicolonIndex)
    match.params['name'] = nameToken
    match.handlers['parseVariableBody'] = Match(left+1, semicolonIndex-1)
    return match

  def matchExpression(self, leftIndex, rightIndex, source):
    """
    Return match.
    """
    rightCursor = rightIndex
    rightHandle = rightIndex

    # tokens may contain ; search new rightCursor
    semicolonIndex = findWordIndex(';', leftIndex, rightIndex, source.tokens)
    if semicolonIndex >= 0:
      rightCursor = semicolonIndex - 1
      rightHandle = semicolonIndex

    outMatch = Match(leftIndex, rightHandle)

    return outMatch

  def handleOperator(self, leftIndex, rightIndex, source):
    rightCursor = rightIndex
    rightMatch = rightIndex

    semicolonIndex = findWordIndex(';', leftIndex, rightIndex, source.tokens)
    if semicolonIndex >= 0:
      rightCursor = semicolonIndex - 1
      rightMatch = semicolonIndex

    outMatch = Match(leftIndex, rightMatch)
    outMatch.handlers['parseOperator'] = Match(leftIndex, rightCursor)

    return outMatch

  def matchSelectFromBody(self, leftIndex, rightIndex, source):
    """
    Find ; and add parseSelectFromBody to handlers
    """
    rightCursor = rightIndex

    # search ; symbol index and correct rightCursor
    # semicolonIndex = findWordIndex(';', leftIndex, rightIndex, source.tokens)
    # if semicolonIndex >= 0: rightCursor = semicolonIndex - 1

    outMatch = Match(leftIndex, rightCursor)
    outMatch.handlers['parseSelectFromBody'] = Match(leftIndex, rightCursor)

    return outMatch

  def handleSelectConcatBody(self, leftIndex, rightIndex, source):
    """
    Find ; and add parseSelectConcatBody to handlers
    """
    rightCursor = rightIndex

    # search ; symbol index and correct rightCursor
    semicolonIndex = findWordIndex(';', leftIndex, rightIndex, source.tokens)
    if semicolonIndex >= 0: rightCursor = semicolonIndex - 1

    outMatch = Match(leftIndex, semicolonIndex)
    outMatch.handlers['parseSelectConcatBody'] = Match(leftIndex, rightCursor)

    return outMatch

  # PARSE

  def createExpression(self, match, source):
    """
    Create tree.
    Return rootNode. 
    """
    funcCallRule = grammar.getRule('function_call')

    # create nodes list with weights
    cursor = match.leftIndex
    nodes = []
    bracketWeight = 0
    while cursor <= match.rightIndex:
      token = source.tokens[cursor]
      # check system functions
      if token.word in grammar.functionNames:
        nodes.append({'kind': token.word, 'match': Match(cursor, cursor), 'weight': grammar.functionsWeight[token.word] + bracketWeight})
        cursor = cursor + 1
        continue
      # check function call
      funcMatch = matchNodes(funcCallRule, cursor, match.rightIndex, source)
      if funcMatch:
        bracketCounter = BracketCounter()
        closedIndex = bracketCounter.findPair(funcMatch.rightIndex, match.rightIndex)
        if closedIndex < 0:
          raise Exception('not found closed bracket ), cursor "%d", linenum "%s", source "%s"' % (cursor, token.linenum, source.filename))
        nodes.append({'kind': 'function', 'match': Match(funcMatch.leftIndex, closedIndex), 'weight': grammar.functionsWeight['function'] + bracketWeight})
        # move cursor after function call
        cursor = closedIndex + 1
        continue
      # add variable
      if token.wordtype in ['name', 'litint', 'litfloat', 'litstring', 'litbool']:
        nodes.append({'kind': 'value', 'match': Match(cursor, cursor), 'weight': bracketWeight})
      # check bracket
      # set nodes additional weights
      elif token.word == '(':
        bracketWeight = bracketWeight + grammar.bracketWeight
      elif token.word == ')':
        bracketWeight = bracketWeight - grammar.bracketWeight
      else:
        raise Exception('Unknown token word "%s", cursor "%d", linenum "%d",  source "%s"' % (token.word, cursor, token.linenum, source.filename))
      # move cursor after function call
      cursor = cursor + 1

    # create tree from nodes
    if len(nodes) > 0:
      return self.createExpressionTree(0, len(nodes), nodes, source)

    return None

  def parseOperator(self, leftIndex, rightIndex, source):
    """
    Return nodes
    """
    # raise Exception('parseOperator not implemented')
    nodes = self.parseByRules(grammar.variable_body_rules, leftIndex, rightIndex, source)
    return nodes

  def parseArrayBody(self, leftIndex, rightIndex, source):
    """
    Create core.ArrayBodyNode create by variable_body_rules.
    """
    # raise Exception('parseArrayBody not implemented')

    leftCursor = leftIndex
    arrayBody = core.ArrayBodyNode()
    while leftCursor <= rightIndex:
      # find ,
      commaIndex = findWordIndex(',', leftCursor, rightIndex, source.tokens)
      rightCursor = rightIndex
      endCursor = rightIndex
      if commaIndex >= 0:
        endCursor = commaIndex
        rightCursor = commaIndex - 1

      # DEBUG
      # raise Exception('leftCursor "%d", rightCursor "%d", tokens "%s"' % (leftCursor, rightCursor, tokensToString(source.tokens[leftCursor:rightCursor+1])))

      nodes = self.parseByRules(grammar.variable_body_rules, leftCursor, rightCursor, source)

      # check nodes and add item
      lenNodes = len(nodes)
      if lenNodes == 1:
        arrayBody.addItem(nodes[0])
      if lenNodes > 1:
        raise Exception('array item must have one or zero body node, linenum "%d", source "%s"' % (source.tokens[leftIndex].linenum, source.filename))

      # shift cursor after , or after rightIndex
      leftCursor = endCursor + 1
    return arrayBody

  def parseVariableBody(self, var, leftIndex, rightIndex, source):
    # search = or :=
    cursorLeft = leftIndex
    firstToken = source.tokens[leftIndex]
    if firstToken.word in ['=', ':=']:
      # set body reactive
      if firstToken.word == ':=':
        var.setBodyReactive(True)
      cursorLeft = leftIndex+1

    # create nodes by rules
    nodes = self.parseByRules(grammar.variable_body_rules, cursorLeft, rightIndex, source)

    if len(nodes) > 1:
      raise Exception('parse error: variable body must have one or zero body node, linenum "%d", source "%s"' % (source.tokens[leftIndex].linenum, source.filename))

    if len(nodes) == 1:
      var.setBody(nodes[0])

  def parseFunctionParams(self, func, leftIndex, rightIndex, source):
    cursor = leftIndex
    paramRule = grammar.getRule('function_param')
    while cursor <= rightIndex:
      # parse by param rule
      match = matchNodes(paramRule, cursor, rightIndex, source)
      if match == None:
        raise Exception('not parse function params, source "%s", linenum "%d"' % (source.filename, source.tokens[leftIndex].linenum))
      # move cursor from match.rightIndex to next and after comma
      cursor = match.rightIndex + 2
      # add parameter to function
      paramName = match.params['name'][0].word
      paramType = match.params['type']

      func.addParameter(paramName, paramType)

  def parseFunctionBody(self, func, leftIndex, rightIndex, source):
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
    nodes = self.parseByRules(grammar.struct_body_rules, leftIndex, rightIndex, source)

    for node in nodes:
      st.addVariable(node)

  def parseClassBody(self, cl, leftIndex, rightIndex, source):
    nodes = self.parseByRules(grammar.class_body_rules, leftIndex, rightIndex, source)
    for node in nodes:
      if node.nodetype == 'function':
        if node.name == None:
          # check if constructor exists
          if cl.constructor != None:
            raise Exception('class constructor redefinition, class name "%s", source "%s"' % (cl.name, source.filename))
          cl.setConstructor(node)
        else:
          # check if function exists
          if node.name in cl.functions:
            raise Exception('class function redefinition, class name "%s", function name "%s", source "%s"' % (cl.name, node.name, source.filename))
          cl.addFunction(node)
      if node.nodetype == 'variable':
        # check if variable exists
        if node.name in cl.variables:
          raise Exception('class variable redefinition, class name "%s", variable name "%s", source "%s"' % (cl.name, node.name, source.filename))
        cl.addVariable(node)

  def parseConstructorInit(self, con, leftIndex, rightIndex, source):
    """
    Check if see "," symbol.
    """
    mapItemRule = grammar.getRule('map_item')

    cursorLeft = leftIndex
    cursorRight = rightIndex
    while cursorLeft <= rightIndex:
      commaIndex = findCommaIndex(leftIndex, rightIndex, source.tokens)
      if commaIndex >= 0:
        cursorRight = commaIndex - 1
      match = matchNodes(mapItemRule, cursorLeft, cursorRight, source)
      if match == None: raise Exception('constructor with parameter item not contains items, source %s' % source.filename) 
      cursorLeft = match.rightIndex + 1
      cursorRight = rightIndex
      # add init item to constructor
      name = match.params['name'][0].word
      nodes = self.nodesByHandlers(match.handlers, source)
      if (len(nodes)) != 1:
        raise Exception('constructor with parameter item must contain only one body node')
      con.addInit(name, nodes[0])

  def parseSelectFromBody(self, selectFrom, leftIndex, rightIndex, source):
    """
    Set in selectFrom where node and order field node.
    """
    # find where
    whereIndex = findWordIndex('where', leftIndex, rightIndex, source.tokens)

    # find order by
    orderIndex = findWordIndex('order', leftIndex, rightIndex, source.tokens)

    # check if exists body
    if whereIndex < 0 and orderIndex < 0:
      raise Exception('select from without where and order, linenum "%d", source "%s"' % (source.tokens[leftIndex].linenum, source.filename))

    # set where expression to selectFrom
    if whereIndex >= 0:
      whereRight = rightIndex
      # set cursor before order by
      if orderIndex >= 0: whereRight = orderIndex-1
      whereExpression = self.createExpression(Match(whereIndex+1, whereRight), source)
      selectFrom.setWhere(whereExpression)
    
    # set order by to selectFrom
    if orderIndex >= 0:
      # check by word
      byToken = source.tokens[orderIndex+1]
      if byToken.word != 'by':
        raise Exception('select from order must follow by word, linenum "%d", source "%s"' % (byToken.linenum, source.filename))

      orderbyParamRule = grammar.getRule('orderby_param')
      match = matchNores(orderByParamRule, orderIndex+2, rightIndex, source)
      if not match:
        raise Exception('select from order by param error, linenum "%d", source "%s"' % (byToken.linenum, source.filename))

      paramName = match.params['name'][0]
      paramOrder = match.params['order'][0].word

      selectFrom.setOrderField(paramName, paramOrder)

  def parseSelectConcatBody(selectConcat, leftIndex, rightIndex, source):
    """
    Add to selectConcat collections.
    """
    raise Exception('parseSelectConcatBody')

  def parseHtml(self, left, right, source):
    """
    Parse html - tag and expression mix.
    Html expression not support logical operations with <, >;
      wrap it in function if needed. 
    Return expression, tag nodes.
    """
    leftCursor = left
    rightCursor = right
    nodes = []
    bracketCounter = TagBracketCounter()
    while leftCursor <= rightCursor:
      # search open bracket
      openBracket = findWordIndex('<', leftCursor, rightCursor, source.tokens)
      # if found open bracket
      if openBracket >= 0:
        # check if have expression before tag, and parse-add it to nodes
        if leftCursor < openBracket:
          nodes.append(self.createExpression(Match(leftCursor, openBracket-1), source))
        # find close bracket
        closeBracket = bracketCounter.findPair(openBracket, rightCursor, source)
        # order = openBracket nameIndex ... closeBracket
        nameIndex = openBracket+1
        nameToken = source.tokens[nameIndex]

        # nameToken.wordtype must be name
        if nameToken.wordtype != 'name':
          raise Exception('not found tag name, linenum "%d", source "%s"' % (nameToken.linenum, source.filename))
        tag = core.TagNode(nameToken.word)
        nodes.append(tag)
        # if have attributes, parse-add it
        if closeBracket - nameIndex > 1:
          self.parseTagAttrs(tag, nameIndex+1, closeBracket-1, source)
        # check if we have open-close tag
        if source.tokens[closeBracket].word == '>':
          # find close tag
          closeTag = self.findCloseTag(nameToken.word, closeBracket+1, rightCursor, source)
          # check closeMatch
          if closeTag == None:
            raise Exception('not found close tag, linenum "%d", source "%s"' % (source.tokens[closeBracket].linenum, source.filename))
          # parse child nodes
          if closeTag.leftIndex - closeBracket > 1:
            childs = self.parseHtml(closeBracket+1, closeTag.leftIndex-1, source)
            # add all childs
            for child in childs: tag.addChild(child)
          # closeBracket equal to close bracket in close tag
          closeBracket = closeTag.rightIndex
        # shift leftCursor after closeBracket
        leftCursor = closeBracket + 1
      else:
        # have only expression node
        nodes.append(self.createExpression(Match(leftCursor, rightCursor), source))
        break

    return nodes

  # utilities

  def createExpressionTree(self, leftIndex, rightIndex, nodes, source):
    minIndex = self.findLighterIndex(leftIndex, rightIndex, nodes)
    node = nodes[minIndex]

    kind = node['kind']
    match = node['match']

    createNode = None

    # create
    if kind == 'function':
      name = source.tokens[match.leftIndex].word
      createNode = core.FunctionCallNode(name)
      # TODO(dem) parse params
    elif kind in grammar.unaryFunctions:
      createNode = core.FunctionCallNode(kind)
      # parse right indexes
      paramNode = self.createExpressionTree(minIndex + 1, rightIndex, nodes, source)
      createNode.addParameter(paramNode)
    elif kind in grammar.binaryFunctions:
      createNode = core.FunctionCallNode(kind)
      leftParam = self.createExpressionTree(minIndex - 1, leftIndex, nodes, source)
      rightParam = self.createExpressionTree(minIndex + 1, rightIndex, nodes, source)
      createNode.addParameter(leftParam)
      createNode.addParameter(rightParam)
    else:
      # we have value node
      value = source.tokens[match.leftIndex]
      createNode = core.ValueNode(value)

    if createNode == None:
      raise Exception('created node in expression is None, source "%s"' % source.filename)

    return createNode

  def findLighterIndex(self, left, right, nodes):
    """
    Search functions first and value in last resort.
    """
    minIndex = -1
    minWeight = 10000
    for num, node in enumerate(nodes[left:right+1], left):
      kind = node['kind']
      weight = node['weight']
      # we have function
      if kind != 'value':
        # set lighter index and weight
        if weight < minWeight:
          minWeight = weight
          minIndex = num
    # if not exists function node, set first value node
    if minIndex < 0: minIndex = left
    return minIndex
