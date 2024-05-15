import re
from tabulate import tabulate

# Define the regular expressions for recognizing MiniScript tokens
KEYWORDS = r'\b(if|while|for|print|return|break|continue|else|in|range|and|or|not)\b'
IDENTIFIERS = r'[a-zA-Z_][a-zA-Z_0-9]*'
LITERALS = r'(\d+)|(["\']([^"\']|\\.)*["\']|true|false|null)'

SYMBOLS = r'[+\-*/()=<>.,;:]|(\s+)|(\n)|(\r\n)|(\r)'

# Define the token types
TOKEN_TYPES = {
    'KEYWORD': 1,
    'IDENTIFIER': 2,
    'LITERAL': 3,
    'SYMBOL': 4
}

# Define the token values
TOKEN_VALUES = {
    'KEYWORD': {
        'if': TOKEN_TYPES['KEYWORD'],
        'while': TOKEN_TYPES['KEYWORD'],
        'for': TOKEN_TYPES['KEYWORD'],
        'print': TOKEN_TYPES['KEYWORD'],
        'return': TOKEN_TYPES['KEYWORD'],
        'break': TOKEN_TYPES['KEYWORD'],
        'continue': TOKEN_TYPES['KEYWORD'],
        'else': TOKEN_TYPES['KEYWORD'],
        'in': TOKEN_TYPES['KEYWORD'],
        'range': TOKEN_TYPES['KEYWORD'],
        'and': TOKEN_TYPES['KEYWORD'],
        'or': TOKEN_TYPES['KEYWORD'],
        'not': TOKEN_TYPES['KEYWORD']
    },
    'IDENTIFIER': {},
    'LITERAL': {},
    'SYMBOL': {}
}

def lexer(code):
    tokens = []
    for match in re.finditer(r'|'.join([KEYWORDS, IDENTIFIERS, LITERALS, SYMBOLS]), code):
        token = match.group()
        if token in KEYWORDS:
            tokens.append({'type': TOKEN_TYPES['KEYWORD'], 'value': token})
        elif re.match(IDENTIFIERS, token):
            tokens.append({'type': TOKEN_TYPES['IDENTIFIER'], 'value': token})
        elif re.match(LITERALS, token):
            if token.startswith('"') or token.startswith("'"):
                tokens.append({'type': TOKEN_TYPES['LITERAL'], 'value': token})
            else:
                try:
                    value = int(token)
                    tokens.append({'type': TOKEN_TYPES['LITERAL'], 'value': value})
                except ValueError:
                    tokens.append({'type': TOKEN_TYPES['LITERAL'], 'value': token})
        elif re.match(SYMBOLS, token):
            if token.isspace():
                tokens.append({'type': TOKEN_TYPES['SYMBOL'], 'value': token})
            elif token == '\n':
                tokens.append({'type': TOKEN_TYPES['SYMBOL'], 'value': token})
            elif token == '\r\n':
                tokens.append({'type': TOKEN_TYPES['SYMBOL'], 'value': token})
            elif token == '\r':
                tokens.append({'type': TOKEN_TYPES['SYMBOL'], 'value': token})
            else:
                tokens.append({'type': TOKEN_TYPES['SYMBOL'], 'value': token})
    return tokens

# Test the lexer with sample input code
code = """
    if x > 5 {
        print("x is greater than 5")
    } else {
        print("x is less than or equal to 5")
    }
    while x > 0 {
        print(x)
        x -= 1
    }
    for i in range(5) {
        print(i)
    }
"""

tokens = lexer(code)

# Print the tokens in a table format
headers = ['Type', 'Value']
table = []
for token in tokens:
    if token['type'] == TOKEN_TYPES['KEYWORD']:
        token_type = 'KEYWORD'
    elif token['type'] == TOKEN_TYPES['IDENTIFIER']:
        token_type = 'IDENTIFIER'
    elif token['type'] == TOKEN_TYPES['LITERAL']:
        token_type = 'LITERAL'
    else:
        token_type = 'SYMBOL'
    table.append([token_type, token['value']])

print(tabulate(table, headers, tablefmt='grid'))

##################################################################



