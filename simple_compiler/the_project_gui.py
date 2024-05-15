import pandas as pd
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, filedialog
import re

# Define the regular expressions for recognizing MiniScript tokens
KEYWORDS = r'\b(if|while|for|print|return|break|continue|else)\b'
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

def parse(tokens):
    # Dummy parse function
    # You need to implement actual parsing logic here
    
    return tokens



def display_tokens_gui(tokens):
    root = tk.Tk()
    root.title("Tokenization and Parsing Output")

    table_frame = ttk.Frame(root)
    table_frame.pack(padx=10, pady=10)

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

    table_label = ttk.Label(table_frame, text="Tokenized and Parsed Output")
    table_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    token_table = ttk.Treeview(table_frame, columns=headers, show='headings')
    for col in headers:
        token_table.heading(col, text=col)
    for row in table:
        token_table.insert("", "end", values=row)
    token_table.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

    root.mainloop()

def tokenize_and_parse(code):
    tokens = lexer(code)
    parsed_tokens = parse(tokens)
    display_tokens_gui(parsed_tokens)

def choose_file_and_tokenize():
    file_path = filedialog.askopenfilename(title="Choose a file", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            code = file.read()
        tokenize_and_parse(code)

# GUI Setup
root = tk.Tk()
root.title("Tokenization and Parsing GUI")
root.geometry("600x500")  # Set initial window size

style = ttk.Style()
style.configure("TButton", foreground="blue", background="blue", font=("Helvetica", 12, "bold"))
style.configure("TLabel", font=("Helvetica", 14, "bold"))

load_button = ttk.Button(root, text="Choose File", command=choose_file_and_tokenize)
load_button.pack(pady=10)

root.mainloop()






# lis4 =  []
# for o in lis4:
#     for p in o:
#         l = 25 - len(str(p))
#         print(p, " " * l, end="")

#     print()

# print()

# # Creating symbol table as list of dictionaries
# sym_table = []
# for h in lis4:
#     sym_table.append({"Name": h[0], "Address": h[1], "Type": h[2], "Dimensions": h[3], "Line Declared": h[4],
#                         "Reference Line": h[5]})

# for h in sym_table:
#     print(h)



# Parse Table
parse_table = {
    'statement_list': {
        'identifier': 'statement ; statement_list',
        'print': 'statement ; statement_list',
        'if': 'statement ; statement_list',
        'while': 'statement ; statement_list',
        ';': 'statement_list',
        '{': 'statement_list { statement_list } statement_list'
    },
    'statement': {
        'identifier': 'assignment',
        'print': 'print expression ;',
        'if': 'if expression { statement_list }',
        'while': 'while expression { statement_list }'
    },
    'assignment': {
        'identifier': 'identifier = expression ;'
    },
    'print': {
        'print': 'print expression ;'
    },
    'if_statement': {
        'if': 'if expression { statement_list }'
    },
    'while_loop': {
        'while': 'while expression { statement_list }'
    },
    'expression': {
        'identifier': 'term',
        '(': 'term',
        'number': 'term',
    },
    'term': {
        'identifier': 'identifier',
        'string': 'string',
        '(': '( expression )',
        'number': 'number'
    },
    'number': {
        'digit': 'digit'
    },
    'identifier': {
        'identifier': 'identifier ( expression ) op term',
        '(': '( expression ) op term'
    },
    'op': {
        '+': '+ term',
        '-': '- term',
        '*': '* term',
        '/': '/ term'
    },
    'string': {
        'identifier': 'identifier',
        'string': 'string'
    },
    'digit': {'digit': 'digit'}
}

# Creating DataFrame from Parse Table
df = pd.DataFrame.from_dict(parse_table, orient='index')
df.index.name = 'Non-terminal'
df.columns.name = 'Terminal'
df.fillna('', inplace=True)
df = df.rename(columns=lambda x: 'digit' if x.isdigit() else x)

# Displaying Parse Table
print()
print("PARSE TABLE:")
print()
print(df)

# Parse Tree created using rules.
# Sample input sequences for different statements
assign_st = ["IDENTIFIER", "IDENTIFIER", "EQUALS", ["NUMBER", "STRING", ["NUMBER", ["PLUS", "MINUS", "TIMES", "DIVIDE"], "NUMBER"]], "SEMI_COLON"]
print_st = ["IDENTIFIER", "LPAREN", ["IDENTIFIER", "NUMBER", "STRING"], "RPAREN", "SEMI_COLON"]
if_st = ["IDENTIFIER", "LPAREN", "IDENTIFIER", ["GREATER_THAN", "LESS_THAN", "EQUALS", ">=", "<="], "NUMBER", " RPAREN", "{", "IDENTIFIER", "LPAREN", "IDENTIFIER", "RPAREN", "SEMI_COLON", "}"]
else_st = ["IDENTIFIER", "{", "IDENTIFIER", "LPAREN", "IDENTIFIER", "RPAREN", "SEMI_COLON", "}"]
while_st = ["IDENTIFIER", "LPAREN", "IDENTIFIER", ["GREATER_THAN", "LESS_THAN", "EQUALS", ">=", "<="], "NUMBER", " RPAREN", "{", "IDENTIFIER", "LPAREN", "IDENTIFIER", "RPAREN", "SEMI_COLON", "}"]





# Define the Compiler class and SymbolTable class
class SymbolTable:
    def __init__(self):
        self.table = {}

    def insert(self, symbol, value):
        self.table[symbol] = value

    def lookup(self, symbol):
        return self.table.get(symbol)

    def print_table(self):
        for symbol, value in self.table.items():
            print(f"{symbol}: {value}")

class Compiler:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.output_text = ""

    def compile(self, source_code):
        # Tokenize the source code
        tokens = self.tokenize(source_code)

        # Parse the tokens
        self.parse(tokens)

    def tokenize(self, source_code):
        # This is a very simple tokenizer and does not handle all possible cases
        tokens = source_code.split()
        return tokens

    def parse(self, tokens):
        for i in range(0, len(tokens), 2):
            symbol = tokens[i]
            value = tokens[i+1]
            self.symbol_table.insert(symbol, value)

    def semantic_analysis(self):
        # Perform semantic analysis on the AST
        # This is a very basic example and does not handle all possible cases
        for symbol, value in self.symbol_table.table.items():
            if value == 'int':
                self.output_text += f"Variable {symbol} is an integer\n"
            elif value == 'float':
                self.output_text += f"Variable {symbol} is a float\n"
            else:
                self.output_text += f"Unknown type for variable {symbol}\n"

    def generate_code(self):
        # Generate machine code or bytecode
        # This is a very basic example and does not handle all possible cases
        self.output_text += "Generated code:\n"
        for symbol, value in self.symbol_table.table.items():
            self.output_text += f"{symbol}: {value}\n"

# GUI Setup
root = tk.Tk()
root.title("Compiler Output GUI")
root.geometry("600x500")

style = ttk.Style()
style.configure("TButton", foreground="blue", background="blue", font=("Helvetica", 12, "bold"))
style.configure("TLabel", font=("Helvetica", 14, "bold"))

# Define the Compiler instance
compiler = Compiler()

# Function to compile the source code
def compile_source_code():
    source_code = source_code_text.get("1.0", tk.END)
    compiler.compile(source_code)
    compiler.semantic_analysis()
    compiler.generate_code()
    update_output_text()

# Function to update the output text in the GUI
def update_output_text():
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, compiler.output_text)

# Text widget for entering source code
source_code_label = ttk.Label(root, text="Enter Source Code:")
source_code_label.pack(pady=5)
source_code_text = ScrolledText(root, height=10, width=60)
source_code_text.pack(pady=5)

# Button to compile source code
compile_button = ttk.Button(root, text="Compile", command=compile_source_code)
compile_button.pack(pady=5)

# Text widget to display compiler output
output_text_label = ttk.Label(root, text="Compiler Output:")
output_text_label.pack(pady=5)
output_text = ScrolledText(root, height=10, width=60)
output_text.pack(pady=5)

root.mainloop()
