
INT_LITERAL_CODE = """
var NUM = 10;
"""
INT_LITERAL_TOKENS = [
    'var', 'NUM', '=', '10', ';'
    ]

FLOAT_LITERAL_CODE = """
var NUM = 12.64;
"""
FLOAT_LITERAL_TOKENS = [
    'var', 'NUM', '=', '12.64', ';'
    ]

STRING_LITERAL_CODE = """
var MSG = "hello world";
"""
STRING_LITERAL_TOKENS = [
    'var', 'MSG', '=', '"hello world"', ';'
    ]

BOOL_VAR_CODE = """
bool isPrint = false;
"""
BOOL_VAR_TOKENS = [
    'bool', 'isPrint', '=', 'false', ';'
    ]

INT_VAR_CODE = """
int instanceCount = 0;
"""
INT_VAR_TOKENS = [
    'int', 'instanceCount', '=', '0', ';'
    ]

FLOAT_VAR_CODE = """
float sum = 20.00;
"""
FLOAT_VAR_TOKENS = [
    'float', 'sum', '=', '20.00', ';'
    ]

STRING_VAR_CODE = """
string message = "Hello, world!";
"""
STRING_VAR_TOKENS = [
    'string', 'message', '=', '"Hello, world!"', ';'
    ]

BOOL_ARRAY_VAR_CODE = """
bool[] flags = [true, false, true, false];
"""
BOOL_ARRAY_VAR_TOKENS = [
    'bool', '[', ']', 'flags', '=', '[', 'true', ',', 'false', ',', 'true', ',', 'false', ']', ';'
    ]

INT_ARRAY_VAR_CODE = """
int[] nums = [12, 13, 14, 15];
"""
INT_ARRAY_VAR_TOKENS = [
    'int', '[', ']', 'nums', '=', '[', '12', ',', '13', ',', '14', ',', '15', ']', ';'
    ]

FLOAT_ARRAY_VAR_CODE = """
float[] nums = [13.23, 27.3, 78.15];
"""
FLOAT_ARRAY_VAR_TOKENS = [
    'float', '[', ']', 'nums', '=', '[', '13.23', ',', '27.3', ',', '78.15', ']', ';'
    ]

STRING_ARRAY_VAR_CODE = """
string[] colors = ["red", "green", "blue"];
"""
STRING_ARRAY_VAR_TOKENS = [
    'string', '[', ']', 'colors', '=', '[', '"red"', ',', '"green"', ',', '"blue"', ']', ';'
    ]

IDENTIFIER_ARRAY_VAR_CODE = """
Value[] values = [Value(1), Value(2), Value(3)];
"""
IDENTIFIER_ARRAY_VAR_TOKENS = [
    'Value', '[', ']', 'values', '=', '[', 'Value', '(', '1', ')', ',', 'Value', '(', '2', ')', ',', 'Value', '(', '3', ')', ']', ';'
    ]

ANON_FUNCTION_CODE = """
() {
}
"""
ANON_FUNCITON_TOKENS = [
    '(', ')', '{', '}'
    ]

ANON_FUNCTION_PARAMS_CODE = """
(int param1, string param2) {
  param1 += 1;
  return param1 * param2;
}
"""
ANON_FUNCTION_PARAMS_TOKENS = [
    '(', 'int', 'param1', ',', 'string', 'param2', ')', '{',
    'param1', '+=', '1', ';',
    'return', 'param1', '*', 'param2', ';', '}'
    ]

FUNCTION_CODE = """
parse() {
}
"""
FUNCTION_TOKENS = [
    'parse', '(', ')', '{', '}'
    ]

FUNCTION_PARAMS_CODE = """
parse(int param1, float param2) {
  param2 += 2.0;
  return param1 * param2;
}
"""
FUNCTION_PARAMS_TOKENS = [
    'parse', '(', 'int', 'param1', ',', 'float', 'param2', ')', '{',
    'param2', '+=', '2.0', ';',
    'return', 'param1', '*', 'param2', ';', '}'
    ]

ENUM_CODE = """
enum identifier {
  MODE_A = 1;
  MODE_B = 2;
  MODE_C = 3;
}
"""
ENUM_TOKENS = [
    'enum', 'identifier', '{',
    'MODE_A', '=', '1', ';',
    'MODE_B', '=', '2', ';',
    'MODE_C', '=', '3', ';',
    '}'
    ]

STRUCT_CODE = """
struct identifier {
  int item1;
}
"""
STRUCT_TOKENS = [
    'struct', 'identifier', '{',
    'int', 'item1', ';',
    '}'
    ]

CLASS_CODE = """
class identifier {
  int item1 = 2;

  float parse(string param1) {
    return 2.80;
  }
}
"""
CLASS_TOKENS = [
    'class', 'identifier', '{',
    'int', 'item1', '=', '2', ';',
    'float', 'parse', '(', 'string', 'param1', ')', '{',
    'return', '2.80', ';',
    '}', 
    '}'
    ]

XML_TAG_SINGLE_CODE = """
<identifier style={fontSize: "12px", color: "#d6d6d6"}></identifier>
"""
XML_TAG_SINGLE_TOKENS = [
    '<', 'identifier', 'style', '=', '{', 'fontSize', ':', '"12px"', ',', 'color', ':', '"#d6d6d6"', '}', '>', '</', 'identifier', '>'
    ]

XML_TAG_CODE = """
<identifier style={fontSize: "12px", color: "#d6d6d6"}/>
"""
XML_TAG_TOKENS = [
    '<', 'identifier', 'style', '=', '{', 'fontSize', ':', '"12px"', ',', 'color', ':', '"#d6d6d6"', '}', '/>'
    ]

SELECT_FROM_CODE = """
select from coll1
where true and false or item1 is 1
order by name, type;
"""
SELECT_FROM_TOKENS = [
    'select', 'from', 'coll1',
    'where', 'true', 'and', 'false', 'or', 'item1', 'is', '1',
    'order', 'by', 'name', ',', 'type', ';'
    ]

SELECT_CONCAT_CODE = """
select concat(collection coll1, collection coll2);
"""
SELECT_CONCAT_TOKENS = [
    'select', 'concat', '(', 'collection', 'coll1', ',', 'collection', 'coll2', ')', ';'
    ]