def parse_Miniscript(tokens):
    statement_list = []
    i = 0
    while i < len(tokens):
        if tokens[i] == 'while':
            statement_list.append(parse_WhileStatement(tokens[i:i+3]))
            i += 3
        elif tokens[i] == 'if':
            statement_list.append(parse_IfStatement(tokens[i:i+3]))
            i += 3
        elif tokens[i] == 'print':
            statement_list.append(parse_PrintStatement(tokens[i:i+2]))
            i += 2
        elif tokens[i] == 'for':
            statement_list.append(parse_ForStatement(tokens[i:i+3]))
            i += 3
        else:
            raise Exception("Invalid statement")
    return statement_list

def parse_IfStatement(tokens):
    if tokens[1] == 'then':
        condition = parse_Expression(tokens[2])
        then_statement = parse_StatementList(tokens[3:])
        else_statement = parse_StatementList(tokens[5:])
        return IfStatement(tokens[0], condition, then_statement, else_statement)
    else:
        raise Exception("Invalid if statement")

def parse_WhileStatement(tokens):
    condition = parse_Expression(tokens[1])
    statement = parse_StatementList(tokens[2:])
    return WhileStatement(tokens[0], condition, statement)

def parse_PrintStatement(tokens):
    return PrintStatement([parse_Factor(tokens[1])])

def parse_ForStatement(tokens):
    loop_variable = parse_Factor(tokens[1])
    range_expression = parse_Expression(tokens[2])
    statement = parse_StatementList(tokens[3:])
    return ForStatement(tokens[0], loop_variable, range_expression, statement)

def parse_StatementList(tokens):
    statement_list = []
    i = 0
    while i < len(tokens):
        statement_list.append(parse_Statement(tokens[i:i+1]))
        i += 1
    return statement_list

def parse_Statement(tokens):
    if tokens[0] == 'print':
        return parse_PrintStatement(tokens)
    elif tokens[0] == 'if':
        return parse_IfStatement(tokens)
    elif tokens[0] == 'while':
        return parse_WhileStatement(tokens)
    elif tokens[0] == 'for':
        return parse_ForStatement(tokens)
    else:
        raise Exception("Invalid statement")

