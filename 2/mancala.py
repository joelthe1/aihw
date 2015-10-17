import operator

def minimax(state):
    moves = []
    max_root = float('-inf')
    next_moves = actions(state, 'max')
    print next_moves
    for index, s in enumerate(next_moves):
        if s:
            continue_flag = continue_move(state, s, 'max')
            if continue_flag:
                temp = minimax_max(s, 1, index+2, my_player)
            else:
                temp = minimax_min(s, 1, index+2, my_player)
            moves.append(temp)
            moves.append(s)
            if temp > max_root:
                max_root = temp
            wfile.write('root'+','+'0,'+str(max_root)+'\n')
    print moves
    scoreArr = [x for i,x in enumerate(moves) if i%2 == 0]
    i, value = max(enumerate(scoreArr), key=operator.itemgetter(1))
    print value, moves[i*2 + 1]
    max_state = moves[i*2 + 1]
    next_legal_state(state, max_state)

def next_legal_state(parent, child):
    global terminator
    if continue_move(parent, child, 'max'):
        preq_moves = actions(child, 'max')
        for preq_s in preq_moves:
            if preq_s:
                next_legal_state(child, preq_s)
    if terminator == 0:
        terminator += 1
        print evaluate(child), child

def terminal_case(state, depth, p_type):
#    if depth > cutoff_depth:
#        return True
    if depth == cutoff_depth:
        next_moves = actions(state, p_type)
        for s in next_moves:
            if s:
                continue_flag = continue_move(state, s, p_type)
                if continue_flag == True:
                    return False
    elif depth < cutoff_depth:
        return False
    return True

def endgame(state, p_type, player):
    end_state = state[:]
    if player == 1:
        for x in range(p1_mancala + 1, p2_mancala):
            end_state[p2_mancala] += end_state[x]
            end_state[x] = 0
        return end_state
    else:
        for x in range(p1_mancala):
            end_state[p1_mancala] += end_state[x]
            end_state[x] = 0
        return end_state
    
def minimax_max(state, depth, pit, player):
    if terminal_case(state, depth, 'max'):
        leaf_value = evaluate(state)
        coins = 0
        if player == 1:
            for x in range(p1_mancala):
                coins += state[x]
            if coins == 0:
                end_state = endgame(state, my_player)
                leaf_value = evaluate(end_state)
        else:
            for x in range(p1_mancala+1, p2_mancala):
                coins += state[x]
            if coins == 0:
                end_state = endgame(state, my_player)
                leaf_value = evaluate(end_state)
        wfile.write(myChar+str(pit)+','+str(depth)+','+str(leaf_value)+'\n')
        return leaf_value
    value = float('-inf')
    wfile.write(myChar+str(pit)+','+str(depth)+','+str(value)+'\n')
    for index, s in enumerate(next_moves):
        if s:
            continue_flag = continue_move(state, s, 'max')
            if depth == cutoff_depth and continue_flag:
                value = max(value, minimax_max(s, depth, index+2, player))
            elif continue_flag:
                value = max(value, minimax_max(s, depth, index+2, player))
            else:
                value = max(value, minimax_min(s, depth + 1, index+2, 1 if player == 2 else 2))
            wfile.write(myChar+str(pit)+','+str(depth)+','+str(value)+'\n')
    return value

def minimax_min(state, depth, pit, player):
    if terminal_case(state, depth, 'min'):
        leaf_value = evaluate(state)
        coins = 0
        if player == 1:
            for x in range(p1_mancala):
                coins += state[x]
            if coins == 0:
                end_state = endgame(state, player)
                leaf_value = evaluate(end_state)
        else:
            for x in range(p1_mancala+1, p2_mancala):
                coins += state[x]
            if coins == 0:
                end_state = endgame(state, player)
                leaf_value = evaluate(end_state)
        wfile.write(oppChar+str(pit)+','+str(depth)+','+str(leaf_value)+'\n')
        return leaf_value
    value = float('inf')
    wfile.write(oppChar+str(pit)+','+str(depth)+','+str(value)+'\n')
    if continue_flag:
        next_moves = actions(state, 'min')
    else:
        next_moves = actions(state, 'max')
    for index, s in enumerate(next_moves):
        if s:
            continue_flag = continue_move(state, s, 'min')
            if depth == cutoff_depth and continue_flag:            
                value = min(value, minimax_min(s, depth, index+2, player))
            elif continue_flag:
                value = min(value, minimax_min(s, depth, index+2, player))
            else:
                value = min(value, minimax_max(s, depth + 1, index+2, 1 if player == 2 else 2))
            wfile.write(oppChar+str(pit)+','+str(depth)+','+str(value)+'\n')
    return value

def evaluate(state):
    return state[p1_mancala] - state[p2_mancala]
    
def continue_move(parent, child, p_type):
    if p_type == 'max':
        if my_player == 1:
            if ((child[p1_mancala] - parent[p1_mancala]) - (child[p1_mancala+1] - parent[p1_mancala+1])) == 1:
#                wfile.write('doing this: max p1 true.\n')
                return True
            return False
        elif my_player == 2:
            if ((child[p2_mancala] - parent[p2_mancala]) - (child[0] - parent[0])) == 1:
#                wfile.write('doing this: max p2 true.\n')                
                return True
            return False
    elif p_type == 'min':
        if my_player == 1:
            if ((child[p2_mancala] - parent[p2_mancala]) - (child[0] - parent[0])) == 1:
#                wfile.write('doing this: min p1 true.\n')
                return True
