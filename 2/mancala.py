import operator

def alphabeta(state):
    global path
    moves = []
    paths = []
    alpha = float('-inf')
    beta = float('inf')
    max_root = float('-inf')
    next_moves = actions(state, 'max')
    print 'in here', next_moves
    wfile.write('root'+',0,-Infinity,-Infinity,Infinity\n')    
    for index, s in enumerate(next_moves):
        if s:
            continue_flag = continue_move(state, index, 'max')
            if continue_flag:
                print 'contiuing.',s
                temp = alphabeta_max(s, 1, index+2, my_player, continue_flag, alpha, beta)
            else:
                temp = alphabeta_min(s, 1, index+2, my_player, continue_flag, alpha, beta)
            moves.append(temp)
            moves.append(s)
            if temp > max_root:
                max_root = temp
            temp = path[:]
            temp.reverse()
            paths.append(temp)
            path = []
            if max_root >= beta:
                write_out_alphabeta('root', 0, 0, max_root, alpha, beta)
#                wfile.write('root'+','+'0,'+str(max_root)+','+str(alpha)+','+str(beta)+'\n')
                break
            alpha = max(alpha, max_root)
            write_out_alphabeta('root', 0, 0, max_root, alpha, beta)
#            wfile.write('root'+','+'0,'+str(max_root)+','+str(alpha)+','+str(beta)+'\n')            
    print moves
    print len(paths)
    print paths
    scoreArr = [x for i,x in enumerate(moves) if i%2 == 0]
    i, value = max(enumerate(scoreArr), key=operator.itemgetter(1)) #breaks for 0 0 0 input.
    print_node = moves[i*2 + 1]
    for node in paths[i]:
        if node['player'] != my_player:
            break
        print node
        children = actions(print_node, 'max')
        for index, s in enumerate(children):
            if s:
                if index+2 == node['move']:
                    print_node = s
    writeout_next_file(print_node)
    print 'final move', print_node
    print value, moves[i*2 + 1]
    max_state = moves[i*2 + 1]
#    next_legal_state(state, max_state)

def alphabeta_max(state, depth, pit, player, parent_continues, alpha, beta):
    global path
    print 'in max and state = ', state
    my_values = {}
    passed_player = player
    player_char = 'B' if player == 1 else 'A'
    next_moves = actions(state, 'max')
    print player,player_char,pit, depth, next_moves
    if terminal_case(state, depth, 'max', parent_continues):
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
        print 'leaf in max', leaf_value
        write_out_alphabeta(player, pit, depth, leaf_value, alpha, beta)
#        write_out(player, pit, depth, leaf_value)
        my_values['value'] = leaf_value
        my_values['player'] = player
        my_values['pit'] = pit
        path.append(my_values)
        return leaf_value
    value = float('-inf')
    my_values['value'] = value
    write_out_alphabeta(player, pit, depth, value, alpha, beta)
    if parent_continues:
        print 'parent_continues is true.', parent_continues
        child_depth = depth
    else:
        child_depth = depth + 1
        player = 1 if player == 2 else 2
    for index, s in enumerate(next_moves):
        if s:
            continue_flag = continue_move(state, index, 'max' if player == my_player else 'min')
            if depth == cutoff_depth and continue_flag:
                print 'in here',value, s, child_depth, index+2, player
                temp = value
                value = max(value, alphabeta_max(s, child_depth, index+2, player, True, alpha, beta))
                if temp != value:
                    my_values['value'] = value
                    my_values['player'] = player
                    my_values['move'] = index+2
            elif continue_flag:
                print 'in here too',value, s, depth, index+2, player
                temp = value
                value = max(value, alphabeta_max(s, child_depth, index+2, player, True, alpha, beta))
                if temp != value:
                    my_values['value'] = value
                    my_values['player'] = player
                    my_values['move'] = index+2
            else:
                print 'doing min.',value, s, child_depth, index+2, player
                temp = value
                value = max(value, alphabeta_min(s, child_depth, index+2, player, False, alpha, beta))
                if temp != value:
                    my_values['value'] = value
                    my_values['player'] = player
                    my_values['move'] = index+2
            if value >= beta:
                write_out_alphabeta(passed_player, pit, depth, value, alpha, beta)
                return value
            alpha = max(alpha, value)
            write_out_alphabeta(passed_player, pit, depth, value, alpha, beta)
    path.append(my_values)
    return value

