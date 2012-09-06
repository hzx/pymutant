

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

gr_type = "(var|bool|int|float|string|identifier){1}([])?"
gr_vars = "{{type}} identifier (= {{expression}})? ;"
gr_func = "( (identifier `,`)* ) { (expression `;`)* (return expression ;)? }"
