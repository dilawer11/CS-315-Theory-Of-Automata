class Interpreter:
    DEFAULT = {
        'int': 0,
        'string': "",
        'char': '\0',
        'double': 0.0,
        'bool': False,
    }
    def __init__(self, name="A Test Program"):
        self.name = name
    def find_env(self, env, identifier):
        if identifier in env:
            return env
        elif 'parent' in env:
            return find_env(env['parent'], identifier)
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
    def eval_compoundstmt(self, stmts, parentenv):
        env = {'parent': parentenv}
        for stmt in stmts:
            nodetype = stmt[0]
            if nodetype == 'stmt':
                self.eval_stmt(stmt[1], env)
    def eval_stmt(self, tree, env):
        stmttype = tree[0]
        if stmttype == "console":
            exps = tree[1]
            print('CONSOLE-> ', end='')
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
        elif stmttype == "if":
            condition_exp = self.eval_exp(tree[1], env)
            ef_stmts = tree[3]
            if condition_exp['value']:
                self.eval_compoundstmt(tree[2], env)
            else:
                met = False
                for ef_stmt in ef_stmts:
                    condition_exp = self.eval_exp(ef_stmt[1], env)
                    if condition_exp['value']:
                        self.eval_compoundstmt(ef_stmt[2], env)
                        met = True
                        break
                if not met and tree[4]:
                    el_stmts = tree[4][1]
                    self.eval_compoundstmt(el_stmts, env)
        
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
    def interpret(self, trees):
        global_env = {}
        try:
            for tree in trees:
                nodetype = tree[0]
                if nodetype == "stmt":
                    self.eval_stmt(tree[1], global_env)
                else:
                    print(f"Unknown node type : {nodetype}")
        except Exception as e:
            print()
            print(e.with_traceback(e.__traceback__))

#TODO char -> ord -> chr
#TODO Strict Type Checking