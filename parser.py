import ply.yacc as yacc
import sys
from lexer import tokens

start = 'namespace'

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('left', 'MOD', 'POWER'),
    ('right', 'NOT'),
)

def p_namespace(p):
    'namespace : element namespace'
    p[0] = [p[1]] + p[2]
def p_namespace_empty(p):
    'namespace : '
    p[0] = []
def p_element_statement(p):
    'element : stmt SEMICOLON'
    p[0] = ('stmt', p[1])
def p_element_if_ef_el(p):
    'element : if ef el'
    p[0] = ('if', [p[1]] + p[2], p[3])
def p_if(p):
    'if : IF exp compoundstmt'
    p[0] = (p[2], p[3])
def p_ef(p):
    'ef : EF exp compoundstmt ef'
    p[0] = [(p[2], p[3])] + p[4]
def p_ef_empty(p):
    'ef : '
    p[0] = []
def p_el(p):
    'el : EL compoundstmt'
    p[0] = p[2]
def p_el_empty(p):
    'el : '
    p[0] = []
def p_optparams(p):
    'optparams : params'
    p[0] = p[1]
def p_optparams_empty(p):
    'optparams : '
    p[0] = []
def p_params(p):
    'params : exp COMMA params'
    p[0] = [ p[1] ] + p[3]
def p_params_exp(p):
    'params : exp'
    p[0] = [ p[1] ]
def p_compoundstmt(p):
    'compoundstmt : LCURLY namespace RCURLY'
    p[0] = p[2]
def p_statements(p):
    'statements : stmt SEMICOLON statements'
    p[0] = [ ("stmt",p[1]) ]  + p[3]
def p_statements_empty(p):
    'statements : '
    p[0] = []
def p_stmt_console(p):
    'stmt : CONSOLE LPARENT optparams RPARENT'
    p[0] = ("console", p[3])
def p_stmt_assignment(p):
    'stmt : IDENTIFIER ASSIGN exp'
    p[0] = ('assign', p[1], p[3])
def p_stmt_init_empty(p):
    'stmt : TYPE IDENTIFIER'
    p[0] = ('init', p[2], p[1], None)
def p_stmt_init_assign(p):
    'stmt : TYPE IDENTIFIER ASSIGN exp'
    p[0] = ('init', p[2], p[1], p[4])
def p_stmt_init_list(p):
    'stmt : TYPE IDENTIFIER ASSIGN LSQBRACE optparams RSQBRACE'
    p[0] = ('init-list', p[2], p[1], p[5])
def p_exp_list_direct(p):
    'exp : IDENTIFIER LSQBRACE optparams RSQBRACE'
    p[0] = ('func', 'index', p[1], p[3])
def p_exp_list_func(p):
    'exp : IDENTIFIER DOT LISTFUNC LPARENT optparams RPARENT'
    p[0] = ('func', p[3], p[1], p[5])

# Expressions
def p_stmt_exp(p):
    'stmt : exp'
    p[0] = ('exp', p[1])
def p_exp_parent(p):
    'exp : LPARENT exp RPARENT'
    p[0] = ('exp', p[2])
def p_exp_identifier(p):
    'exp : IDENTIFIER'
    p[0] = ("identifier",p[1])

# Types
def p_exp_string(p):
    'exp : STRING'
    p[0] = ("string", p[1])
def p_exp_bool(p):
    'exp : BOOL'
    p[0] = ("bool", p[1])
def p_exp_int(p):
    'exp : INT'
    p[0] = ("int", p[1])
def p_exp_double(p):
    'exp : DOUBLE'
    p[0] = ("double", p[1])
def p_exp_char(p):
    'exp : CHAR'
    p[0] = ("char", p[1])

# Arithimetic Ops
def p_exp_postfix_plusplus(p):
    'exp : IDENTIFIER PLUSPLUS'
    p[0] = ("post-plusplus", p[1])
def p_exp_prefix_plusplus(p):
    'exp : PLUSPLUS IDENTIFIER'
    p[0] = ("pre-plusplus", p[1])
def p_exp_postfix_minusminus(p):
    'exp : IDENTIFIER MINUSMINUS'
    p[0] = ("post-plusplus", p[1])
def p_exp_prefix_minusminus(p):
    'exp : MINUSMINUS IDENTIFIER'
    p[0] = ("pre-minusminus", p[1])
def p_exp_plus(p):
    'exp : exp PLUS exp'
    p[0] = ("plus", p[1], p[3])
def p_exp_minus(p):
    'exp : exp MINUS exp'
    p[0] = ("minus", p[1], p[3])
def p_exp_multiply(p):
    'exp : exp MULTIPLY exp'
    p[0] = ("multiply", p[1], p[3])
def p_exp_divide(p):
    'exp : exp DIVIDE exp'
    p[0] = ("divide", p[1], p[3])
def p_exp_not(p):
    'exp : NOT exp'
    p[0] = ("not", p[2])
def p_exp_and(p):
    'exp : exp AND exp'
    p[0] = ("and", p[1], p[3])
def p_exp_or(p):
    'exp : exp OR exp'
    p[0] = ("or", p[1], p[3])
def p_exp_lt(p):
    'exp : exp LT exp'
    p[0] = ('LT', p[1], p[3])
def p_exp_gt(p):
    'exp : exp GT exp'
    p[0] = ('GT', p[1], p[3])
def p_exp_le(p):
    'exp : exp LE exp'
    p[0] = ('LE', p[1], p[3])
def p_exp_ge(p):
    'exp : exp GE exp'
    p[0] = ('GE', p[1], p[3])
def p_exp_ne(p):
    'exp : exp NE exp'
    p[0] = ('NE', p[1], p[3])
def p_exp_eq(p):
    'exp : exp EQ exp'
    p[0] = ('EQ', p[1], p[3])
def p_exp_mod(p):
    'exp : exp MOD exp'
    p[0] = ('MOD', p[1], p[3])
def p_exp_power(p):
    'exp : exp POWER exp'
    p[0] = ('POWER', p[1], p[3])
# Special Cases
def p_exp_neg(p):
    'exp : MINUS exp'
    p[0] = ('NEG', p[2])
def p_error(p):
    print(f'ERROR -> {p}')