def alphabeta_min(state, depth, pit, player, parent_continues, alpha, beta):
    global path
    print 'in min and state = ', state
    my_values = {}
    player_char = 'B' if player == 1 else 'A'
    passed_player = player
    next_moves = actions(state, 'min')
    print player,player_char, depth,pit, next_moves
    print 'parent continues = ', parent_continues
    if terminal_case(state, depth, 'min', parent_continues):
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
        write_out_alphabeta(player, pit, depth, leaf_value, alpha, beta)
        my_values['value'] = leaf_value
        my_values['player'] = player
        my_values['pit'] = pit
        path.append(my_values)
        print ('leaf in min')
        return leaf_value
    value = float('inf')
    my_values['value'] = value
    write_out_alphabeta(player, pit, depth, value, alpha, beta)
    if parent_continues:
        print 'parent_continues is true.', parent_continues
        child_depth = depth
    else:
        child_depth = depth + 1
        player = 1 if player == 2 else 2
    for index, s in enumerate(next_moves):
        if s:
            continue_flag = continue_move(state, index, 'max' if player == my_player else 'min')
            if depth == cutoff_depth and continue_flag:
                print 'in here',value, s, child_depth, index+2, player
                temp = value
                value = min(value, alphabeta_min(s, child_depth, index+2, player, True, alpha, beta))
                if temp != value:
                    my_values['value'] = value
                    my_values['player'] = player
                    my_values['move'] = index+2
            elif continue_flag:
                print 'in here too',value, s, depth, index+2, player
                temp = value
                value = min(value, alphabeta_min(s, child_depth, index+2, player, True, alpha, beta))
                if temp != value:
                    my_values['value'] = value
                    my_values['player'] = player
                    my_values['move'] = index+2
            else:
                print 'doing min.',value, s, child_depth, index+2, player
                temp = value
                value = min(value, alphabeta_max(s, child_depth, index+2, player, False, alpha, beta))
                if temp != value:
                    my_values['value'] = value
                    my_values['player'] = player
                    my_values['move'] = index+2
            if value <= alpha:
                write_out_alphabeta(passed_player, pit, depth, value, alpha, beta)
                return value
            beta = min(beta, value)
            write_out_alphabeta(passed_player, pit, depth, value, alpha, beta)
#            write_out(passed_player, pit, depth, value)                    
    path.append(my_values)
    return value

def minimax(state):
    global path
    moves = []
    paths = []
    max_root = float('-inf')
    next_moves = actions(state, 'max')
    print 'in here', next_moves
    wfile.write('root'+',0,-Infinity\n')    
    for index, s in enumerate(next_moves):
        if s:
            continue_flag = continue_move(state, index, 'max')
            if continue_flag:
                print 'contiuing.',s
                temp = minimax_max(s, 1, index+2, my_player, continue_flag)
            else:
                temp = minimax_min(s, 1, index+2, my_player, continue_flag)
            moves.append(temp)
            moves.append(s)
            if temp > max_root:
                max_root = temp
            wfile.write('root'+','+'0,'+str(max_root)+'\n')
            temp = path[:]
            temp.reverse()
            paths.append(temp)
            path = []
    print moves
    print len(paths)
    print paths
    scoreArr = [x for i,x in enumerate(moves) if i%2 == 0]
    i, value = max(enumerate(scoreArr), key=operator.itemgetter(1)) #breaks for 0 0 0 input.
    print_node = moves[i*2 + 1]
    for node in paths[i]:
        if node['player'] != my_player:
            break
        print node
        children = actions(print_node, 'max')
        for index, s in enumerate(children):
            if s:
                if index+2 == node['move']:
                    print_node = s
    writeout_next_file(print_node)
    print 'final move', print_node
    print value, moves[i*2 + 1]
    max_state = moves[i*2 + 1]
#    next_legal_state(state, max_state)

def writeout_next_file(state):
    y = -2
    for x in range(p1_mancala+1, p2_mancala):
        nfile.write(str(state[y]) + ' ')
        y -= 1
    nfile.write('\n')
    for x in range(p1_mancala):
        nfile.write(str(state[x]) + ' ')
    nfile.write('\n')
    nfile.write(str(state[p2_mancala]) + '\n')
    nfile.write(str(state[p1_mancala]) + '\n')
    
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

def terminal_case(state, depth, p_type, continued):
    print 'in terminal_case'
    print state, depth,p_type, continued
    if depth == cutoff_depth:
        if continued:
            return False
        else:
