from collections import deque
from collections import OrderedDict
import sys

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
#    for k,v in graph.iteritems():
#        for k2, v2 in v.iteritems():
#            print k + ' ---> ' + k2

def dfs(s):
    global graph, startTime, dest
    explored = []
    stack = []
    stack.append(s)
    while True:
        if not stack:
            print 'None'
            return
        node = stack.pop()
        explored.append(node)
        if node in dest:
            print node, startTime + len(explored) - 1
            return
        children = graph[node]
        if children:
            for keys in children:
                if keys not in explored:
                    stack.append(keys)

def bfs(s):
    global graph, startTime, dest
    explored = []
    frontier = deque()
    frontier.append(s)
    while True:
        if not frontier:
            print 'None'
            return
        node = frontier.popleft()
        explored.append(node)
        if node in dest:
            print node, startTime + len(explored) - 1
            return
        children = graph[node]
        if children:
            for keys in children:
                if not keys in frontier and not keys in explored:
                    frontier.append(keys)

def ucs(s):
    print 'in ucs.'

inputFile = sys.argv[2]
with open(inputFile) as inp:
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
        if algo.lower() == 'dfs':
            build_graph(True)
            dfs(src)
        elif algo.lower() == 'bfs':
            build_graph(False)
            bfs(src)
#        elif algo.lower() == 'ucs':
#            print ''
#            print 'ucs'
