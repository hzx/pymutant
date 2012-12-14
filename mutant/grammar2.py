

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

    'constructor': '({function_params})! {function_body}!',
    'constructor_call': '<name>(name) {constructor_init}!',

    'enum_var': '<name>(name) = <value>(litint) ;',
    'struct_extends': 'extends <base_name>(name)',
    'class_extends': 'extends <base_name>(name)',
    'order_by': '<order_field>(name)',

    'simple_type': 'bool|int|float|string|datetime|tag|event|name',
    'array_type': '{simple_type} [ ]',
    'type': '{array_type}|{simple_type}',

    'select_from': 'select from {selectfrom_body}!',
    'select_concat': 'select concat {selectconcat_body}!',

    'expression_body': '{expression}!',

    # 'singletag': '< name {tagattrs}! />',
    # 'tag': '< name {tagattrs}! > {tag}! </ name >',
    'tag': '{tag}!',
    'tagContent': '<name>(name) {tagattrs}!',
    'tagattrs': '',

    'if': 'if {if_body}!',
    }

functionsWeight = {
    '>': 4,
    '<': 4,
    '>=': 4,
    '<=': 4,
    '==': 4,
    '!=': 4,
    'not': 4,
    'and': 4,
    'or': 4,
    'function': 3,
    '*': 2,
    '/': 2,
    '%': 2,
    '+': 1,
    '-': 1,
    }
bracketWeight = 5

# empty, grammarparser store here compiled rules (above)
compiled = {
    }

# handled names
handlers = {
    # global
    # other
    'variable_body': None,
    'operator': None,
    'function_params': None,
    'function_body': None,
    'enum_body': None,
    'struct_body': None,
    'class_body': None,
    'expression': None,
    'selectfrom_body': None,
    'selectconcat_body': None,
    'tagattrs': None,
    'tag': None,
    'if_body': None,
    }

global_rules = ['define', 'variable', 'function', 'enum', 'struct', 'class']
define_body_rules = ['function_declaration', 'type']
variable_body_rules = ['constructor_call', 'function_call', 'select_from', 'select_concat', 'tag', 'expression_body']
function_body_rules = ['if', 'variable', 'function_return','expression']
enum_body_rules = ['enum_var']
struct_body_rules = ['variable']
class_body_rules = ['constructor', 'variable', 'function']


def getRule(name):
  return compiled[name]

def getHandler(name):
  return handlers[name]

def setHandler(name, handler):
  handlers[name] = handler