def parse_Expression(tokens):
    if len(tokens) == 1:
        return parse_Factor(tokens[0])
    else:
        return Term(parse_Expression(tokens[:len(tokens)//2]), tokens[len(tokens)//2], parse_Expression(tokens[len(tokens)//2+1:]))

def parse_Factor(tokens):
    if re.match(IDENTIFIERS, tokens[0]):
        return Identifier(tokens[0])
    elif re.match(LITERALS, tokens[0]):
        if tokens[0].startswith('"') or tokens[0].startswith("'"):
            return StringLiteral(tokens[0])
        else:
            return Number(int(tokens[0]))
    else:
        raise Exception("Invalid factor")

def parse_Term(tokens):
    if len(tokens) == 1:
        return parse_Factor(tokens[0])
    else:
        return Term(parse_Term(tokens[:len(tokens)//2]), tokens[len(tokens)//2], parse_Term(tokens[len(tokens)//2+1:]))

class AST:
    def __init__(self, type, children=None):
        self.type = type
        self.children = children if children else []

    def __str__(self):
        return f'{self.type}({", ".join(str(child) for child in self.children)})'

class PrintStatement(AST):
    def __init__(self, expression):
        super().__init__('PrintStatement')
        self.expression = expression

class IfStatement(AST):
    def __init__(self, keyword, condition, then_statement, else_statement):
        super().__init__('IfStatement')
        self.keyword = keyword
        self.condition = condition
        self.then_statement = then_statement
        self.else_statement = else_statement

class WhileStatement(AST):
    def __init__(self, keyword, condition, statement):
        super().__init__('WhileStatement')
        self.keyword = keyword
        self.condition = condition
        self.statement = statement

class ForStatement(AST):
    def __init__(self, keyword, loop_variable, range_expression, statement):
        super().__init__('ForStatement')
        self.keyword = keyword
        self.loop_variable = loop_variable
        self.range_expression = range_expression
        self.statement = statement

class Term(AST):
    def __init__(self, left, operator, right):
        super().__init__('Term')
        self.left = left
        self.operator = operator
        self.right = right

class Factor(AST):
    def __init__(self, value):
        super().__init__('Factor')
        self.value = value

class Number(AST):
    def __init__(self, value):
        super().__init__('Number')
        self.value = value

class Identifier(AST):
    def __init__(self, value):
        super().__init__('Identifier')
        self.value = value

class StringLiteral(AST):
    def __init__(self, value):
        super().__init__('StringLiteral')
        self.value = value

class BooleanLiteral(AST):
    def __init__(self, value):
        super().__init__('BooleanLiteral')
        self.value = value

class NullLiteral(AST):
    def __init__(self, value):
        super().__init__('NullLiteral')
        self.value = value




class Statement:
    def __init__(self, indent):
        self.indent = indent
        self.children = []

class Expression:
    def __init__(self, depth):
        self.depth = depth
        self.children = []

class Variable:
    def __init__(self, declared):
        self.declared = declared







######################################################################################



import sys

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add_variable(self, name, var_type):
        self.symbols[name] = {'type': 'variable', 'var_type': var_type}

    def add_function(self, name, return_type, parameters):
        self.symbols[name] = {'type': 'function', 'return_type': return_type, 'parameters': parameters}

    def get_symbol(self, name):
        return self.symbols.get(name, None)

    def print_table(self):
        print("Symbol Table:")
        for name, symbol_info in self.symbols.items():
            if symbol_info['type'] == 'variable':
                print(f"Variable: {name}, Type: {symbol_info['var_type']}")
            elif symbol_info['type'] == 'function':
                print(f"Function: {name}, Return Type: {symbol_info['return_type']}, Parameters: {symbol_info['parameters']}")

# Example usage:
symbol_table = SymbolTable()

# Add variables
symbol_table.add_variable('x', 'int')
symbol_table.add_variable('y', 'float')

# Add functions
symbol_table.add_function('add', 'int', ['int', 'int'])
symbol_table.add_function('multiply', 'float', ['float', 'float'])

# Print symbol table
symbol_table.print_table()



class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def analyze(self, ast):
        try:
            for node in ast:
                if node['type'] == 'function_declaration':
                    self.analyze_function_declaration(node)
                elif node['type'] == 'assignment':
                    self.analyze_assignment(node)
                elif node['type'] == 'variable':
                    self.analyze_variable(node)
        except MiniScriptError as e:
            print(f"Error: {e}")
            response = input("Do you want to continue executing the program? (y/n): ")
            if response.lower() == 'y':
                # Continue executing the program
                pass
            else:
                # Exit the program
                sys.exit(1)

    def analyze_function_declaration(self, node):
        function_name = node['children'][0]
        self.symbol_table.add_symbol(function_name, None)
        print(f"Function '{function_name}' declared.")

    def analyze_assignment(self, node):
        variable_name = node['children'][0]
        value = node['children'][1]

        if not isinstance(variable_name, str):
            raise MiniScriptError("Invalid variable name in assignment.")

        if not self.symbol_table.get_symbol(variable_name):
            raise MiniScriptError(f"Undefined variable: '{variable_name}'.")
        else:
            print(f"Variable '{variable_name}' assigned.")

    def analyze_variable(self, node):
        variable_name = node['children'][0]

        if not isinstance(variable_name, str):
            raise MiniScriptError("Invalid variable name.")

        if not self.symbol_table.get_symbol(variable_name):
            raise MiniScriptError(f"Undefined variable: '{variable_name}'.")
        else:
            print(f"Variable '{variable_name}' used.")

class MiniScriptError(Exception):
    def __init__(self, message):
        super().__init__(message)

# Example AST nodes
ast = [
    {'type': 'function_declaration', 'children': ['add']},
    {'type': 'assignment', 'children': ['x', 10]},
    {'type': 'variable', 'children': ['x']},
    {'type': 'assignment', 'children': ['y', 20]},
    {'type': 'variable', 'children': ['y']},
    {'type': 'variable', 'children': ['z']}  # This will raise an error as 'z' is not assigned in any function
]

# Perform semantic analysis
analyzer = SemanticAnalyzer()
try:
    analyzer.analyze(ast)
    print("Semantic analysis passed successfully.")
    analyzer.symbol_table.print_table()  
except Exception as e:
    print("Semantic analysis failed:", e)









##########################





class CodeOptimization:
    # ...

    def optimize_expression(self, expression):
        # Implement expression simplification logic here
        pass

    def constant_folding(self, expression):
        # Implement constant folding logic here
        pass

    def dead_code_elimination(self, node):
        # Implement dead code elimination logic here
        pass

    def loop_optimization(self, node):
        # Implement loop optimization logic here
        pass


