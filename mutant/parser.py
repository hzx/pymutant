from mutant import core as core
from mutant import grammar
from mutant.counters import BracketCounter, TagBracketCounter, findCommaIndex
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
    grammar.setHandler('import', self.createImport)
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

    grammar.setHandler('enum_body', self.matchEnumBody)

    grammar.setHandler('struct_body', self.matchStructBody)

    grammar.setHandler('class_body', self.matchClassBody)
    grammar.setHandler('constructor', self.createConstructor)
    grammar.setHandler('constructor_call', self.createConstructorCall)
    grammar.setHandler('constructor_init', self.matchConstructorInit)

    grammar.setHandler('variable_assign', self.createVariableAssign)
    grammar.setHandler('match_variable_assign', self.matchVariableAssign)

    grammar.setHandler('array_value', self.createArrayValue)
    grammar.setHandler('array_body', self.createArrayBody)
    grammar.setHandler('dict_body', self.createDictBody)
    grammar.setHandler('dict_value', self.createDictValue)
    grammar.setHandler('match_array_body', self.matchArrayBody)
    grammar.setHandler('match_dict_body', self.matchDictBody)

    grammar.setHandler('insert', self.createInsert)
    grammar.setHandler('insert_body', self.matchInsertBody)
    grammar.setHandler('parseInsertBody', self.parseInsertBody)
    grammar.setHandler('select_count', self.createSelectCount)
    grammar.setHandler('select_one', self.createSelectOne)
    grammar.setHandler('selectone_body', self.matchSelectOneBody)
    grammar.setHandler('parseSelectOneBody', self.parseSelectOneBody)
    grammar.setHandler('select_from', self.createSelectFrom)
    grammar.setHandler('select_concat', self.createSelectConcat)
    grammar.setHandler('update', self.createUpdate)
    grammar.setHandler('update_body', self.matchUpdateBody)
    grammar.setHandler('parseUpdateBody', self.parseUpdateBody)
    grammar.setHandler('delete_from', self.createDeleteFrom)

    grammar.setHandler('select_sum', self.createSelectSum)

    grammar.setHandler('selectfrom_body', self.matchSelectFromBody)
    grammar.setHandler('selectconcat_body', self.matchSelectConcatBody)
    grammar.setHandler('deletefrom_body', self.matchDeleteFromBody)

    grammar.setHandler('tag', self.createTag)
    grammar.setHandler('tag_body', self.matchTag)

    grammar.setHandler('if', self.createIf)
    grammar.setHandler('if_body', self.matchIfBody)
    grammar.setHandler('parseIfExpr', self.parseIfExpr)
    grammar.setHandler('parseIfBody', self.parseIfBody)
    grammar.setHandler('parseElseBody', self.parseElseBody)

    grammar.setHandler('for', self.createFor)
    grammar.setHandler('iteration_body', self.matchIterationBody)
    grammar.setHandler('parseIterationBody', self.parseIterationBody)
    grammar.setHandler('for_body', self.matchForBody)
    grammar.setHandler('parseForBody', self.parseForBody)

    grammar.setHandler('while', self.createWhile)
    grammar.setHandler('while_expression', self.matchWhileExpression)
    grammar.setHandler('parseWhileExpression', self.parseWhileExpression)
    
    grammar.setHandler('operator', self.handleOperator)

    # bind parsers
    grammar.setHandler('parseDictBody', self.parseDictBody)
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
    grammar.setHandler('parseDeleteFromBody', self.parseDeleteFromBody)

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
    baseName = None
    if 'base_name' in match.params:
      baseName = match.params['base_name'][0].word
    st = core.StructNode(name, baseName)

    self.runHandlers(st, match.handlers, source)

    return st

  def createClass(self, match, source):
    """
    Create core.ClassNode.
    """
    name = match.params['name'][0].word
    baseName = None
    if 'base_name' in match.params:
      baseName = match.params['base_name'][0].word
    cl = core.ClassNode(name, baseName)

    self.runHandlers(cl, match.handlers, source)

    return cl

  # OTHER RULES

  def createArrayValue(self, match, source):
    value = match.params['value'][0].word
    index = match.params['index'][0].word
    return core.ArrayValueNode(value, index)

  def createArrayBody(self, match, source):
    nodes = self.nodesByHandlers(match.handlers, source)
    
    if len(nodes) == 0:
      leftToken = source.tokens[match.leftIndex]
      raise Exception('createArrayBody nodes == 0, begin token "%s", linenum "%d", source "%s"' % (leftToken.word, leftToken.linenum, source.filename))

    return nodes[0]

  def createDictBody(self, match, source):
    nodes = self.nodesByHandlers(match.handlers, source)

    return nodes[0]

  def createDictValue(self, match, source):
    value = match.params['value'][0].word
    hsh = match.params['hsh'][0].word
    return core.DictValueNode(value, hsh)

  def createInsert(self, match, source):
    """
    Create core.InsertNode
    """
    name = match.params['name'][0].word

    ins = core.InsertNode(name)

    self.runHandlers(ins, match.handlers, source)

    return ins

  def matchInsertBody(self, left, right, source):
    """
    Match to ; or to right
    """
    rightParse = right
    rightEnd = right

    # find ;
    semicolonIndex = findWordIndex(';', left, right, source.tokens)
    if semicolonIndex >= 0:
      rightParse = semicolonIndex - 1
      rightEnd = semicolonIndex

    # compose match
    match = Match(left, rightEnd)
    match.handlers['parseInsertBody'] = Match(left, rightParse)

    return match

  def parseInsertBody(self, ins, left, right, source):
    """
    Add value to core.InsertNode, after or before expression.
    """
    # cursor for parsing after before where
    cursor = left
    # right cursor for parsing value expression
    rightCursor = right

    # search after word
    afterIndex = findWordIndex('after', left, right, source.tokens)
    if afterIndex >= 0:
      ins.setAfter()
      cursor = afterIndex + 1
      rightCursor = afterIndex - 1

    # search before word
    beforeIndex = findWordIndex('before', left, right, source.tokens)
    if beforeIndex >= 0:
      ins.setBefore()
      cursor = beforeIndex + 1
      rightCursor = beforeIndex - 1

    # parse value expression
    value = self.createExpression(Match(left, rightCursor), source)
    ins.setValue(value)

    # parse where expression
    if afterIndex >= 0 or beforeIndex >= 0:
      where = self.createExpression(Match(cursor, right), source)
      ins.setWhere(where)

  def createSelectCount(self, match, source):
    """
    Create core.SelectCountNode
    """
    name = match.params['name'][0].word
    selectCount = core.SelectCountNode(name)

    return selectCount

  def createSelectOne(self, match, source):
    """
    Create core.SelectOneNode
    """
    name = match.params['name'][0].word
    selectOne = core.SelectOneNode(name)

    self.runHandlers(selectOne, match.handlers, source)

    return selectOne

  def matchSelectOneBody(self, left, right, source):
    """
    Match to ; or right
    """
    rightCursor = right
    rightEnd = right

    semicolonIndex = findWordIndex(';', left, right, source.tokens)
    if semicolonIndex >= 0:
      rightCursor = semicolonIndex - 1
      rightEnd = semicolonIndex

    match = Match(left, rightEnd)
    match.handlers['parseSelectOneBody'] = Match(left, rightCursor)

    return match

  def parseSelectOneBody(self, selectOne, left, right, source):
    """
    Add where to selectOne node.
    """
    expr = self.createExpression(Match(left, right), source)
    selectOne.setWhere(expr)

  def createSelectFrom(self, match, source):
    """
    Create core.SelectFromNode
    """
    name = match.params['name'][0].word
    selectFrom = core.SelectFromNode(name)

    self.runHandlers(selectFrom, match.handlers, source)

    return selectFrom

  def matchSelectFromBody(self, leftIndex, rightIndex, source):
    """
    Return match.
    """
    rightCursor = rightIndex
    rightEnd = rightIndex

    semicolonIndex = findWordIndex(';', leftIndex, rightIndex, source.tokens)
    if semicolonIndex >= 0:
      rightCursor = semicolonIndex - 1
      rightEnd = semicolonIndex

    match = Match(leftIndex, rightEnd)
    match.handlers['parseSelectFromBody'] = Match(leftIndex, rightCursor)

    return match

  def createSelectConcat(self, match, source):
    """
    Create core.SelectConcatNode.
    """
    selectConcat = core.SelectConcatNode()

    self.runHandlers(selectConcat, match.handlers, source)

    return selectConcat

  def matchSelectConcatBody(self, left, right, source):
    """
    Return match.
    """
    match = Match(left, right)
    match.handlers['parseSelectConcatBody'] = Match(left, right)

    return match

  def createUpdate(self, match, source):
    """
    Create core.UpdateNode
    """
    name = match.params['name'][0].word
    upd = core.UpdateNode(name)

    self.runHandlers(upd, match.handlers, source)

    return upd

  def matchUpdateBody(self, left, right, source):
    """
    Match to ; or to right
    """
    rightParse = right
    rightEnd = right

    # find ;
    semicolonIndex = findWordIndex(';', left, right, source.tokens)
    if semicolonIndex >= 0:
      rightParse = semicolonIndex - 1
      rightEnd = semicolonIndex

    # compose match
    match = Match(left, rightEnd)
    match.handlers['parseUpdateBody'] = Match(left, rightParse)

    return match

  def parseUpdateBody(self, upd, left, right, source):
    """
    Add set items and where expression to update.
    """
    # search where
    whereIndex = findWordIndex('where', left, right, source.tokens)
    if whereIndex < 0:
      raise Exception('parse update body error, where not found, linenum "%d", source "%d"' % (source.tokens[left].linenum, source.filename))

    # parse where
    where = self.createExpression(Match(whereIndex+1, right), source)
    upd.setWhere(where)

    # parse set items
    cursor = left
    while cursor < whereIndex:
      rightCursor = whereIndex - 1
      rightEnd = rightCursor
      # find ,
      commaIndex = findCommaIndex(cursor, rightEnd, source.tokens)
      if commaIndex >= 0:
        rightCursor = commaIndex - 1
        rightEnd = commaIndex

      nameToken = source.tokens[cursor]
      if nameToken.wordtype != 'name':
        raise Exception('Update set must begin from name token, actual "%s", linenum "%d", source "%s"' % (nameToken.wordtype, nameToken.linenum, source.filename))

      equalIndex = cursor + 1
      leftExprIndex = cursor + 2
      if (equalIndex > rightCursor) or (leftExprIndex > rightCursor):
        raise Exception('Update set not enough tokens, linenum "%d", source "%s"' % (nameToken.linenum, source.filename))

      equalToken = source.tokens[equalIndex]
      if equalToken.wordtype != '=':
        raise Exception('Update set not found = after name, actual "%s", linenum "%d", source "%s"' % (equalToken.wordtype, equalToken.linenum, source.filename))

      expr = self.createExpression(Match(cursor+2, rightCursor), source)
      name = nameToken.word

      # add set item
      upd.addItem(name, expr)

      cursor = rightEnd + 1

  def createDeleteFrom(self, match, source):
    """
    Create core.DeleteFromNode.
    """
    name = match.params['name'][0].word
    deleteFrom = core.DeleteFromNode(name)

    self.runHandlers(deleteFrom, match.handlers, source)

    return deleteFrom

  def createSelectSum(self, match, source):
    """
    Create core.SelectSumNode.
    """
    name = match.params['name'][0].word
    by = match.params['by'][0].word

    selectSum = core.SelectSumNode(name, by)

    return selectSum

  def matchDeleteFromBody(self, left, right, source):
    """
    Return match. Search ;.
    """
    rightParse = right
    rightEnd = right

    semicolonIndex = findWordIndex(';', left, right, source.tokens)
    if semicolonIndex >= 0:
      rightParse = semicolonIndex - 1
      rightEnd = semicolonIndex

    if source.tokens[left].word != 'where':
      raise Exception('delete from body, where not found, linenum "%d", source "%s"' % (source.tokens[left].linenum, source.filename))

    match = Match(left, rightEnd)
    match.handlers['parseDeleteFromBody'] = Match(left, rightParse)

    return match

  def parseDeleteFromBody(self, deleteFrom, left, right, source):
    """
    Add where expression to deleteFrom node.
    """
    leftToken = source.tokens[left]
    whereIndex = findWordIndex('where', left, right, source.tokens)

    if whereIndex < 0:
      raise Exception('delete from not found where keyword, linenum "%d", source "%s"' % (leftToken.linenum, source.filename))

    if right - whereIndex < 1:
      raise Exception('delete from where not found expression, linenum "%d", source "%s"' % (leftToken.linenum, source.filename))

    expr = self.createExpression(Match(whereIndex+1, right), source)
    deleteFrom.setWhere(expr)

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

  def createIf(self, match, source):
    """
    Create core.IfNode.
    """
    ifNode = core.IfNode()

    self.runHandlers(ifNode, match.handlers, source)

    return ifNode
      
  def matchIfBody(self, left, right, source):
    leftToken = source.tokens[left]

    curlyIndex = findWordIndex('{', left, right, source.tokens)
    if curlyIndex < 0:
      return None

    exprMatch = Match(left, curlyIndex-1)

    bracketCounter = BracketCounter()

    # search close curly
    closeCurlyIndex = bracketCounter.findPair(curlyIndex, right, source.tokens)
    if closeCurlyIndex < 0:
      return None

    bodyMatch = Match(curlyIndex+1, closeCurlyIndex-1)

    rightEnd = closeCurlyIndex

    # search else
    elseMatch = None
    elseIndex = closeCurlyIndex + 1
    if (elseIndex < right) and (source.tokens[closeCurlyIndex+1].word == 'else'):
      elseOpen = elseIndex + 1
      if source.tokens[elseOpen].word != '{':
        raise Exception('else must have { }, linenum "%d", source "%s"' % (leftToken.linenum, source.filename))
      elseClose = bracketCounter.findPair(elseOpen, right, source.tokens)

      # create else Match

      elseMatch = Match(elseOpen+1, elseClose-1)
      rightEnd = elseClose

    # create mathces

    match = Match(left, rightEnd)
    match.handlers['parseIfExpr'] = exprMatch
    match.handlers['parseIfBody'] = bodyMatch
    if elseMatch != None:
      match.handlers['parseElseBody'] = elseMatch

    return match

  def parseIfExpr(self, ifNode, left, right, source):
    expr = self.createExpression(Match(left, right), source)
    ifNode.expr = expr

  def parseIfBody(self, ifNode, left, right, source):
    if (right - left) <= 1: return

    # bodyRule = grammar.getRule('function_body')
    nodes = self.parseByRules(grammar.function_body_rules, left, right, source)

    ifNode.body = nodes

  def parseElseBody(self, ifNode, left, right, source):
    if (right - left) <= 1: return

    # bodyRule = grammar.getRule('function_body')
    nodes = self.parseByRules(grammar.function_body_rules, left, right, source)

    ifNode.elseBody = nodes

  def createFor(self, match, source):
    """
    Create core.ForNode.
    """
    node = core.ForNode()
    self.runHandlers(node, match.handlers, source)
    return node

  def matchIterationBody(self, left, right, source):
    bracket = findWordIndex('{', left, right, source.tokens)
    if bracket < 0: return None

    endIndex = bracket - 1

    match = Match(left, endIndex)
    match.handlers['parseIterationBody'] = Match(left, endIndex)

    return match

  def parseIterationBody(self, forNode, left, right, source):
    # check min tokens count
    leftToken = source.tokens[left]
    if right - left < 2:
      raise Exception('for iteration body must have 3 tokens, linenum, "%d", source "%s"' % (leftToken.linenum, source.filename))

    # check "in" token
    inToken = source.tokens[right-1]
    if inToken.word != 'in':
      raise Exception('for iteration body not have "in" keyword, linenum, "%d", source "%s"' % (inToken.linenum, source.filename))

    rightToken = source.tokens[right]

    # save itemName, collName
    itemName = leftToken.word
    collName = rightToken.word

    forNode.itemName = itemName
    forNode.collName = collName


  def matchForBody(self, left, right, source):
    leftToken = source.tokens[left]
    if leftToken.word != '{': return None

    bracketCounter = BracketCounter()
    endIndex = bracketCounter.findPair(left, right, source.tokens)
    if endIndex < 0: return None

    match = Match(left, endIndex)
    match.handlers['parseForBody'] = Match(left+1, endIndex-1)

    return match

  def parseForBody(self, forNode, left, right, source):
    if right - left <= 1: return

    nodes = self.parseByRules(grammar.function_body_rules, left, right, source)

    forNode.body = nodes

  def createWhile(self, match, source):
    """
    Create core.WhileNode.
    """
    node = core.WhileNode()
    self.runHandlers(node, match.handlers, source)
    return node

  def matchWhileExpression(self, left, right, source):
    leftToken = source.tokens[left]
    bracketIndex = findWordIndex('{', left, right, source.tokens)
    if bracketIndex < 0:
      raise Exception('while expression not have { bracket, linenum "%s", source "%s"' % (leftToken.linenum, source.filename))

    match = Match(left, bracketIndex - 1)
    match.handlers['parseWhileExpression'] = Match(left, bracketIndex - 1)

    return match

  def parseWhileExpression(self, whileNode, left, right, source):
    if right - left <= 1: return

    whileNode.expr = self.createExpression(Match(left, right), source)

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
      if not (nameToken.wordtype in ['name', 'class', 'count']):
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
    rightEnd = rightIndex
    leftToken = source.tokens[leftIndex]

    if leftToken.word != '[':
      return None

    # find ']'
    bracketCounter = BracketCounter()
    closeIndex = bracketCounter.findPair(leftIndex, rightIndex, source.tokens)
    if closeIndex < 0:
      rawTokens = tokensToString(source.tokens[leftIndex:rightIndex+1])
      raise Exception('not found "]" for array_body, linenum "%d", source "%s", tokens "%s"' % (leftToken.linenum, source.filename, rawTokens))

    # check ; after ]
    nextIndex = closeIndex + 1
    if nextIndex <= rightIndex and source.tokens[nextIndex].word == ';':
      rightEnd = nextIndex

    # compose match
    match = Match(leftIndex, rightEnd)
    # if (closeIndex - leftIndex) > 1:
    match.handlers['parseArrayBody'] = Match(leftIndex+1, closeIndex-1)
    return match

  def matchDictBody(self, leftIndex, rightIndex, source):
    """
    Return match to { and } and check ;
    """
    rightCursor = rightIndex
    rightEnd = rightIndex
    leftToken = source.tokens[leftIndex]

    if leftToken.word != '{':
      return None

    # find '}'
    bracketCounter = BracketCounter()
    closeIndex = bracketCounter.findPair(leftIndex, rightIndex, source.tokens)
    if closeIndex < 0:
      raise Exception('not found "}" for dict_body, linenum "%d", source "%s"' % (leftToken.linenum, source.filename))

    # check ; after }
    nextIndex = closeIndex + 1
    if nextIndex <= rightIndex and source.tokens[nextIndex].word == ';':
      rightEnd = nextIndex

    # compose match
    match = Match(leftIndex, rightEnd)
    # if (closeIndex - leftIndex) > 1:
    match.handlers['parseDictBody'] = Match(leftIndex+1, closeIndex-1)
    return match

  def matchFunctionParams(self, leftIndex, rightIndex, source):
    if source.tokens[leftIndex].word == '(':
      bracketCounter = BracketCounter()
      closeIndex = bracketCounter.findPair(leftIndex, rightIndex, source.tokens)
      match = Match(leftIndex, closeIndex)
      match.handlers['parseFunctionParams'] = Match(leftIndex+1, closeIndex-1)
      return match
    return None

  def matchFunctionBody(self, leftIndex, rightIndex, source):
    if source.tokens[leftIndex].word == '{':
      bracketCounter = BracketCounter()
      closeIndex = bracketCounter.findPair(leftIndex, rightIndex, source.tokens)
      match = Match(leftIndex, closeIndex)
      match.handlers['parseFunctionBody'] = Match(match.leftIndex+1, closeIndex-1)
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

  def matchEnumBody(self, leftIndex, rightIndex, source):
    """
    Match { and }
    """
    if source.tokens[leftIndex].word == '{':
      bracketCounter = BracketCounter()
      closeIndex = bracketCounter.findPair(leftIndex, rightIndex, source.tokens)
      match = Match(leftIndex, closeIndex)
      match.handlers['parseEnumBody'] = Match(match.leftIndex+1, closeIndex-1)
      return match
    return None

  def matchStructBody(self, leftIndex, rightIndex, source):
    """
    Match { and }
    """
    if source.tokens[leftIndex].word == '{':
      bracketCounter = BracketCounter()
      closeIndex = bracketCounter.findPair(leftIndex, rightIndex, source.tokens)
      match = Match(leftIndex, closeIndex)
      match.handlers['parseStructBody'] = Match(match.leftIndex+1, closeIndex-1)
      return match
    return None

  def matchClassBody(self, leftIndex, rightIndex, source):
    """
    Match class body, left token must be { and right token must be }
    """
    if source.tokens[leftIndex].word == '{':
      bracketCounter = BracketCounter()
      closeIndex = bracketCounter.findPair(leftIndex, rightIndex, source.tokens)
      match = Match(leftIndex, closeIndex)
      match.handlers['parseClassBody'] = Match(match.leftIndex+1, closeIndex-1)
      return match
    return None

  def createConstructor(self, match, source):
    """
    Create core.FunctionNode with decltype and name is None
    """
    con = core.FunctionNode(decltype=None, name=None)

    self.runHandlers(con, match.handlers, source)

    return con
    

  def createConstructorCall(self, match, source):
    """
    Create constructor (function) node.
    """
    name = match.params['name'][0].word
    con = core.FunctionCallNode(name)

    self.runHandlers(con, match.handlers, source)

    return con

  def matchConstructorInit(self, leftIndex, rightIndex, source):
    """
    Return match between "{" and "} or ;"
    """
    leftToken = source.tokens[leftIndex]
    if leftToken.word == '{':
      # search }
      bracketCounter = BracketCounter()
      closeIndex = bracketCounter.findPair(leftIndex, rightIndex, source.tokens)

      # check it must exists
      if closeIndex < 0:
        raise Exception('matchConstructorInit: not found }, linenum "%d", source "%s"' % (leftToken.linenum, source.filename))

      # match right end index
      rightEnd = closeIndex

      # search ;
      semicolonIndex = closeIndex + 1
      if semicolonIndex <= rightIndex and source.tokens[semicolonIndex].word == ';':
        rightEnd = semicolonIndex

      # compose match
      match = Match(leftIndex, rightEnd)
      match.handlers['parseConstructorInit'] = Match(leftIndex+1, closeIndex-1)
      return match

    return None

  def createVariableAssign(self, match, source):
    """
    Create core.ValueNode.
    """
    name = match.params['name']
    value = core.ValueNode(name)
    value.isName = True

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
    match.params['name'] = nameToken.word
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

    rightEnd = match.rightIndex
    if source.tokens[match.rightIndex].word == ';':
      rightEnd = match.rightIndex - 1

    nodes = []
    bracketWeight = 0
    while cursor <= rightEnd:
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

        # DEBUG
        bracketToken = source.tokens[funcMatch.rightIndex]
        if bracketToken.word!= '(':
          raise Exception('funcMatch ok mut funcMatch.rightIndex not "(", actual "%s", linenum "%d", leftIndex "%d", rightIndex "%d"' % (bracketToken.word, bracketToken.linenum, match.leftIndex, match.rightIndex))

        closedIndex = bracketCounter.findPair(funcMatch.rightIndex, match.rightIndex, source.tokens)
        if closedIndex < 0:
          raise Exception('not found closed bracket ), cursor "%d", linenum "%s", source "%s"' % (cursor, token.linenum, source.filename))
        nodes.append({'kind': 'function', 'match': Match(funcMatch.leftIndex, closedIndex), 'weight': grammar.functionsWeight['function'] + bracketWeight})
        # move cursor after function call
        cursor = closedIndex + 1
        continue
      # add variable
      if token.wordtype in ['name', 'litint', 'litfloat', 'litstring', 'litbool', 'none', 'asc', 'order', 'after', 'before', 'count']:
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
    leftCursor = leftIndex
    arrayBody = core.ArrayBodyNode()
    while leftCursor <= rightIndex:
      rightCursor = rightIndex
      endCursor = rightIndex
      # find ,
      commaIndex = findCommaIndex(leftCursor, rightIndex, source.tokens)
      if commaIndex >= 0:
        endCursor = commaIndex
        rightCursor = commaIndex - 1

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

  def parseDictBody(self, leftIndex, rightIndex, source):
    """
    Create core.DictBodyNode, create by variable_body_rules.
    """
    leftCursor = leftIndex
    dictBody = core.DictBodyNode()
    while leftCursor <= rightIndex:
      rightCursor = rightIndex
      endCursor = rightIndex
      # find ,
      commaIndex = findCommaIndex(leftCursor, rightIndex, source.tokens)
      if commaIndex >= 0:
        rightCursor = commaIndex - 1
        endCursor = commaIndex

      # find key, first token must be litstring
      leftToken = source.tokens[leftCursor]
      if not (leftToken.wordtype in ['litint', 'litstring', 'name']):
        raise Exception('Dict key in dict_body must be litint, litstring, name types, actual "%s", linenum "%d", source "%s"' % (leftToken.wordtype, leftToken.linenum, source.filename))
      keyName = leftToken.word

      # find ;
      nextIndex = leftCursor + 1
      if nextIndex <= rightIndex and source.tokens[nextIndex].word == ':':
        # add dict item
        nodes = self.parseByRules(grammar.variable_body_rules, nextIndex+1, rightCursor, source)
        dictBody.addItem(keyName, nodes[0])
      else:
        raise Exception('dict_body after key must follow ":", linenum "%d", source "%s"' % (leftToken.linenum, source.filename))

      # shift cursors
      leftCursor = endCursor + 1
    return dictBody

  def parseVariableBody(self, var, leftIndex, rightIndex, source):
    # search = or :=
    cursorLeft = leftIndex
    firstToken = source.tokens[leftIndex]

    if firstToken.word in ['=', ':=']:
      # set body reactive
      if firstToken.word == ':=':
        var.setBodyReactive(True)
      cursorLeft = leftIndex + 1

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
        raise Exception('not parse function params, source "%s", linenum "%d", tokens "%s"' % (source.filename, source.tokens[leftIndex].linenum, tokensToString(source.tokens[cursor:rightIndex+1])))
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
      match = matchNodes(enumVarRule, cursor, rightIndex, source)
      if match == None: break
      # add enum member
      name = match.params['name'][0].word
      value = match.params['value'][0].word
      en.addMember(name, value)
      # move cursor to next
      cursor = match.rightIndex + 1

  def parseStructBody(self, st, leftIndex, rightIndex, source):
    """
    Add core.StructVariableNode to st.
    """
    # check if struct have body
    if (rightIndex - leftIndex) == 1: return

    structVarRule = grammar.getRule('struct_variable')
    cursor = leftIndex

    while cursor <= rightIndex:
      leftToken = source.tokens[cursor]

      # find ;
      semicolonIndex = findWordIndex(';', cursor, rightIndex, source.tokens)
      if semicolonIndex < 0:
        raise Exception('struct variable not found ;, linenum "%d", source "%s"' % (leftToken.linenum, source.filename))

      # match struct variable nodes
      match = matchNodes(structVarRule, cursor, semicolonIndex-1, source)
      if match == None:
        raise Exception('no matches found for struct variable body, first token "%s", linenum "%d", source "%s"' % (leftToken.word, leftToken.linenum, source.filename))

      # add struct variable
      decltype = match.params['type']
      name = match.params['name'][0].word
      var = core.StructVariableNode(decltype, name)

      # add strut variables params
      self.runHandlers(var, match.handlers, source)

      # add variable to struct
      st.addVariable(var)

      # shift cursor
      cursor = semicolonIndex + 1

  def parseClassBody(self, cl, leftIndex, rightIndex, source):
    """
    Add to cl constructor, variables, functions
    """
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
    dictBody = self.parseDictBody(leftIndex, rightIndex, source)
    for name, item in dictBody.items.items():
      con.addInit(name, item)

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

      orderByParamRule = grammar.getRule('orderby_param')
      match = matchNodes(orderByParamRule, orderIndex+2, rightIndex, source)
      if not match:
        raise Exception('select from order by param error, linenum "%d", source "%s"' % (byToken.linenum, source.filename))

      paramName = match.params['name'][0].word
      paramOrder = match.params['order'][0].word

      selectFrom.setOrderField(paramName, paramOrder)

  def parseSelectConcatBody(self, selectConcat, left, right, source):
    """
    Add to selectConcat collections.
    """
    cursor = left
    while cursor <= right:
      cursorToken = source.tokens[cursor]
      if not (cursorToken.wordtype in [',', 'name']):
        raise Exception('select concat body unknown tokey wordtype, actual "%s", linenum "%d", source "%s"' % (cursorToken.wordtype, cursorToken.linenum, source.filename))
      if cursorToken.wordtype == 'name':
        name = cursorToken.word
        selectConcat.addCollection(name)
      cursor = cursor + 1

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
        closeBracket = bracketCounter.findPair(openBracket, rightCursor, source.tokens)
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
      self.parseCallParams(createNode, match.leftIndex, match.rightIndex, source)
    elif kind in grammar.unaryFunctions:
      createNode = core.FunctionCallNode(kind)
      # parse right indexes
      paramNode = self.createExpressionTree(minIndex + 1, rightIndex, nodes, source)
      createNode.addParameter(paramNode)
    elif kind in grammar.binaryFunctions:
      createNode = core.FunctionCallNode(kind)
      leftParam = self.createExpressionTree(leftIndex, minIndex - 1, nodes, source)
      rightParam = self.createExpressionTree(minIndex + 1, rightIndex, nodes, source)
      createNode.addParameter(leftParam)
      createNode.addParameter(rightParam)
    else:
      # we have value node
      leftToken = source.tokens[match.leftIndex]
      createNode = core.ValueNode(leftToken.word)
      wt = leftToken.wordtype
      # set value flag type
      if wt == grammar.LITBOOL_TYPE:
        createNode.isLitBool = True
      elif wt == grammar.LITINT_TYPE:
        createNode.isLitInt = True
      elif wt == grammar.LITFLOAT_TYPE:
        createNode.isLitFloat = True
      elif wt == grammar.LITSTRING_TYPE:
        createNode.isLitString = True
      elif wt == grammar.NAME_TYPE:
        createNode.isName = True
      else:
        # raise Exception('unknown wordtype for ValueNode, actual "%s", source "%s"' % (wt, source.filename))
        # exists asc|desc, none
        pass

    if createNode == None:
      raise Exception('created node in expression is None, source "%s"' % source.filename)

    return createNode

  def parseCallParams(self, fncall, leftIndex, rightIndex, source):
    """
    Every params parse as expression, divide by comma.
    """
    leftToken = source.tokens[leftIndex]
    # check left bracket
    if source.tokens[leftIndex+1].word != '(':
      raise Exception('function call without open bracket, instead bracket we have "%s", linenum "%d", source "%s"' % (source.tokens[leftIndex+1].word, leftToken.linenum, source.filename))
    # check right bracket
    if source.tokens[rightIndex].word != ')':
      raise Exception('function call without close bracket, linenum "%d", source "%s"' % (leftToken.linenum, source.filename))
    # shift right from "name ("
    leftCursor = leftIndex + 2
    # shift left from ")"
    rightEnd = rightIndex - 1
    while leftCursor <= rightEnd:
      rightCursor = rightEnd
      # find ,
      commaIndex = findCommaIndex(leftCursor, rightCursor, source.tokens)
      if commaIndex >= 0:
        rightCursor = commaIndex - 1
      # parse expression and add it to params
      param = self.createExpression(Match(leftCursor, rightCursor), source)
      # add param to function call node
      fncall.addParameter(param)
      # move leftCursor
      if commaIndex >= 0:
        leftCursor = commaIndex + 1
      else:
        leftCursor = rightCursor + 1

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
