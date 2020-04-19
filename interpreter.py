import tokenizer
import parser
import ply.lex as lex
import ply.yacc as yacc
import sys

class Interpreter:
    DEFAULT = {
        'int': 0,
        'string': "",
        'char': '\0',
        'double': 0.0,
        'bool': False,
    }
    def __init__(self):
        print("Welcome to my DA Lang Interpreter")
    def find_env(self, env, identifier):
        if identifier in env:
            return env
        elif 'parent' in env:
            return self.find_env(env['parent'], identifier)
        else:
            return None
    # Lookup A Value of a Variable
    def env_lookup(self, env, identifier):
        var_env = self.find_env(env, identifier)
        if var_env is None:
            raise Exception(f"Variable '{identifier}' not declared")
        else:
            return var_env[identifier]      
    
    # Used to declare variable
    def env_declare(self, env, identifier, value):
        var_env = self.find_env(env, identifier)
        if var_env is None:
            if value['type'] == 'char':
                value['value'] = ord(value['value'])
            env[identifier] = value
        else:
            raise Exception('RedeclarationError')
    # Env Update
    def env_update(self, env, identifier, value):
        var_env = self.find_env(env, identifier)
        if var_env is None:
            raise Exception(f"Variable '{identifier}' not declared")
        else:
            if value['type'] == 'char':
                value['value'] = ord(value['value'])
            if var_env[identifier]['type'] == value['type']:
                var_env[identifier]['value'] = value['value']
            elif var_env[identifier]['type'] == 'bool' and value['type'] in ['char', 'int']:
                if value['value'] == 0 or value['value'] == 1:
                    var_env[identifier]['value'] = bool(value['value'])
                else:
                    raise Exception(f"TypeError: Can only set bool with 1,0, true, false")
            elif var_env[identifier]['type'] == 'double' and value['type'] in ['char', 'int']:
                var_env[identifier]['value'] = float(value['value'])
            elif var_env[identifier]['type'] == 'int' and value['type'] in ['char']:
                var_env[identifier]['value'] = int(value['value'])
            else:
                raise Exception(f"TypeError: Cannot set type '{var_env[identifier]['type']}' with type '{value['type']}'")
    def eval_stmt(self, tree, env):
        stmttype = tree[0]
        if stmttype == "console":
            exps = tree[1]
            for exp in exps:
                result = self.eval_exp(exp, env)
                representation = None
                if result['type'] == 'char':
                    representation = chr(result['value'])
                else:
                    representation = result['value']
                print(representation, end=' ')
            print()
        elif stmttype == "init":
            identifier = tree[1]
            dtype = tree[2]
            self.env_declare(env, identifier, {'value': self.DEFAULT[dtype], 'type': dtype})
            if tree[3] is not None:
                result = self.eval_exp(tree[3], env)
                self.env_update(env, identifier, result)

        elif stmttype == "exp":
            result = self.eval_exp(tree[1], env)
        elif stmttype == "assign":
            identifier = tree[1]
            result = self.eval_exp(tree[2], env)
            self.env_update(env, identifier, result)
        else:
            raise Exception(f"Unknown Statement Type in eval_stmt: {stmttype}")
        
    def plus(self, x, y):
        op = '+'
        ls_type = x['type']
        rs_type = y['type']
        ls_val = x['value']
        rs_val = y['value']
        if ls_type == 'bool' or rs_type == 'bool':
            raise Exception(f"Variables of type 'bool' cannot use operator '{op}'")
        elif ls_type == rs_type:
            return {'value': ls_val + rs_val, 'type': ls_type}
        elif ls_type in ['int', 'double'] and rs_type in ['int', 'double']:
            return {'value': ls_val + rs_val, 'type': 'double'}
        else:
            raise Exception(f"Variables of type '{ls_type}' and '{rs_type}' cannot use operator '{op}'")
    def minus(self, x, y):
        op = '-'
        ls_type = x['type']
        rs_type = y['type']
        ls_val = x['value']
        rs_val = y['value']
        if ls_type in ['bool', 'string'] or rs_type in ['bool', 'string']:
            raise Exception(f"Variables of type 'bool' or 'string' cannot use operator '{op}'")
        elif ls_type == rs_type:
            return {'value': ls_val - rs_val, 'type': ls_type}
        elif ls_type in ['int', 'double'] and rs_type in ['int', 'double']:
            return {'value': ls_val - rs_val, 'type': 'double'}
        else:
            raise Exception(f"Variables of type '{ls_type}' and '{rs_type}' cannot use operator '{op}'")
    def multiply(self, x, y):
        op = '*'
        ls_type = x['type']
        rs_type = y['type']
        ls_val = x['value']
        rs_val = y['value']
        if ls_type in ['bool', 'string'] or rs_type in ['bool', 'string']:
            raise Exception(f"Variables of type 'bool' or 'string' cannot use operator '{op}'")
        elif ls_type == rs_type:
            return {'value': ls_val * rs_val, 'type': ls_type}
        elif ls_type in ['int', 'double'] and rs_type in ['int', 'double']:
            return {'value': ls_val * rs_val, 'type': 'double'}
        else:
            raise Exception(f"Variables of type '{ls_type}' and '{rs_type}' cannot use operator '{op}'")
    def divide(self, x, y):
        op = '/'
        ls_type = x['type']
        rs_type = y['type']
        ls_val = x['value']
        rs_val = y['value']
        if ls_type in ['bool', 'string'] or rs_type in ['bool', 'string']:
            raise Exception(f"Variables of type 'bool' or 'string' cannot use operator '{op}'")
        elif ls_type == rs_type:
            if ls_type == 'double':
                return {'value': ls_val / rs_val, 'type': ls_type}
            else:
                return {'value': int(ls_val // rs_val), 'type': ls_type}
        elif ls_type in ['int', 'double'] and rs_type in ['int', 'double']:
            return {'value': ls_val / rs_val, 'type': 'double'}
        else:
            raise Exception(f"Variables of type '{ls_type}' and '{rs_type}' cannot use operator '{op}'")
    def mod(self, x, y):
        op = '%'
        ls_type = x['type']
        rs_type = y['type']
        ls_val = x['value']
        rs_val = y['value']
        if ls_type == 'int' and rs_type == 'int':
            return {'value': int(ls_val % rs_val), 'type': ls_type}
        elif ls_type in ['int', 'double'] and rs_type in ['int', 'double']:
            return {'value': ls_val % rs_val, 'type': 'double'}
        else:
            raise Exception(f"Variables of type '{ls_type}' and '{rs_type}' cannot use operator '{op}'")
    def power(self, x, y):
        op = '^'
        ls_type = x['type']
        rs_type = y['type']
        ls_val = x['value']
        rs_val = y['value']
        if ls_type == 'int' and rs_type == 'int':
            return {'value': int(ls_val ** rs_val), 'type': ls_type}
        elif ls_type in ['int', 'double'] and rs_type in ['int', 'double']:
            return {'value': ls_val ** rs_val, 'type': 'double'}
        else:
            raise Exception(f"Variables of type '{ls_type}' and '{rs_type}' cannot use operator '{op}'")
    def neg(self, x):
        op = '-'
        ls_type = x['type']
        ls_val = x['value']
        if ls_type in ['int', 'double']:
            return {'value': -ls_val, 'type': ls_type}
        else:
            raise Exception(f"Variable of type '{ls_type}' cannot use operator '{op}'")

    def eval_exp(self, tree, env):
        nodetype = tree[0]
        result = None
        if nodetype == "exp":
            result = self.eval_exp(tree[1], env)
        elif nodetype == "identifier":
            result = self.env_lookup(env, tree[1])
        elif nodetype == "double":
            result = {'value': float(tree[1]), 'type': 'double'}
        elif nodetype == "int":
            result = {'value': int(tree[1]), 'type': 'int'}
        elif nodetype == "char":
            result = {'value': tree[1], 'type': 'char'}
        elif nodetype == "bool":
            b = tree[1]
            if b == "true":
                result = {'value': True, 'type': 'bool'}
            elif b == "false":
                result = {'value': False, 'type': 'bool'}
            else:
                Exception(f'Value not understood for bool type: {b}')
        elif nodetype == "string":
            result = {'value': tree[1], 'type': 'string'}
        elif nodetype == "post-plusplus":
            result = self.env_lookup(env, tree[1])
            if result['type'] == 'int':
                self.env_update(env, tree[1], {'value': result['value'] + 1, 'type': result['type']})
            else:
                raise Exception(f"++ can only be used with int type, '{tree[1]}' is type {result['type']}")
        elif nodetype == "pre-plusplus":
            result = self.env_lookup(env, tree[1])
            if result['type'] == 'int':
                result['value'] += 1
                self.env_update(env, tree[1], result)
            else:
                raise Exception(f"++ can only be used with int type, '{tree[1]}' is type {result['type']}")
        elif nodetype == "post-minusminus":
            result = self.env_lookup(env, tree[1])
            if result['type'] == 'int':
                self.env_update(env, tree[1], {'value': result['value'] - 1, 'type': result['type']})
            else:
                raise Exception(f"-- can only be used with int type, '{tree[1]}' is type {result['type']}")
        elif nodetype == "pre-minusminus":
            result = self.env_lookup(env, tree[1])
            if result['type'] == 'int':
                result['value'] -= 1
                self.env_update(env, tree[1], result['value'])
            else:
                raise Exception(f"-- can only be used with int type, '{tree[1]}' is type {result['type']}")
        elif nodetype == "plus":
            ls = self.eval_exp(tree[1], env)
            rs = self.eval_exp(tree[2], env)
            result = self.plus(ls, rs)
        elif nodetype == "minus":
            ls = self.eval_exp(tree[1], env)
            rs = self.eval_exp(tree[2], env)
            result = self.minus(ls, rs)
        elif nodetype == "multiply":
            ls = self.eval_exp(tree[1], env)
            rs = self.eval_exp(tree[2], env)
            result = self.multiply(ls, rs)
        elif nodetype == "divide":
            ls = self.eval_exp(tree[1], env)
            rs = self.eval_exp(tree[2], env)
            result = self.divide(ls, rs)
        elif nodetype == "MOD":
            ls = self.eval_exp(tree[1], env)
            rs = self.eval_exp(tree[2], env)
            result = self.mod(ls, rs)
        elif nodetype == "POWER":
            ls = self.eval_exp(tree[1], env)
            rs = self.eval_exp(tree[2], env)
            result = self.power(ls, rs)
        elif nodetype == "NEG":
            rs = self.eval_exp(tree[1], env)
            result = self.neg(rs)
        elif nodetype == "not":
            ls = self.eval_exp(tree[1], env)
            result = {'value': not ls['value'], 'type': 'bool'}
        elif nodetype == "and":
            ls = self.eval_exp(tree[1], env)
            rs = self.eval_exp(tree[2], env)
            result = {'value': ls['value'] and rs['value'], 'type': 'bool'}
        elif nodetype == "or":
            ls = self.eval_exp(tree[1], env)
            rs = self.eval_exp(tree[2], env)
            result = {'value': ls['value'] or rs['value'], 'type': 'bool'}
        elif nodetype == "LT":
            ls = self.eval_exp(tree[1], env)
            rs = self.eval_exp(tree[2], env)
            result = {'value': ls['value'] < rs['value'], 'type': 'bool'}
        elif nodetype == "GT":
            ls = self.eval_exp(tree[1], env)
            rs = self.eval_exp(tree[2], env)
            result = {'value': ls['value'] > rs['value'], 'type': 'bool'}
        elif nodetype == "LE":
            ls = self.eval_exp(tree[1], env)
            rs = self.eval_exp(tree[2], env)
            result = {'value': ls['value'] <= rs['value'], 'type': 'bool'}
        elif nodetype == "GE":
            ls = self.eval_exp(tree[1], env)
            rs = self.eval_exp(tree[2], env)
            result = {'value': ls['value'] >= rs['value'], 'type': 'bool'}
        elif nodetype == "NE":
            ls = self.eval_exp(tree[1], env)
            rs = self.eval_exp(tree[2], env)
            result = {'value': ls['value'] != rs['value'], 'type': 'bool'}
        elif nodetype == "EQ":
            ls = self.eval_exp(tree[1], env)
            rs = self.eval_exp(tree[2], env)
            result = {'value': ls['value'] == rs['value'], 'type': 'bool'}
        return result
    def interpretNameSpace(self, trees, parentenv):
        env = {}
        if parentenv is not None:
            env['parent'] = parentenv

        for tree in trees:
            nodetype = tree[0]
            if nodetype == "stmt":
                self.eval_stmt(tree[1], env)
            elif nodetype == "if":
                if_namespaces = tree[1]
                el_namespace = tree[2]
                met = False
                for if_namespace in if_namespaces:
                    condition_exp = if_namespace[0]
                    namespace = if_namespace[1]
                    result = self.eval_exp(condition_exp, env)
                    if result['value']:
                        met = True
                        self.interpretNameSpace(namespace, env)
                        break
                if not met:
                    self.interpretNameSpace(el_namespace, env)
            else:
                print(f"Unknown node type : {nodetype}")
    def interpret(self, trees):
        try:
            print("OUTPUT:")
            self.interpretNameSpace(trees, None)
        except Exception as e:
            print(e)


def run(code, print_tokens=False, print_tree=False):
    dalexer = lex.lex(module=tokenizer)

    # Tokenize
    dalexer.input(code)
    if print_tokens:
        while True:
            tok = dalexer.token()
            if not tok: 
                break
            print(tok)
    
    # Parse
    daparser = yacc.yacc(module=parser)
    parse_tree = daparser.parse(code, lexer=dalexer)
    if print_tree:
        for t in parse_tree:
            print(t)
    
    # Interprets
    dainterpreter = Interpreter()
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
