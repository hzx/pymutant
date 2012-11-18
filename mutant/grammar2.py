

rules = {
    'import': 'import {namespace_name}<module> as name<alias> ;',
    'define': 'define name<alias> {type}<type> ;',
    'variable': 'var|{type}<type> name<name> ;',
    'function': '{type}<type> (name<name>)? ( {function_params}! ) { {function_body}! }',
    'enum': 'enum name<name> { {enum_body}! }',
    'struct': 'struct name<name> { {struct_body}! }',
    'class': 'class name<name> (extends {namespace_name}<base_name>)? { {class_body}! }',

    'namespace_name': '(name `.`)+',
    'type': '',
    'function_params': '',
    'function_body': '',
    'enum_body': '',
    'struct_body': '',
    'class_body': '',
    }
