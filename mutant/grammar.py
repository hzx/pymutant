
SYMBOL_TOKENS = [
    '(', ')', '{', '}', '[', ']',
    ':=', '+=', '-=', '*=', '/=', '>=', '<=', '==', '!=',
    '</', '/>',
    '.', ',', ';', ':', '"', "'", '#',
    '^', '=', '+', '-', '*', '/', '\\', '!', '%', '?', '>', '<',
    # '~',
    ]

SYSTEM_TOKENS = [
    'define', 'import', 'extern', 'return', 'as',
    'void', 'var', 'bool', 'int', 'float', 'string', 'tag', 'event',
    'true', 'false', 'return', 'none',
    'static', 'interface', 'class', 'struct', 'enum', 'optional', 'extends',
    'implements', 'this',
    'if', 'else',
    'select', 'concat', 'from', 'where', 'and', 'or', 'is', 'in', 'not', 'order', 'by', 
    'map', 'reduce',
    'rmap',
    ]

HTML_TAGS = [
    'div', 'span', 'p', 'h1', 'h2', 'h3', 'ul', 'ol', 'li',
    ]

HTML_EVENTS = [
    'onload', 'onunload', 'onclick', 'onhover',
    ]

ALPHA_RE = '[\ a-zA-Z0-9_\(\)\{\}\[\]\.\,\;\:\'\^\=\+\-\*/\\\?><#!%]'

# Regexes

NAME_RE = '(?:[_a-zA-Z][_a-zA-Z0-9]*[.]?)+'
NAME_TYPE = 'name'
LITINT_RE = '[0-9]+'
LITINT_TYPE = 'litint'
LITFLOAT_RE = '[0-9]+\.[0-9]+'
LITFLOAT_TYPE = 'litfloat'
LITSTRING_RE = "'[^']*'"
LITSTRING_TYPE = 'litstring'
LITBOOL_LIST = ['true', 'false']
LITBOOL_TYPE = 'litbool'


rules = {
    'import': 'import <module>(name) as <alias>(name) ;',
    'define': 'define <alias>(name) {define_body}!',
    'variable': '<type>(var|{type}) <name>(name) {variable_body}!',
    'function': '{function_type} ({function_name})? {function_params}! {function_body}!',
    'enum': 'enum <name>(name) {enum_body}!',
    'struct': 'struct <name>(name) ({struct_extends})? {struct_body}!',
    'class': 'class <name>(name) ({class_extends})? {class_body}!',

    'function_declaration': '{function_type} {function_params}! {function_body}!',
    'function_type': '<type>(void|{type})',
    'function_name': '<name>(name)',
    'function_param': '<type>({type}) <name>(name)',
    'function_return': 'return ({operator}!)?',
    'function_call': '<name>(name) (',

    # 'constructor': '({function_params})! {function_body}!',
    'constructor': '( ) {function_body}!',
    'constructor_call': '<name>(name) ( ) {constructor_init}!',

    'variable_assign': '{match_variable_assign}!',

    'enum_var': '<name>(name) = <value>(litint) ;',
    'struct_extends': 'extends <base_name>(name)',
    'class_extends': 'extends <base_name>(name)',
    'order_by': '<order_field>(name)',

    'simple_type': 'bool|int|float|string|datetime|tag|event|name',
    'array_type': '{simple_type} [ ]',
    'dict_type': '{ {simple_type} : {simple_type} }',
    'type': '{array_type}|{simple_type}',

    'array_value': '<value>(name) [ <index>(litint) ]',
    'array_body': '{match_array_body}!',
    'dict_body': '{match_dict_body}!',

    'select_from': 'select from <name>(name) {selectfrom_body}!',
    'select_concat': 'select concat {selectconcat_body}!',

    'orderby_param': '<name>(name) <order>(name)',

    'expression': '{expression_body}!',

    # 'singletag': '< name {tagattrs}! />',
    # 'tag': '< name {tagattrs}! > {tag}! </ name >',
    'tag': '{tag_body}!',
    'tagContent': '<name>(name) {tagattrs}!',
    'tagattrs': '',

    'if': 'if {if_body}!',
    'map_item': '<name>(name) : {expression_body}!',
    }

unaryFunctions = ['not']
binaryFunctions = ['>', '<', '>=', '<=', '==', '!=', 'and', 'or', '*', '/', '%', '+', '-']
functionNames = unaryFunctions + binaryFunctions
functionsWeight = {
    'function': 4,
    '>': 3,
    '<': 3,
    '>=': 3,
    '<=': 3,
    '==': 3,
    '!=': 3,
    'not': 3,
    'and': 3,
    'or': 3,
    '*': 2,
    '/': 2,
    '%': 2,
    '+': 1,
    '-': 1,
    }
bracketWeight = 5

# empty, grammarparser store here compiled rules (above)
compiled = {}

# handled names
handlers = {}

global_rules = ['define', 'variable', 'function', 'enum', 'struct', 'class']
define_body_rules = ['function_declaration', 'type']
variable_body_rules = ['constructor_call', 'select_from', 'select_concat', 'tag', 'array_body', 'array_value', 'dict_body', 'expression']
function_body_rules = ['if', 'variable', 'variable_assign', 'function_return','expression']
enum_body_rules = ['enum_var']
struct_body_rules = ['variable']
class_body_rules = ['constructor', 'variable', 'function']
tag_child_rules = ['tag', 'expression']

def getRule(name):
  return compiled[name]

def getHandler(name):
  return handlers[name]

def setHandler(name, handler):
  handlers[name] = handler