#            wfile.write('doing this: min p1 false.\n')            
            return False
        elif my_player == 2:
            if ((child[p1_mancala] - parent[p1_mancala]) - (child[p1_mancala+1] - parent[p1_mancala+1])) == 1:
#                wfile.write('doing this: min p2 true.\n')
                return True
            return False
    
def actions(state, p_type):
    length = p2_mancala + 1
    action_set = []
    if p_type == 'max':
        if my_player == 1:
             for x in range(p1_mancala):
                if state[x] != 0:
                    temp = state[:]
                    coins = temp[x]
                    temp[x] = 0
                    z = 1
                    for y in range(coins):
                        if ((x+y+z)%(length)) == p2_mancala:
                            z += 1
                        if y == coins-1:
                            if temp[(x+y+z)%(length)] == 0 and ((x+y+z)%(length)) < p1_mancala:
                                if temp[-((x+y+z)%(length))-2] != 0:
                                    temp[p1_mancala] += (temp[-((x+y+z)%(length))-2] + 1)
                                    temp[-((x+y+z)%(length))-2] = 0
                                else:
                                    temp[(x+y+z)%(length)] += 1
                            else:
                                temp[(x+y+z)%(length)] += 1
                        else:
                            temp[(x+y+z)%(length)] += 1
                    action_set.append(temp)
                else:
                    action_set.append([])

        elif my_player == 2:
            for x in range(p1_mancala + 1, p2_mancala):
                if state[x] != 0:
                    temp = state[:]
                    coins = temp[x]
                    temp[x] = 0
                    z = 1
                    for y in range(coins):
                        if ((x+y+z)%(length)) == p1_mancala:
                            z += 1
                        if y == coins-1:
                            if temp[(x+y+z)%(length)] == 0 and ((x+y+z)%(length)) > p1_mancala and ((x+y+z)%(length)) != p2_mancala:
                                if temp[length-((x+y+z)%(length))-2] != 0:
                                    temp[p2_mancala] += (temp[length-((x+y+z)%(length))-2] + 1)
                                    temp[length-((x+y+z)%(length))-2] = 0
                                else:
                                    temp[(x+y+z)%(length)] += 1
                            else:
                                temp[(x+y+z)%(length)] += 1
                        else:
                            temp[(x+y+z)%(length)] += 1
                    action_set.append(temp)
                else:
                    action_set.append([])
            action_set.reverse()

    if p_type == 'min':
        if my_player == 2:
            for x in range(p1_mancala):
                if state[x] != 0:
                    temp = state[:]
                    coins = temp[x]
                    temp[x] = 0
                    z = 1
                    for y in range(coins):
                        if ((x+y+z)%(length)) == p2_mancala:
                            z += 1
                        if y == coins-1:
                            if temp[(x+y+z)%(length)] == 0 and ((x+y+z)%(length)) < p1_mancala:
                                if temp[-((x+y+z)%(length))-2] != 0:
                                    temp[p1_mancala] += (temp[-((x+y+z)%(length))-2] + 1)
                                    temp[-((x+y+z)%(length))-2] = 0
                                else:
                                    temp[(x+y+z)%(length)] += 1
                            else:
                                temp[(x+y+z)%(length)] += 1
                        else:
                            temp[(x+y+z)%(length)] += 1
                    action_set.append(temp)
                else:
                    action_set.append([])

        elif my_player == 1:
            for x in range(p1_mancala + 1, p2_mancala):
                if state[x] != 0:
                    temp = state[:]
                    coins = temp[x]
                    temp[x] = 0
                    z = 1
                    for y in range(coins):
                        if ((x+y+z)%(length)) == p1_mancala:
                            z += 1
                        if y == coins-1:
                            if temp[(x+y+z)%(length)] == 0 and ((x+y+z)%(length)) > p1_mancala and ((x+y+z)%(length)) != p2_mancala:
                                if temp[length-((x+y+z)%(length))-2] != 0:
                                    temp[p2_mancala] += (temp[length-((x+y+z)%(length))-2] + 1)
                                    temp[length-((x+y+z)%(length))-2] = 0
                                else:
                                    temp[(x+y+z)%(length)] += 1
                            else:
                                temp[(x+y+z)%(length)] += 1
                        else:
                            temp[(x+y+z)%(length)] += 1
                    action_set.append(temp)
                else:
                    action_set.append([])
            action_set.reverse()
    return action_set


wfile = open('output.txt', 'w')
wfile.write('Node,Depth,Value\n')    
rfile = 'input.txt' #sys.argv[2]
with open(rfile) as inputFile:
    task = inputFile.readline().strip()
    my_player = int(inputFile.readline().strip())
    cutoff_depth = int(inputFile.readline().strip())
    p2_inp = inputFile.readline().strip().split(' ')
    p1_inp = inputFile.readline().strip().split(' ')
    p2_mancala_inp = inputFile.readline().strip()
    p1_mancala_inp = inputFile.readline().strip()

p1_mancala = len(p1_inp)
p1_inp.append(p1_mancala_inp)
p1 = [int(x) for x in p1_inp]

p2_mancala = 0
p2_inp.reverse()
p2_inp.append(p2_mancala_inp)
p2 = [int(x) for x in p2_inp]

state = p1 + p2
p2_mancala = len(state) - 1

terminator = 0

myChar = 'B'
oppChar = 'A'
opp_player = 2

if my_player == 2:
    myChar = 'A'
    oppChar = 'B'
    opp_player = 1
    

print state
print 'my player:', my_player
#print p1_mancala
#print p2_mancala

print actions(state, 'max')
#print evaluate(state, 'min')

#minimax(state)
wfile.close()
