

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
INT_RE = '[0-9]+'
INT_TYPE = 'intdigit'
FLOAT_RE = '[0-9]+\.[0-9]+'
FLOAT_TYPE = 'floatdigit'
STRING_RE = '\"[^".]*\"|\'[^\'.]*\''
STRING_TYPE = 'strlit'

TYPE_NAME = "type"
TYPE = "var|bool|int|float|string|identifier ([])?"

CALLFUNC_NAME = "callfunc"
CALLFUNC = "identifier ( {callparams} )"

CALLOBJFUNC_NAME = "callobjfunc"
CALLOBJFUNC = "identifier.identifier ( {callparams} )"

MULT_NAME = 'mult'
MULT = '{expression} * {expression}'

MULTASSIGN_NAME = 'multassign'
MULTASSIGN = 'identifier *= {expression}'

DIV_NAME = 'div'
DIV = '{expression} / {expression}'

DIVASSIGN_NAME = 'divassign'
DIVASSIGN = 'identifier /= {expression}'

ADD_NAME = 'add'
ADD = '{expression} + {expression}'

ADDASSIGN_NAME = 'addassign'
ADDASSIGN = 'identifier += {expression}'

SUB_NAME = 'sub'
SUB = '{expression} - {expression}'

SUBASSIGN_NAME = 'subassign'
SUBASSIGN = 'identifier -= {expression}'

GREATER_NAME = 'greater'
GREATER = '{expression} > {expression}'

LESS_NAME = 'less'
LESS = '{expression} < {expression}'

GREATEREQUAL_NAME = 'greaterequal'
GREATEREQUAL = '{expression} >= {expression}'

LESSEQUAL_NAME = 'lessequal'
LESSEQUAL = '{expression} <= {expression}'

EXPRESSION_NAME = "expression"
EXPRESSION = "identifier|{callfunc}|identifier.identifier|{callobjfunc}|{multiply}|{divide}"

VARDECLARE_NAME = "vardeclare"
VARDECLARE = "{type} identifier (= {expression})? ;"

VARASSIGN_NAME = "varassign"
VARASSIGN = "identifier = {expression} ;"

MAPBODY_NAME = 'mapbody'
MAPBODY = '{ identifier : {variable}|{strlit} }'

PARAMS_NAME = "params"
PARAMS = "({type} identifier `,`)*"

CALLPARAMS_NAME = "callparams"
CALLPARAMS = "({expression} `,`)*"

FUNCTION_NAME = "function"
FUNCTION = "{type} identifier ( {params} ) {  }"

ENUM_NAME = "enum"
ENUM = "enum identifier { (identifier = {intdigit} ;)* }"

STRUCT_NAME = "struct"
STRUCT = "struct identifier { ({type} identifier ;)* }"

CONSTRUCTOR_NAME = "constructor"
CONSTRUCTOR = "( {params} ) {  }"

CLASS_NAME = "class"
CLASS = "class identifier (extends identifier)? { {constructor}|{variable}|{function} }"

SELECTORDERBY_NAME = 'selectorderby'
SELECTORDERBY = 'order by (identifier `,`)*'

SELECTFROM_NAME = "selectfrom"
SELECTFROM = "select from identifier where {expression} ({selectorderby})?"

CONCATPARAMS_NAME = "concatparams"
CONCATPARAMS = "({expression} `,`){2,}"

SELECTCONCAT_NAME = "selectconcat"
SELECTCONCAT = "select concat {concatparams}"

TAGATTRS_NAME = "tagattrs"
TAGATTRS = "identifier = {mapbody}|{variable}|{strlit}|identifier"

TAG_NAME = "tag"
TAG = "< identifier {tagattrs} > ({tag}|{singletag})* </ identifier >"

SINGLETAG_NAME = "singletag"
SINGLETAG = "< identifier {tagattrs} />"
