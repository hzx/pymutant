

SYMBOL_TOKENS = [
    '(', ')', '{', '}', '[', ']',
    ':=', '+=', '-=', '*=', '/=', '>=', '<=',
    '</', '/>',
    '.', ',', ';', ':', '"', "'", '#',
    '^', '=', '+', '-', '*', '/', '\\', '!', '?', '@', '>', '<', '%',
    # '~',
    ]

SYSTEM_TOKENS = [
    'import', 'extern', 'return',
    'var', 'bool', 'int', 'float', 'string',
    'true', 'false', 'return',
    'class', 'struct', 'enum', 'optional', 'extends',
    # use map instead and {value1: func1, value2: func2}'if', 'else',
    'select', 'concat', 'from', 'where', 'and', 'or', 'is', 'in', 'not', 'order', 'by', 
    'map', 'reduce',
    ]

HTML_TOKENS = [
    'div', 'span', 'p', 'h1', 'h2', 'h3',
    'onclick',
    ]

ALPHA_RE = '[\ a-zA-Z_0-9\(\)\{\}\[\]\.\,\;\:"\'\^\=\+\-\*/\\\!\?@><%#]'

# regexes
IDENT_RE = '[a-zA-Z_][a-zA-Z_0-9]*'
IDENT_TYPE = 'identifier'

# TODO(dem) replace DIGIT_RE by INT_RE and FLOAT_RE
INT_RE = '[0-9]+'
INT_TYPE = 'intdigit'
FLOAT_RE = '[0-9]+\.[0-9]+'
FLOAT_TYPE = 'floatdigit'

DIGIT_RE = '[0-9]+\.?[0-9]*'
DIGIT_TYPE = 'digit'
STRING_RE = '\"[^".]*\"|\'[^\'.]*\''
STRING_TYPE = 'strlit'

"""
Grammar consists of regex like syntax.
Placeholders {{expression_name}} must be replaced.
"""
GRAMMAR = [
    { "contexttype": "var" },
    { "type": "bool|int|float|string" },
    { "complextype": "{{type}}[]|identifier[]" }, 
    { "var": "{{type}} identifier (= expression)? ;" },
    { "arr": "[ (identifier `,`)* ]" },
    { "dic": "{ (identifier : expression `,`)* }" },
    { "func": "identifier ( (identifier `,`)* ) { (expression `;`)* (return expression ;)? }" },
    { "anonfunc": "( (identifier `,`)* ) { (expression `;`)* (return expression ;)? }" },
    { "enum": "enum identifier { (identifier = digit ;)* }" },
    { "struct": "struct identifier { (identifier = expression ;)* }" },
    { "class": "class identifier { ({{anonfunc}})?|(identifier = expression ;)*|({{func}})* }" },
    { "classinstance": "identifier ( (identifier `,`)* ) ({ (identifier = expression `,`)* })? ;" },
    { "selfrom": "select from identifier (where expression)? (order by identifier)?" },
    { "selconc": "select concat ( (grselfrom `,`)+ )" },
    { "tag": "< identifier (style = { (identifier : strlit `,`)? })? > (expression)? </ identifier >" },
    { "tagsingle": "< identifier />" },
    ]

"""
Declare grammar.
"""

GR_TYPE = "var|bool|int|float|string|identifier ([])?"
GR_TYPE_NAME = "type"

GR_VARIABLE = "{{type}}"
GR_VARIABLE_NAME = "variable"

GR_PARAMS = ""
GR_PARAMS_NAME = "params"

GR_FUNCTION = "{{type}} identifier ( ({{params}})* ) {}"
GR_FUNCTION_NAME = "function"

GR_ENUM = "enum identifier { (identifier = )* }"
GR_ENUM_NAME = "enum"

GR_STRUCT = ""
GR_STRUCT_NAME = "struct"

GR_CLASS = ""
GR_CLASS_NAME = "class"

GR_SELECTFROM = "select from identifier where ()+ (order by (identifier `,`)*)?"
GR_SELECTFROM_NAME = "selectfrom"

GR_SELECTCONCAT = "select concat ( ({{params}})+ )"
GR_SELECTCONCAT_NAME = "selectconcat"

gr_tagattrs = ""
gr_tagattrsname = "tagattrs"

gr_tag = "< identifier {{tagattrs}} > ({{tag}}|{{singletag}})* </ identifier >"
gr_tag_name = "tag"

gr_singletag = "< identifier {{tagattrs}} />"
gr_singletag_name = "singletag"
