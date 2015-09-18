from collections import deque
from collections import OrderedDict
import heapq
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
#    print graph

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

def inOffTime(periods, epoch):
    offTimes = set()
    if len(periods) <= 1:
        return False
    slots = periods[1:]
    for s in slots:
        t = s.split('-')
        for x in range(int(t[0]), int(t[1]) + 1):
            offTimes.add(x)
    if epoch%24 in periods:
        return True
                                        
def ucs(s):
    global graph, startTime, dest
    closed = []
    openq = []
    heapq.heappush(openq, (0, s))
    while True:
        if not openq:
            print 'None'
            return
        node = heapq.heappop(openq)
        if node[1] in dest:
            print node[1], (node[0] + startTime)%24
            return
        children = graph[node[1]]
        if children:
            for child in children:
                flag = False
                childCost = int(children[child][0]) + node[0]
                if inOffTime(children[child], node[0]):
                    continue
                for vals in openq:
                    if vals[1] == child:
                        if vals[0] > childCost:
                            print openq.index(vals)
                            openq[openq.index(vals)] = (childCost, child)
                            heapq.heapify(openq)
#                            heapq.heappush(openq, (childCost, child))
                            flag = True
                            break
                if flag:
                    continue
                for vals in closed:
                    if vals[1] == child:
                        if vals[0] > childCost:
                            closed.remove(closed.index(vals))
                            heapq.heappush(openq, (childCost, child))
                            flag = True
                            break
                if flag:
                    continue
                else:
                    heapq.heappush(openq, (childCost, child))
        closed.append(node)
                        
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
        elif algo.lower() == 'ucs':
            print 
            build_graph(False)            
            ucs(src)
