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
        return None
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

def fol_bc_ask(kb, query):
    return fol_bc_or(kb, query, {})

def fol_bc_or(kb, goal, theta):
    for expr in kb:
        for s in fol_bc_and(kb, expr.lhs, unify(expr.rhs, goal, theta)):
            yield s

def fol_bc_and(kb, goals, theta):
    if theta == None:
        return
    elif len(goals) == 0:
        yield theta
    else:
        first, rest = goals[0], goals[1:]
        for s in fol_bc_or(kb, subs(theta, first), theta):
            for s2 in fol_bc_and(kb, rest, s):
                yield s2

def subs(theta, var):
    var_copy = deepcopy(var)
    if len(theta) == 0:
        return var_copy
    for val in var_copy.args:
        if isinstance(val, Variable) and val.value in theta:
            val.value = theta[val.value]
    return var_copy

def objectify(var):
    global var_counter
    var_map = {}
    arg_list = []
    results = []
    for sentence in var:
        match = re.match(r'([~A-Z].*?)[(](.*)[)]', sentence)
        op_str = match.group(1)
        args_str = match.group(2)
        args = args_str.split(',')
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
        return Clause(results[:-1], results[-1])
    else:
        return Clause([results[0]], True)
        
var_counter = 0
queries = []
clauses = {}
objs = []
kb = []
with open('input.txt') as inp:
    num_queries = int(inp.readline())
    for x in range(num_queries):
        query = [inp.readline()[:-1]]
        queries.append(objectify(query).lhs)
    
    num_clauses = int(inp.readline())
    for x in range(num_clauses):
        line = inp.readline()[:-1]
        clause = [x.strip() for x in line.split('=>')]
        if len(clause) > 1:
            lhs = [x.strip() for x in clause[0].split('^')]
            clause = lhs + [clause[-1]]
        print clause
        v = objectify(clause)
        print v.lhs
        print v.rhs
        kb.append(objectify(clause))

print len(queries)
print len(kb)
print queries[0]
answer = fol_bc_ask(kb, queries[0])
for val in answer:
    print 'the answer is', val
#for query in queries:
#    answer = fol_bc_ask(kb, query)
#    print 'in here'
#    for res in answer:
#        print 'in here again'
#        print res
