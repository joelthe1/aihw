import re
from copy import deepcopy
import sys

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
    elif isinstance(x, Constant) and isinstance(y, Constant):
        if x.value == y.value:
                return theta
        return None
    elif isinstance(x, Variable):
        return unify_var(x, y, theta)
    elif isinstance(y, Variable):
        return unify_var(y, x, theta)
    elif isinstance(x, Compound) and isinstance(y, Compound):
        return unify(x.args, y.args, unify(x.op, y.op, theta))
    elif type(x) is list and type(y) is list and len(x) == len(y):
        if len(x) == 0:
            return theta
        return unify(x[1:], y[1:], unify(x[0], y[0], theta))
    else:
        return None

def unify_var(var, x, theta):
    if var.value in theta:
        return unify(theta[var.value], x, theta)
    elif isinstance(x, Constant):
        if x.value in theta:
            return unify(var, theta[x.value], theta)
    elif isinstance(x, basestring):
        if x in theta:
            return unify(var, theta[x.value], theta)
    theta_copy = dict(theta)
    if not isinstance(x, basestring):
        theta_copy[var.value] = x.value
    else:
        theta_copy[var.value] = x
    return theta_copy
        
def subs(theta, var):
    var_copy = deepcopy(var)
    if len(theta) == 0:
        return var_copy
    for index,val in enumerate(var.args):
        if isinstance(val, Variable) and val.value in theta:
            if theta[val.value][:2] == 'x_':
                var_copy.args[index].value = theta[val.value]
            else:
                var_copy.args[index] = Constant(theta[val.value])
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
                arg_list.append(Variable(var_match.group(0)))
            elif constt_match is not None:
                arg_list.append(Constant(constt_match.group(0)))
        temp_comp = Compound(op_str, arg_list)
        arg_list = []
        results.append(temp_comp)
    if len(results) > 1:
        return Clause(results[:-1], results[-1])
    else:
        return Clause(True, results[0])

def standardize(clause):
    global var_counter
    var_map = {}
    for ar in clause.rhs.args:
        if isinstance(ar, Variable):
            if ar.value in var_map:
                ar.value = var_map[ar.value]
            else:
                temp = ar.value
                ar.value = 'x_%d' % var_counter
                var_map[temp] = ar.value
                var_counter += 1
        
    if clause.lhs is not True:
        for l in clause.lhs:
            for ar in l.args:
                if isinstance(ar, Variable):
                    if ar.value in var_map:
                        ar.value = var_map[ar.value]
                    else:
                        temp = ar.value
                        ar.value = 'x_%d' % var_counter
                        var_map[temp] = ar.value
                        var_counter += 1
    return clause
                        
def fol_ask(query, theta = {}):
    print
    print '####', query.op
    rets = []
    for c in kb:
        clause = deepcopy(c)
        clause = standardize(clause)
        s = unify(clause.rhs, query, theta)
        print 's is ', s
        if s is None:
            continue
        elif clause.lhs == True:
            return s
        else:
            for p in clause.lhs:
                rets = []
                sub_p = subs(s, p)
                ret_theta = fol_ask(sub_p, s)
                rets.append(ret_theta)
                if ret_theta == None:
                    break
            if None not in rets:
                return s
    return None

var_counter = 0
queries = []
clauses = {}
objs = []
kb = []
inputFile = sys.argv[2]
with open(inputFile) as inp:
    num_queries = int(inp.readline())
    for x in range(num_queries):
        query = [inp.readline()[:-1]]
        queries.append(objectify(query).rhs)

    num_clauses = int(inp.readline())
    for x in range(num_clauses):
        line = inp.readline()[:-1]
        clause = [x.strip() for x in line.split('=>')]
        if len(clause) > 1:
            lhs = [x.strip() for x in clause[0].split('^')]
            clause = lhs + [clause[-1]]
        kb.append(objectify(clause))

wfile = open('output.txt','w')
print len(kb)
for query in queries:
    answer = fol_ask(query)
    if answer is None:
        wfile.write('FALSE\n')
    else:
        wfile.write('TRUE\n')
    break
wfile.close()
