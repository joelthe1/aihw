import re

class Constant:
    def __init__(self, cname):
        self.value = cname

class Variable:
    def __init__(self, vname):
        self.value = vname

class Compound:
    def __init__(self, op, args):
        self.op = op
        self.args = args

def unify(x, y, theta = {}):
#    print x, y, theta
    if theta is None:
#        print 'doing this'
        return False
    elif x == y:
#        print 'not here1'
        return theta
    elif isinstance(x, Variable):
#        print 'not here2'
        return unify_var(x, y, theta)
    elif isinstance(y, Variable):
#        print 'not here3'
        return unify_var(y, x, theta)
    elif isinstance(x, Compound) and isinstance(y, Compound):
#        print 'not here4'
        return unify(x.args, y.args, unify(x.op, y.op, theta))
    elif type(x) is list and type(y) is list:
#        print 'not here5'
        return unify(x[1:], y[1:], unify(x[0], y[0], theta))
    else:
#        print 'here finally'
        return None

def unify_var(var, x, theta):
#    print 'printing theta', theta
    if var.value in theta:
        return unify(theta[var.value], x, theta)
    elif x.value in theta:
        return unify(var, theta[x.value], theta)
    elif occur_check(var, x, theta):
        return None
    else:
        theta_copy = dict(theta)
        theta_copy[var.value] = x.value
        return theta_copy

def occur_check(var, x, theta):
    if var == x:
#        print 'doing this', var, x
        return True
    elif isinstance(x, Variable) and x.value in theta:
#        print 'in 2', x.value
        return occur_check(var, theta[x.value], theta)
    elif isinstance(x, Compound):
#        print 'now in this', x.op, x.args
        o1 = occur_check(var, x.op, theta)
#        print 'after this'
        o2 = occur_check(var, x.args, theta)
        return o1 or o2
    elif type(x) is list:
#        print 'and in this', x
        for e in x:
#            print e
            if occur_check(var, e, theta):
                return True
    else:
        return False

def standardize_variables(var):
    if not isinstance(var, Compound):
        return var
    elif isinstance(var, Compound):
        if val in var.args:
            if isinstance(val, Variable):
                pass
        
#def fol_bc_ask(kb, query):
#    return fol_bc_or(kb, query, {})

#def fol_bc_or(kb, goal, theta):
    

def objectify(var):
    global var_counter
    var_map = {}
    arg_list = []
    for sentence in var:
        match = re.match(r'([~A-Z].*?)[(](.*)[)]', sentence)
        op_str = match.group(1)
        args_str = match.group(2)
        args = args_str.split(',')
        print args
        for val in args:
            var_match = re.match(r'^[a-z]', val)
            if var_match is not None:
                print var_match.group(0)
                var_map[var_match.group(0)] = 'x_%d' % var_counter
                temp_var = Variable(var_map[var_match.group(0)])
                arg_list.append(temp_var)
                var_counter += 1

        temp_comp = Compound(op_str, arg_list)
        print 'here'
        print temp_comp.op
        print temp_comp.args

        
var_counter = 0
queries = []
clauses = {}
objs = []
with open('input.txt') as inp:
    num_queries = int(inp.readline())
    for x in range(num_queries):
        queries.append(inp.readline()[:-1])
#    print queries
    
    num_clauses = int(inp.readline())
    for x in range(num_clauses):
        line = inp.readline()[:-1]
        clause = [x.strip() for x in line.split('=>')]
#        for c in clause:
        print clause

con_bob = Constant('Bob')
con_alice = Constant('Alice')
print con_bob.value
print con_alice.value

var_x = Variable('x')
var_y = Variable('y')
print var_x.value
print var_y.value

l1 = [var_x, var_y]
l2 = [con_bob, con_alice]



comp_dxy = Compound('D', [var_x, var_y])
comp_edxy = Compound('E', [comp_dxy, var_y])

comp_djb = Compound('D', [con_bob, con_alice])
print comp_dxy.op
print comp_dxy.args[0].value
print comp_djb.op
print comp_djb.args[0].value
print hasattr(comp_djb, '__class__')
print 'here'
print unify(comp_dxy, comp_djb)
print unify(con_bob, var_x)

print occur_check(var_y, comp_dxy, {})

objectify(['Asdlkf(x,y,Goal)','Box(x,Ant,y)'])
