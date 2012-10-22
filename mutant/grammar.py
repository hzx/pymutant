

SYMBOL_TOKENS = [
    '(', ')', '{', '}', '[', ']',
    ':=', '+=', '-=', '*=', '/=', '>=', '<=',
    '</', '/>',
    '.', ',', ';', ':', '"', "'", '#',
    '^', '=', '+', '-', '*', '/', '^', '\\', '!', '%', '?', '>', '<',
    # '~',
    ]

SYSTEM_TOKENS = [
    'define', 'import', 'extern', 'return',
    'var', 'bool', 'int', 'float', 'string',
    'true', 'false', 'return', 'none',
    'static', 'interface', 'class', 'struct', 'enum', 'optional', 'extends',
    'implements',
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

NAME_RE = '[_a-zA-Z][_a-zA-Z0-9]*'
NAME_TYPE = 'name'
LITINT_RE = '[0-9]+'
LITINT_TYPE = 'litint'
LITFLOAT_RE = '[0-9]+\.[0-9]+'
LITFLOAT_TYPE = 'litfloat'
LITSTRING_RE = "'[^']*'"
LITSTRING_TYPE = 'litstring'

# Main grammar rules

VARIABLE_NAME = "variable"
VARIABLE = "var|{type} name (= {expression})? ;"

FUNCTION_NAME = "function"
FUNCTION = "({type})? (name)? ( {params} ) { {funcbody} }"

ENUM_NAME = "enum"
ENUM = "enum name { (name = {intdigit} ;)* }"

STRUCT_NAME = "struct"
STRUCT = "struct name { ({type} name ;)* }"

CLASS_NAME = "class"
CLASS = "class name (extends name)? { {constructor}|{variable}|{function} }"

SELECTFROM_NAME = "selectfrom"
SELECTFROM = "select from name where {expression} (order by {orderbyparams})?"

SELECTCONCAT_NAME = "selectconcat"
SELECTCONCAT = "select concat {concatparams}"

TAG_NAME = "tag"
TAG = "< name {tagattrs} > ({tag}|{singletag})* </ name >"

SINGLETAG_NAME = "singletag"
SINGLETAG = "< name {tagattrs} />"

# Subgrammar rules

SIMPLETYPE_NAME = 'simpletype'
SIMPLETYPE = 'bool|int|float|string|name|tag|event'

ARRAYTYPE_NAME = 'arraytype'
ARRAYTYPE = '{simpletype} []'

MAPTYPE_NAME = 'maptype'
MAPTYPE = '{simpletype} : {simpletype} {}'

TYPE_NAME = "type"
TYPE = "{arraytype}|{maptype}|{simpletype}"

IFELSE_NAME = 'ifelse'
IFELSE = 'if {expression} { {expression} } ({else})?'

ELSE_NAME = 'else'
ELSE = 'else { {expression} }'

VARLOCAL_NAME = 'varlocal'
VARLOCAL = '(var|{type})? (this .)? name (= {expression})? ;'

FUNCCALL_NAME = 'funccall'
FUNCCALL = '(this .)? name ( {callparams} )'

PARAMS_NAME = "params"
PARAMS = "({type} name `,`)*"

ORDERBYPARAMS_NAME = 'orderbyparams'
ORDERBYPARAMS = '(name `,`)+'

CALLPARAMS_NAME = "callparams"
CALLPARAMS = "({expression} `,`)*"

CONSTRUCTORCALL_NAME = 'constructorcall'
CONSTRUCTORCALL = 'name ( ) { (name : {expression} `,`)* } ;'

# TODO(dem) solve more complex parsing operators

FUNCBODY_NAME = 'funcbody'
FUNCBODY = '({expression} `;`)* (return)? ({expression} `;`)*'

# CALLFUNC_NAME = "callfunc"
# CALLFUNC = "name ( {callparams} )"
# 
# CALLOBJFUNC_NAME = "callobjfunc"
# CALLOBJFUNC = "name.name ( {callparams} )"
# 
# MULT_NAME = 'mult'
# MULT = '{expression} * {expression}'
# 
# MULTASSIGN_NAME = 'multassign'
# MULTASSIGN = 'name *= {expression}'
# 
# DIV_NAME = 'div'
# DIV = '{expression} / {expression}'
# 
# DIVASSIGN_NAME = 'divassign'
# DIVASSIGN = 'name /= {expression}'
# 
# ADD_NAME = 'add'
# ADD = '{expression} + {expression}'
# 
# ADDASSIGN_NAME = 'addassign'
# ADDASSIGN = 'name += {expression}'
# 
# SUB_NAME = 'sub'
# SUB = '{expression} - {expression}'
# 
# SUBASSIGN_NAME = 'subassign'
# SUBASSIGN = 'name -= {expression}'
# 
# GREATER_NAME = 'greater'
# GREATER = '{expression} > {expression}'
# 
# LESS_NAME = 'less'
# LESS = '{expression} < {expression}'
# 
# GREATEREQUAL_NAME = 'greaterequal'
# GREATEREQUAL = '{expression} >= {expression}'
# 
# LESSEQUAL_NAME = 'lessequal'
# LESSEQUAL = '{expression} <= {expression}'
# 
# EXPRESSION_NAME = "expression"
# EXPRESSION = "name|{callfunc}|name.name|{callobjfunc}|{multiply}|{divide}"
# 
# VARASSIGN_NAME = "varassign"
# VARASSIGN = "name = {expression} ;"
# 
# MAPBODY_NAME = 'mapbody'
# MAPBODY = '{ name : {variable}|{strlit} }'
# 
# PARAMS_NAME = "params"
# PARAMS = "({type} name `,`)*"
# 
# CALLPARAMS_NAME = "callparams"
# CALLPARAMS = "({expression} `,`)*"
# 
# CONSTRUCTOR_NAME = "constructor"
# CONSTRUCTOR = "( {params} ) {  }"
# 
# SELECTORDERBY_NAME = 'selectorderby'
# SELECTORDERBY = 'order by (name `,`)*'
# 
# CONCATPARAMS_NAME = "concatparams"
# CONCATPARAMS = "({expression} `,`){2,}"
# 
# TAGATTRS_NAME = "tagattrs"
# TAGATTRS = "name = {mapbody}|{variable}|{strlit}|name"
