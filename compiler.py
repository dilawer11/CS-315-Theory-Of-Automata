import tokenizer
import parser
from interpreter import Interpreter
import ply.lex as lex
import ply.yacc as yacc
import sys

def run(code="x+y\n1-2"):
    dalexer = lex.lex(module=tokenizer)
    daparser = yacc.yacc(module=parser)
    dainterpreter = Interpreter()
    # code = "console(not true == (not (not d)) and (true != 0))"
    if code[-1]!='\n':
        code += '\n'
    dalexer.input(code)
     # Tokenize
    while True:
        tok = dalexer.token()
        if not tok: 
            break      # No more input
        print(tok)
    parse_tree = daparser.parse(code, lexer=dalexer)
    for t in parse_tree:
        print(t)
    dainterpreter.interpret(trees=parse_tree)

def main(filename, mode):
    with open(filename, 'r') as f:
        data = f.read()
    run(data)
if __name__ == "__main__":
    # You can compile the program using python3 compiler.py [FILENAME] [OPTIONS]
    # FILENAME is the Code file for the language
    # OPTIONS can be one of [t, p, c] where 't' is for tokens, 'p' is for parse tree, 'c' is for compile [Default: c]
    if len(sys.argv) == 2:
        mode = 'c'
        filename = sys.argv[1]
        main(filename, mode)
    elif len(sys.argv) == 3:
        mode = sys.argv[2]
        filename = sys.argv[1]
        main(filename, mode)
    else:
        print('No Code File Specified. Exiting...')