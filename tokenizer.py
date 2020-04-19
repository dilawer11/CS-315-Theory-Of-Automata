import ply.lex as lex

tokens = (
    'INT', #int
    'DOUBLE', #double
    'CHAR', # char
    'STRING', # string
    'BOOL', # bool
    'CONSOLE', # console
    'COMMA', # ,
    'ASSIGN', # =
    'LSQBRACE', #[
    'RSQBRACE', #]
    'LPARENT', # (
    'RPARENT', # )
    'LCURLY', # {
    'RCURLY', # }
    'IF', # if
    'EF', # ef
    'EL', # el
    'PLUS', # +
    'MINUS', # -
    'DIVIDE', # /
    'MULTIPLY', # *
    'MOD', # %
    'POWER', # ^
    'PLUSPLUS', # ++
    'MINUSMINUS', # --
    'LT', # <
    'GT', # >
    'LE', # <=
    'GE', # >=
    'NE', # !=
    'EQ', # ==
    'NOT', # not
    'AND', # and
    'OR', # or
    'DOT', # .
    'TYPE', # int, string, double, char, bool
    'IDENTIFIER', # variable name
    'SEMICOLON', # end of a line
)

t_COMMA = r','
t_LSQBRACE = r'\['
t_RSQBRACE = r'\]'
t_LPARENT = r'\('
t_RPARENT = r'\)'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_DIVIDE = r'/'
t_MULTIPLY = r'\*'
t_POWER = r'\^'
t_MOD = r'%'
t_LE = r'<='
t_LT = r'<'
t_GE = r'>='
t_GT = r'>'
t_EQ = r'=='
t_NE = r'!='
t_ASSIGN = r'='
t_SEMICOLON = r';'

t_ignore = ' \t\v\r' # whitespace

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
def t_TYPE(t):
    r'int|string|bool|char|double'
    return t
def t_BOOL(t):
    r'true|false'
    return t
def t_OR(t):
    r'or'
    return t
def t_AND(t):
    r'and'
    return t
def t_NOT(t):
    r'not'
    return t
def t_IF(t):
    r'if'
    return t
def t_EF(t):
    r'ef'
    return t
def t_EL(t):
    r'el'
    return t
def t_CONSOLE(t):
    r'console'
    return t
def t_IDENTIFIER(t):
    r'[a-zA-Z][a-zA-Z0-9|_]*'
    return t
def t_STRING(t):
    r'"[^"\n]*"'
    t.value = t.value[1:-1]
    return t
def t_CHAR(t):
    r"'\\?[^']'"
    t.value = t.value[1:-1]
    return t
def t_PLUSPLUS(t):
    r'\+\+'
    return t
def t_MINUSMINUS(t):
    r'--'
    return t
def t_MINUS(token):
    r'-'
    return token
def t_PLUS(token):
    r'\+'
    return token
def t_DOUBLE(token):
    r'\d+\.\d+'
    token.value = float(token.value)
    return token
def t_INT(token):
    r'\d+'
    token.value = int(token.value)
    return token
def t_DOT(t):
    r'\.'
    return t
def t_error(t):
    print ("DA Language Illegal Lexer: " + t.value[0])
    t.lexer.skip(1)

