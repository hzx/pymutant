

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

# Main grammar rules

DEFINE_NAME = "define"
DEFINE = "define name {expression}! ;"

VARIABLE_NAME = "variable"
VARIABLE = "var|{type} name (= {varbody}!)? ;"

FUNCTION_NAME = "function"
FUNCTION = "({type})? (name)? ( {params} ) { {funcbody}! }"

ENUM_NAME = "enum"
ENUM = "enum name { {enumbody} }"

STRUCT_NAME = "struct"
STRUCT = "struct name { {structbody} }"

CLASS_NAME = "class"
CLASS = "class name (extends name)? { {classbody} }"

# Subgrammar rules

VARBODY_NAME = 'varbody'
VARBODY = '{selectfrom}|{selectconcat}|{expression}!'

ENUMBODY_NAME = 'enumbody'
ENUMBODY = '(name = {litint} ;)*'

STRUCTBODY_NAME = 'structbody'
STRUCTBODY = '({type} name ;)*'

CLASSBODY_NAME = 'classbody'
CLASSBODY = '{constructor}|{variable}|{function}'

# Query

SELECTFROM_NAME = "selectfrom"
SELECTFROM = "select from name where {expression}! (order by {orderbyparams})?"

SELECTCONCAT_NAME = "selectconcat"
SELECTCONCAT = "select concat {concatparams}"

ORDERBYPARAMS_NAME = 'orderbyparams'
ORDERBYPARAMS = '(name `,`)+'

# HTML

TAG_NAME = "tag"
TAG = "< name {tagattrs} > ({tag}|{singletag})* </ name >"

SINGLETAG_NAME = "singletag"
SINGLETAG = "< name {tagattrs} />"

TAGATTRS_NAME = 'tagattrs'
TAGATTRS = ''

# Type

NAMETYPE_NAME = 'nametype'
NAMETYPE = '(name `.`)+'

SIMPLETYPE_NAME = 'simpletype'
SIMPLETYPE = 'bool|int|float|string|{nametype}|tag|event'

ARRAYTYPE_NAME = 'arraytype'
ARRAYTYPE = '{simpletype} [ ]'

MAPTYPE_NAME = 'maptype'
MAPTYPE = '{simpletype} : {simpletype} { }'

SETTYPE_NAME = 'settype'
SETTYPE = '{simpletype} { }'

TYPE_NAME = "type"
TYPE = "{arraytype}|{maptype}|{settype}|{simpletype}"

# funcbody

IF_NAME = 'if'
IF = 'if {expression}! { {funcbody}! } ({else})?'

ELSE_NAME = 'else'
ELSE = 'else { {funcbody}! }'

FUNCCALL_NAME = 'funccall'
FUNCCALL = '{nametype} ( {callparams} )'

PARAMS_NAME = "params"
PARAMS = "({type} name `,`)*"

CALLPARAMS_NAME = "callparams"
CALLPARAMS = "({expression}! `,`)*"

CONSTRUCTORCALL_NAME = 'constructorcall'
CONSTRUCTORCALL = 'name ( ) { (name : {varbody} `,`)* } ;'

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

RULES = {
    # main grammar rules
    DEFINE_NAME: DEFINE,
    VARIABLE_NAME: VARIABLE,
    FUNCTION_NAME: FUNCTION,
    ENUM_NAME: ENUM,
    STRUCT_NAME: STRUCT,
    CLASS_NAME: CLASS,
    # subrules
    ENUMBODY_NAME: ENUMBODY,
    STRUCTBODY_NAME: STRUCTBODY,
    CLASSBODY_NAME: CLASSBODY,
    # query
    SELECTFROM_NAME: SELECTFROM,
    SELECTCONCAT_NAME: SELECTCONCAT,
    ORDERBYPARAMS_NAME: ORDERBYPARAMS,
    # HTML
    TAG_NAME: TAG,
    SINGLETAG_NAME: SINGLETAG,
    # type
    NAMETYPE_NAME: NAMETYPE,
    SIMPLETYPE_NAME: SIMPLETYPE,
    ARRAYTYPE_NAME: ARRAYTYPE,
    MAPTYPE_NAME: MAPTYPE,
    SETTYPE_NAME: SETTYPE,
    TYPE_NAME: TYPE,
    # funcbody
    IF_NAME: IF,
    ELSE_NAME: ELSE,
    FUNCCALL_NAME: FUNCCALL,
    PARAMS_NAME: PARAMS,
    CALLPARAMS_NAME: CALLPARAMS,
    CONSTRUCTORCALL_NAME: CONSTRUCTORCALL,
    }

GLOBAL_RULES = [
    DEFINE_NAME,
    VARIABLE_NAME,
    FUNCTION_NAME,
    ENUM_NAME,
    STRUCT_NAME,
    CLASS_NAME,
    ]

EXPRESSION_RULES = [
    SELECTFROM_NAME,
    SELECTCONCAT_NAME,
    SINGLETAG_NAME,
    TAG_NAME,
    ]

FUNCBODY_RULES = [
    VARIABLE_NAME,
    IF_NAME,
    ]

ENUMBODY_RULES = [
    ]

STRUCTBODY_RULES = [
    ]

CLASSBODY_RULES = [
    ]
