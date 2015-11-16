class Constant:
    def __init__(self, cname):
        self.cname = cname
        self.type = 'const'

class Variable:
    def __init__(self, vame):
        self.vname = vname
        self.type = 'var'

class Compound:
    def __init__(self, op, args):
        self.op = op
        self.args = args
        self.type = 'comp'

class List:
    def __init__(self, values):
        self.values = values
        self.type = 'list'

def unify(x, y, theta = {}):
    if not theta:
        return False
    elif x == y:
        return theta
    elif x.type == 'var':
        return unify_var(x, y, theta)
    elif y.type == 'var':
        return unify_var(y, x, theta)
    elif x.type == 'comp' and y.type == 'comp':
        return unify(x.args, y.args, unify(x.op, y.op, theta))
    elif x.type == 'list' and y.type == 'list':
        return unify(x.values[1:], y.values[1:], unify(x[0], y[0], theta))
    else:
        return False

def unify_var(var, x, theta):
    if var in theta:
        return unify(theta[var], x, theta)
    elif x in theta:
        return unify(var, theta[x], theta)
    #TO DO: OccurCheck
    else:
        theta[var] = x
        return theta
    
queries = []
clauses = {}
with open('input.txt') as inp:
    num_queries = int(inp.readline())
    for x in range(num_queries):
        queries.append(inp.readline()[:-1])
    print queries
    
    num_clauses = int(inp.readline())
    for x in range(num_clauses):
        line = inp.readline()[:-1]
        clause = line.split('=>')
        print clause

