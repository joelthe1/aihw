import re
from copy import deepcopy

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

class Clause:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

def unify(x, y, theta = {}):
    if theta is None:
        return False
    elif x == y:
        return theta
    elif isinstance(x, Variable):
        return unify_var(x, y, theta)
    elif isinstance(y, Variable):
        return unify_var(y, x, theta)
    elif isinstance(x, Compound) and isinstance(y, Compound):
        return unify(x.args, y.args, unify(x.op, y.op, theta))
    elif type(x) is list and type(y) is list:
        return unify(x[1:], y[1:], unify(x[0], y[0], theta))
    else:
        return None

def unify_var(var, x, theta):
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
        return True
    elif isinstance(x, Variable) and x.value in theta:
        return occur_check(var, theta[x.value], theta)
    elif isinstance(x, Compound):
        o1 = occur_check(var, x.op, theta)
        o2 = occur_check(var, x.args, theta)
        return o1 or o2
    elif type(x) is list:
        for e in x:
            if occur_check(var, e, theta):
                return True
    else:
        return False

#def fol_bc_ask(kb, query):
#    return fol_bc_or(kb, query, {})

#def fol_bc_or(kb, goal, theta):
    

def subs(theta, var):
    var_copy = deepcopy(var)
    if len(theta) == 0:
        return var_copy
    for val in var_copy.args:
        if isinstance(val, Variable) and val.value in theta:
            val.value = theta[val.value]
    print var_copy
    return var_copy

def objectify(var):
    global var_counter
    global kb
    var_map = {}
    arg_list = []
    results = []
    print 'printing var', var
    for sentence in var:
        match = re.match(r'([~A-Z].*?)[(](.*)[)]', sentence)
        op_str = match.group(1)
        args_str = match.group(2)
        args = args_str.split(',')
        print args
        for val in args:
            var_match = re.match(r'^[a-z]', val)
            constt_match = re.match(r'^[A-Z].*', val)
            if var_match is not None:
                if var_match.group(0) in var_map:
                    temp_var = Variable(var_map[var_match.group(0)])
                else:    
                    var_map[var_match.group(0)] = 'x_%d' % var_counter
                    temp_var = Variable(var_map[var_match.group(0)])
                arg_list.append(temp_var)
                var_counter += 1
            elif constt_match is not None:
                arg_list.append(Constant(constt_match.group(0)))
        temp_comp = Compound(op_str, arg_list)
        arg_list = []
        results.append(temp_comp)
    if len(results) > 1:
        c = Clause(results[:-1], results[-1])
    else:
        c = Clause(results[0], True)
    kb.append(c)
        
var_counter = 0
queries = []
clauses = {}
objs = []
kb = []
with open('input.txt') as inp:
    num_queries = int(inp.readline())
    for x in range(num_queries):
        queries.append(inp.readline()[:-1])
    
    num_clauses = int(inp.readline())
#    num_clauses = 1 #Testing
    for x in range(num_clauses):
        line = inp.readline()[:-1]
        clause = [x.strip() for x in line.split('=>')]
        objectify(clause)
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

#objectify(['Asdlkf(x,y,Goal)','Box(x,Ant,y)'])
print kb
#print len(kb), kb[0].lhs[0].args[1].value, kb[0].rhs.args[2].value

t2 = unify(kb[0].lhs[0], kb[0].rhs)
print 'united', t2
temp = subs({'x_1':'Alice', 'x_0':'Bob'}, kb[0].rhs)
print temp.op
print temp.args[0].value
print temp.args[1].value
print temp.args[2].value
