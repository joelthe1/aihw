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