#            wfile.write('')
            return True
    elif depth < cutoff_depth:
        print 'returning false from terminal'
        return False
    print 'returning true from terminal'
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

def write_out(player, pit, depth, value):
    player_char = 'B' if player == 1 else 'A'
    if value == float('inf'):
        wfile.write(player_char+str(pit)+','+str(depth)+',Infinity\n')
    elif value == float('-inf'):
        wfile.write(player_char+str(pit)+','+str(depth)+',-Infinity\n')
    else:
        wfile.write(player_char+str(pit)+','+str(depth)+','+str(value)+'\n')

def write_out_alphabeta(player, pit, depth, value, alpha, beta):
    player_char = 'B' if player == 1 else 'A'
    if player == 'root':
        player_char = 'root'
        pit = ''
    if alpha == float('inf'):
        alpha = 'Infinity'
    elif alpha == float('-inf'):
        alpha = '-Infinity'
    if beta == float('inf'):
        beta = 'Infinity'
    elif beta == float('-inf'):
        beta = '-Infinity'
    if value == float('inf'):
        wfile.write(player_char+str(pit)+','+str(depth)+',Infinity,'+str(alpha)+','+str(beta)+'\n')
    elif value == float('-inf'):
        wfile.write(player_char+str(pit)+','+str(depth)+',-Infinity,'+str(alpha)+','+str(beta)+'\n')
    else:
        wfile.write(player_char+str(pit)+','+str(depth)+','+str(value)+','+str(alpha)+','+str(beta)+'\n')
                
def minimax_max(state, depth, pit, player, parent_continues):
    global path
    print 'in max and state = ', state
    my_values = {}
    passed_player = player
    player_char = 'B' if player == 1 else 'A'
    next_moves = actions(state, 'max')    
    print player,player_char,pit, depth, next_moves
    if terminal_case(state, depth, 'max', parent_continues):
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
        print 'leaf in max', leaf_value
        write_out(player, pit, depth, leaf_value)
#        my_values['value'] = leaf_value
#        my_values['player'] = player
#        my_values['move'] = pit
#        path.append(my_values)
        return leaf_value
    value = float('-inf')
    my_values['value'] = value
    write_out(player, pit, depth, value)    
    if parent_continues:
        print 'parent_continues is true.', parent_continues
        child_depth = depth
    else:
        child_depth = depth + 1
        player = 1 if player == 2 else 2
    for index, s in enumerate(next_moves):
        if s:
            continue_flag = continue_move(state, index, 'max' if player == my_player else 'min')
            if depth == cutoff_depth and continue_flag:
                print 'in here',value, s, child_depth, index+2, player
                temp = value
                value = max(value, minimax_max(s, child_depth, index+2, player, True))
                if temp != value:
                    my_values['value'] = value
                    my_values['player'] = player
                    my_values['move'] = index+2
            elif continue_flag:
                print 'in here too',value, s, depth, index+2, player
                temp = value
                value = max(value, minimax_max(s, child_depth, index+2, player, True))
                if temp != value:
                    my_values['value'] = value
                    my_values['player'] = player
                    my_values['move'] = index+2
            else:
                print 'doing min.',value, s, child_depth, index+2, player
                temp = value
                value = max(value, minimax_min(s, child_depth, index+2, player, False))
                if temp != value:
                    my_values['value'] = value
                    my_values['player'] = player
                    my_values['move'] = index+2
            write_out(passed_player, pit, depth, value)                    
    path.append(my_values)
    return value

def minimax_min(state, depth, pit, player, parent_continues):
    global path
    print 'in min and state = ', state
    my_values = {}
    player_char = 'B' if player == 1 else 'A'
    passed_player = player
    next_moves = actions(state, 'min')
    print player,player_char, depth,pit, next_moves
    print 'parent continues = ', parent_continues
    if terminal_case(state, depth, 'min', parent_continues):
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
        write_out(player, pit, depth, leaf_value)
