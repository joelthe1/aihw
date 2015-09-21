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
        graph[temp[0]] = {}
        graph[temp[1]] = {}
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
    parent = {}
    while True:
        if not stack:
            print 'None'
            wfile.write('None\n')
            return
        node = stack.pop()
        explored.append(node)
        if node in dest:
            temp_node = node
            path_time = 0
            while temp_node != s:
                temp_node = parent[temp_node]
                path_time += 1
            time = (startTime + path_time)%24
            print node, time
            wfile.write(node + ' ' + str(time) + '\n')
            return
        children = graph[node]
        if children:
            for keys in children:
                if keys not in explored:
                    stack.append(keys)
                    parent[keys] = node

def bfs(s):
    global graph, startTime, dest
    explored = []
    parent = {}
    frontier = deque()
    frontier.append(s)
    while True:
        if not frontier:
            print 'None'
            wfile.write('None\n')
            return
        node = frontier.popleft()
        explored.append(node)
        if node in dest:
            temp_node = node
            path_time = 0
            while temp_node != s:
                temp_node = parent[temp_node]
                path_time += 1
            time = (startTime + path_time)%24
            print node, time
            wfile.write(node + ' ' + str(time) + '\n')
            return
        children = graph[node]
        if children:
            for keys in children:
                if not keys in frontier and not keys in explored:
                    frontier.append(keys)
                    parent[keys] = node

def inOffTime(periods, epoch):
    offTimes = set()
    if len(periods) <= 1:
        return False
    slots = periods[1:]
    for s in slots:
        t = s.split('-')
        for x in range(int(t[0]), int(t[1]) + 1):
            offTimes.add(x)
    if epoch%24 in offTimes:
        return True
                                        
def ucs(s):
    global graph, startTime, src, dest
    closed = []
    closednodes = []
    openq = []
    opennodes = []
    heapq.heappush(openq, (startTime, s))
    opennodes.append(s)
    while True:
        if not openq:
            print 'None'
            wfile.write('None' + '\n')
            return
        node = heapq.heappop(openq)
        opennodes.remove(node[1])
        if node[1] in dest:
            print node[1], node[0]%24
            wfile.write(node[1] + ' ' + str(node[0]%24) + '\n')
            return
        children = graph[node[1]]
        if children:
            for child in children:
                childCost = int(children[child][0]) + node[0]
                if child not in opennodes and child not in closednodes and not inOffTime(children[child], node[0]):
                    heapq.heappush(openq, (childCost, child))
                    opennodes.append(child)
                elif child in opennodes and not inOffTime(children[child], node[0]):
                    old_child_index = [y[1] for y in openq].index(child)
                    if childCost < openq[old_child_index][0]:
                        del openq[old_child_index]
                        openq.append((childCost, child))
                        heapq.heapify(openq)
                elif child in closednodes and not inOffTime(children[child], node[0]):
                    old_child_index = [y[1] for y in closed].index(child)                    
                    if childCost < closed[old_child_index][0]:
                        del closed[old_child_index]
                        closednodes.remove(child)
                        heapq.heappush(openq, (childCost, child))
                        opennodes.append(child)
        closed.append(node)
        closednodes.append(node[1])
                        
inputFile = sys.argv[2]
wfile = open('output.txt', 'w')
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
            build_graph(False)            
            ucs(src)
wfile.close()
