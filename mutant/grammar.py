
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
    'void', 'var', 'bool', 'int', 'float', 'string', 'tag', 'event', 'object', 'robject',
    'true', 'false', 'return', 'none',
    'static', 'interface', 'class', 'struct', 'enum', 'optional', 'extends',
    'implements',
    #'this',
    'if', 'else', 'for', 'while',
    'insert', 'select', 'concat', 'update', 'delete', 'count', 'one', 'value', 'set', 'from', 'where', 'and', 'or', 'is', 'isnot', 'in', 'not', 'order', 'by', 'before', 'after', 'asc', 'desc',
    'map', 'reduce', 'sum',
    ]

HTML_TAGS = [
    'div', 'span', 'p', 'img', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'input', 'textarea', 'strong', 'ul', 'ol', 'li', 'tr', 'th', 'td', 'br',
    ]

HTML_EVENTS = [
    'onload', 'onunload', 'onclick', 'onhover',
    ]

ALPHA_RE = '[\ a-zA-Z0-9_\(\)\{\}\[\]\.\,\;\:\'\^\=\+\-\*/\\\?><#!%]'

SIMPLE_TYPES = ['bool','int','float','string','datetime','tag','event', 'name', 'object', 'robject']
VALUE_TYPES = ['bool', 'int', 'float', 'string', 'datetime']

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
    'variable': '<type>(var|{type}) <name>(name|order|event|class|count) {variable_body}!',
    'function': '{function_type} ({function_name})? {function_params}! {function_body}!',
    'enum': 'enum <name>(name) {enum_body}!',
    'interface': 'interface <name>(name) {interface_body}!',
    'struct': 'struct <name>(name) ({struct_extends})? {struct_body}!',
    'class': 'class <name>(name) ({class_extends})? {class_body}!',

    'function_declaration': '{function_type} {function_params}! {function_body}!',
    'function_type': '<type>(void|{type})',
    'function_name': '<name>(name|insert|select|concat|update|delete|count)',
    'function_param': '<type>(var|{type}) <name>(name|order|after|before|count|event)',
    'function_return': 'return ({operator}!)?',
    'function_call': '<name>(name|int|float) (',

    'struct_variable': '<type>({type}) <name>(name) {constructor_init}!',

    # 'constructor': '({function_params})! {function_body}!',
    # 'constructor': '( ) {function_body}!',
    'constructor': '{function_params}! {function_body}!',
    'constructor_call': '<name>(name) ( ) {constructor_init}!',

    'variable_assign': '{match_variable_assign}!',

    'enum_var': '<name>(name) = <value>(litint) ;',
    'struct_extends': 'extends <base_name>(name)',
    'class_extends': 'extends <base_name>(name|tag)',
    'order_by': '<order_field>(name)',

    'simple_type': 'bool|int|float|string|datetime|tag|event|name|object|robject',
    'array_type': '{simple_type} [ ]',
    'dict_type': '{ {simple_type} : {simple_type} }',
    'type': '{dict_type}|{array_type}|{simple_type}',

    'array_value': '<value>(name) [ <index>(litint) ]',
    'array_body': '{match_array_body}!',
    'dict_body': '{match_dict_body}!',

    'insert': 'insert <name>(name) value {insert_body}!',
    'select_count': 'select count <name>(name)',
    'select_one': 'select one <name>(name) where {selectone_body}!',
    'select_from': 'select from <name>(name) {selectfrom_body}!',
    'select_concat': 'select concat {selectconcat_body}!',
    'update': 'update <name>(name) set {update_body}!',
    'delete_from': 'delete from <name>(name) {deletefrom_body}!',
    #return select sum order.foods by price;
    'select_sum': 'select sum <name>(name) by <by>(name)',

    'orderby_param': '<name>(name) <order>(asc|desc)',

    'expression': '{expression_body}!',

    'tag': '{tag_body}!',

    'if': 'if {if_body}!',
    'for': 'for {iteration_body}! {for_body}!',
    'while': 'while {while_expression}! {for_body}!',
    }

unaryFunctions = ['not']
binaryFunctions = ['>', '<', '>=', '<=', 'is', 'isnot', 'and', 'or', '*', '/', '%', '+', '-']
functionNames = unaryFunctions + binaryFunctions
functionsWeight = {
    'function': 4,
    '>': 3,
    '<': 3,
    '>=': 3,
    '<=': 3,
    'is': 3,
    'isnot': 3,
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
variable_body_rules = ['constructor_call', 'insert', 'select_sum', 'select_count', 'select_one', 'select_from', 'select_concat', 'update', 'delete_from', 'tag', 'array_body', 'array_value', 'dict_body', 'expression']
function_body_rules = ['insert', 'update', 'delete_from', 'if', 'for', 'while', 'variable', 'variable_assign', 'function_return','expression']
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