#        my_values['value'] = leaf_value
#        my_values['player'] = player
#        my_values['move'] = pit
#        path.append(my_values)
        print ('leaf in min')
        return leaf_value
    value = float('inf')
    my_values['value'] = value
    write_out(player, pit, depth, value)    
    if parent_continues:
        print 'parent_continues is true.', parent_continues
        child_depth = depth
    else:
        child_depth = depth + 1
        player = 1 if player == 2 else 2
    for index, s in enumerate(next_moves):
        if s:
            continue_flag = continue_move(state, index, 'max' if player == my_player else 'min')
            if depth == cutoff_depth and continue_flag:
                print 'in here',value, s, child_depth, index+2, player
                temp = value
                value = min(value, minimax_min(s, child_depth, index+2, player, True))
                if temp != value:
                    my_values['value'] = value
                    my_values['player'] = player
                    my_values['move'] = index+2
            elif continue_flag:
                print 'in here too',value, s, depth, index+2, player
                temp = value
                value = min(value, minimax_min(s, child_depth, index+2, player, True))
                if temp != value:
                    my_values['value'] = value
                    my_values['player'] = player
                    my_values['move'] = index+2
            else:
                print 'doing min.',value, s, child_depth, index+2, player
                temp = value
                value = min(value, minimax_max(s, child_depth, index+2, player, False))
                if temp != value:
                    my_values['value'] = value
                    my_values['player'] = player
                    my_values['move'] = index+2
            write_out(passed_player, pit, depth, value)                    
    path.append(my_values)
    return value

def evaluate(state):
    if my_player == 1:
        return state[p1_mancala] - state[p2_mancala]
    else:
        return state[p2_mancala] - state[p1_mancala]
    
def continue_move(parent, index, p_type):
    length = p2_mancala + 1    
    if p_type == 'max':
        if my_player == 1:
            z = 1
            pos = 0
            for x in range(parent[index]):
                if ((index+x+z)%(length)) == p2_mancala:
                    z += 1
                pos = ((index+x+z)%(length))
            if pos == p1_mancala:
                return True
                print 'p1_mancalad.'
            return False
            print pos
        else:
            z = 1
            pos = 0
            print p2_mancala-index-1
            for x in range(parent[p2_mancala-index-1]):
                if ((p2_mancala-index+x+z-1)%(length)) == p1_mancala:
                    z += 1
                pos = ((p2_mancala-index+x+z-1)%(length))
            if pos == p2_mancala:
                return True
                print 'p2_mancalad.'
            return False
            print pos
    elif p_type == 'min':
        if my_player == 2:
            z = 1
            pos = 0
            for x in range(parent[index]):
                if ((index+x+z)%(length)) == p2_mancala:
                    z += 1
                pos = ((index+x+z)%(length))
            if pos == p1_mancala:
                return True
                print 'p1_mancalad.'
            return False
            print pos
        else:
            z = 1
            pos = 0
            print p2_mancala-index-1
            for x in range(parent[p2_mancala-index-1]):
                if ((p2_mancala-index+x+z-1)%(length)) == p1_mancala:
                    z += 1
                pos = ((p2_mancala-index+x+z-1)%(length))
            if pos == p2_mancala:
                return True
                print 'p2_mancalad.'
            return False
            print pos
    
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
                                temp[p1_mancala] += (temp[-((x+y+z)%(length))-2] + 1)
                                temp[-((x+y+z)%(length))-2] = 0
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
                                temp[p2_mancala] += (temp[length-((x+y+z)%(length))-2] + 1)
                                temp[length-((x+y+z)%(length))-2] = 0
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
                                temp[p1_mancala] += (temp[-((x+y+z)%(length))-2] + 1)
                                temp[-((x+y+z)%(length))-2] = 0
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
                                temp[p2_mancala] += (temp[length-((x+y+z)%(length))-2] + 1)
                                temp[length-((x+y+z)%(length))-2] = 0
                            else:
                                temp[(x+y+z)%(length)] += 1
                        else:
                            temp[(x+y+z)%(length)] += 1
                    action_set.append(temp)
                else:
                    action_set.append([])
            action_set.reverse()
    return action_set

nfile = open('next_state.txt', 'w')
wfile = open('output.txt', 'w')
rfile = 'input.txt' #sys.argv[2]
with open(rfile) as inputFile:
    task = int(inputFile.readline().strip())
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
path = []

myChar = 'B'
oppChar = 'A'
opp_player = 2

if my_player == 2:
    myChar = 'A'
    oppChar = 'B'
    opp_player = 1

print state
print 'my player:', my_player

if task == 1:
    wfile.write('Node,Depth,Value\n')
    cutoff_depth = 1
    minimax(state)
elif task == 2:
    wfile.write('Node,Depth,Value\n')
    minimax(state)
elif task == 3:
    wfile.write('Node,Depth,Value,Alpha,Beta\n')
    alphabeta(state)
    
wfile.close()
nfile.close()









