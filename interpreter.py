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
            env[identifier] = value
        else:
            raise Exception('RedeclarationError')
    # Env Update
    def env_update(self, env, identifier, value):
        var_env = self.find_env(env, identifier)
        if var_env is None:
            raise Exception(f"Variable '{identifier}' not declared")
        else:
            var_env[identifier] = value
    def eval_compoundstmt(self, stmts, parentenv):
        env = {'parent': parentenv}
        for stmt in stmts:
            self.eval_stmt(stmt, env)
    def eval_stmt(self, tree, env):
        stmttype = tree[0]
        if stmttype == "console":
            exps = tree[1]
            print('CONSOLE-> ', end='')
            for exp in exps:
                result = self.eval_exp(exp, env)
                print(result['value'], end=' ')
            print()
        elif stmttype == "init":
            identifier = tree[1]
            dtype = tree[2]
            if tree[3] is not None:
                result = self.eval_exp(tree[3], env)
            else:
                result = {'value': self.DEFAULT[dtype], 'type': dtype}
            self.env_declare(env, identifier, result)
        elif stmttype == "exp":
            result = self.eval_exp(tree[1], env)
        elif stmttype == "assign":
            identifier = tree[1]
            result = self.eval_exp(tree[2], env)
            self.env_update(env, identifier, result)
        elif stmttype == "if":
            condition_exp = self.eval_exp(tree[1], env)
            ef_stmts = tree[3]
            if condition_exp:
                self.eval_compoundstmt(tree[2], env)
            else:
                met = False
                for ef_stmt in ef_stmts:
                    condition_exp = self.eval_exp(ef_stmt[1], env)
                    if condition_exp:
                        self.eval_compoundstmt(ef_stmt[2], env)
                        met = True
                        break
                if not met:
                    el_stmts = tree[4]
                    self.eval_compoundstmt(el_stmts, env)
        
    def plus(self, x, y):
        return {'value': x['value'] + y['value'], 'type': x['type']}
    def minus(self, x, y):
        return {'value': x['value'] - y['value'], 'type': x['type']}
    def multiply(self, x, y):
        return {'value': x['value'] * y['value'], 'type': x['type']}
    def divide(self, x, y):
        return {'value': x['value'] / y['value'], 'type': x['type']}
    def mod(self, x, y):
        return {'value': x['value'] % y['value'], 'type': x['type']}
    def power(self, x, y):
        return {'value': x['value'] ** y['value'], 'type': x['type']}
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