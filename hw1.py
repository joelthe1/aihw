def build_graph(f):
    graph = {}
    print 'here'
    x = 0
    y = 0
    for line in f:
#        print line.strip()
        if line.strip() == '':
            break
        if x >= 0 and x < 3:
            nodes = line.strip().split(' ')
#            print nodes
            for node in nodes:
                graph[node] = {}
        elif x == 3:
            y = int(line.strip())
        elif x > 3 and x <= (3+y):
            pipes = line.strip().split(' ')
            tempList = []
#            print pipes
            pipeLength = int(pipes[2])
            tempList.append(pipeLength)
            tempList.extend(pipes[4:])
            print pipes[1], tempList
            graph[pipes[0]][pipes[1]] = tempList
        x += 1
    return graph
    
def dfs(g, s):
    explored = []
    temp = []
    stack = [s]
    while g:
        if not stack:
            return False
        node = stack.pop()
        print node
        if node in explored:
            continue
        explored.append(node) 
        children = g[node]
        if children:
            for keys in children:
                stack.append(keys)
#            temp = sorted(temp, key=str.lower, reverse=True)
 #           stack = stack + temp
#            print stack
        
                
        

with open('graph-input.txt') as inp:
    print inp.readline().strip()    
    print inp.readline().strip()
    graph = build_graph(inp)
    print graph
    dfs(graph, 'A')

