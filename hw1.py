from collections import deque
from collections import OrderedDict

def build_graph(order=False):
    global algo, src, dest, mids, pipesNum, pipes, startTime, graph
    graph.clear()
    graph[src] = {}
    for nodes in dest:
        graph[nodes] = {}
    for nodes in mids:
        graph[nodes] = {}
    for x in range(pipesNum):
        temp = pipes[x].split(' ')
        graph[temp[0]][temp[1]] = (temp[2:3] + temp[4:])
    for key in graph:
        d = graph[key]
        if d:
            od = OrderedDict(sorted(d.items(), key=lambda t: t[0], reverse=order))
            graph[key] = od
    for k,v in graph.iteritems():
        for k2, v2 in v.iteritems():
            print k + ' ---> ' + k2

def dfs(s):
    global graph, startTime, dest
    explored = []
    temp = []
    stack = [s]
    while True:
        if not stack:
            print 'None'
            return False
        node = stack.pop()
        explored.append(node)
        if node in dest:
            print node, startTime + len(explored) - 1
            return node
        children = graph[node]
        if children:
            for keys in children:
                if keys not in explored:
                    stack.append(keys)

def bfs(g, s, d, st):
    print "and here"
    explored = []
    frontier = deque(s)
#    if s in d:
#        print s
#        return
    while g:
        if not frontier:
            print explored
            return False
        node = frontier.popleft()
        explored.append(node)
        children = g[node]
        if children:
            for keys in children:
                if not keys in frontier and not keys in explored:
 #                   if keys in d:
#                        print explored
 #                       return
                    frontier.append(keys)

with open('graph-input.txt') as inp:
    testCases = int(inp.readline().strip())
    graph = {}
    for x in range(testCases):
        algo = inp.readline().strip()
        src = inp.readline().strip()
        dest = inp.readline().strip().split(' ')
        mids = inp.readline().strip().split(' ')
        pipesNum = int(inp.readline().strip())
        pipes = []
        for y in range(pipesNum):
            pipes.append(inp.readline().strip())
        startTime = int(inp.readline().strip())
        inp.readline()
        build_graph(True)
        #TODO: Add handler for invalid start node.
        if algo.lower() == 'dfs':
            dfs(src)
#        if algo.lower() == 'bfs'
