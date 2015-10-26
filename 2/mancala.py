import operator
import sys

def alphabeta(state):
    moves = []
    paths = ''
    alpha = float('-inf')
    beta = float('inf')
    max_root = float('-inf')
    next_moves = actions(state, 'max')
    wfile.write('root'+',0,-Infinity,-Infinity,Infinity\n')    
    for index, s in enumerate(next_moves):
        if s:
            continue_flag = continue_move(state, index, 'max')
            if continue_flag:
                temp = alphabeta_max(s, 1, index+2, my_player, continue_flag, alpha, beta)
            else:
                temp = alphabeta_min(s, 1, index+2, my_player, continue_flag, alpha, beta)
            if temp['value'] > max_root:
                max_root = temp['value']
                paths = temp['path']
            if max_root >= beta:
                write_out_alphabeta('root', 0, 0, max_root, alpha, beta)
                break
            alpha = max(alpha, max_root)
            write_out_alphabeta('root', 0, 0, max_root, alpha, beta)
    paths.reverse()
    player = 0
    print_node = state
    for node in paths:
        if node['player'] != my_player:
            break
        children = actions(print_node, 'max')
        for index, s in enumerate(children):
            if s:
                if index+2 == node['move']:
                    print_node = s

    p1_coins = 0
    p2_coins = 0
    for x in range(p1_mancala):
        p1_coins += print_node[x]
    for x in range(p1_mancala+1, p2_mancala):
        p2_coins += print_node[x]

    if p1_coins == 0:
        print_node = endgame(print_node,  1)
    elif p2_coins == 0:
        print_node = endgame(print_node, 2)

    writeout_next_file(print_node)

def alphabeta_max(state, depth, pit, player, parent_continues, alpha, beta):
    subtree_path = []
    my_values = {}
    passed_player = player
    player_char = 'B' if player == 1 else 'A'
    next_moves = actions(state, 'max')

    coins = 0
    for x in range(p1_mancala):
        coins += state[x]
    if coins == 0:
        end_state = endgame(state,  1)
        leaf_value = evaluate(end_state)
        write_out_alphabeta(player, pit, depth, leaf_value, alpha, beta)
        my_values['player'] = player
        my_values['move'] = pit
        return {'value':leaf_value, 'path':[my_values]}
    
    coins = 0
    for x in range(p1_mancala+1, p2_mancala):
        coins += state[x]
    if coins == 0:
        end_state = endgame(state, 2)
        leaf_value = evaluate(end_state)
        write_out_alphabeta(player, pit, depth, leaf_value, alpha, beta)
        my_values['player'] = player
        my_values['move'] = pit
        return {'value':leaf_value, 'path':[my_values]}

    if terminal_case(state, depth, 'max', parent_continues):
        leaf_value = evaluate(state)
        write_out_alphabeta(player, pit, depth, leaf_value, alpha, beta)
        my_values['player'] = player
        my_values['move'] = pit
        return {'value':leaf_value, 'path':[my_values]}
    
    value = float('-inf')
    my_values['move'] = pit
    my_values['player'] = player
    ret_val = {}
    ret_val['path'] = []
    write_out_alphabeta(player, pit, depth, value, alpha, beta)
    if parent_continues:
        child_depth = depth
    else:
        child_depth = depth + 1
        player = 1 if player == 2 else 2
    for index, s in enumerate(next_moves):
        if s:
            continue_flag = continue_move(state, index, 'max' if player == my_player else 'min')
            temp = value
            if depth == cutoff_depth and continue_flag:
                ret_val = alphabeta_max(s, child_depth, index+2, player, True, alpha, beta)
                value = max(value, ret_val['value'])
            elif continue_flag:
                ret_val = alphabeta_max(s, child_depth, index+2, player, True, alpha, beta)
                value = max(value, ret_val['value'])
            else:
                ret_val = alphabeta_min(s, child_depth, index+2, player, False, alpha, beta)
                value = max(value, ret_val['value'])
            if temp < value:
                subtree_path = ret_val['path'][:]
            if value >= beta:
                write_out_alphabeta(passed_player, pit, depth, value, alpha, beta)
                subtree_path.append(my_values)
                return {'value':value, 'path':subtree_path}
            alpha = max(alpha, value)
            write_out_alphabeta(passed_player, pit, depth, value, alpha, beta)
    subtree_path.append(my_values)
    return {'value':value, 'path':subtree_path}

def alphabeta_min(state, depth, pit, player, parent_continues, alpha, beta):
    subtree_path = []
    my_values = {}
    player_char = 'B' if player == 1 else 'A'
    passed_player = player
    next_moves = actions(state, 'min')

    coins = 0
    for x in range(p1_mancala):
        coins += state[x]
    if coins == 0:
        end_state = endgame(state,  1)
        leaf_value = evaluate(end_state)
        write_out_alphabeta(player, pit, depth, leaf_value, alpha, beta)
        my_values['player'] = player
        my_values['move'] = pit
        return {'value':leaf_value, 'path':[my_values]}        
    
    coins = 0
    for x in range(p1_mancala+1, p2_mancala):
        coins += state[x]
    if coins == 0:
        end_state = endgame(state, 2)
        leaf_value = evaluate(end_state)
        write_out_alphabeta(player, pit, depth, leaf_value, alpha, beta)
        my_values['player'] = player
        my_values['move'] = pit
        return {'value':leaf_value, 'path':[my_values]}        

    if terminal_case(state, depth, 'min', parent_continues):
        leaf_value = evaluate(state)
        write_out_alphabeta(player, pit, depth, leaf_value, alpha, beta)
        my_values['player'] = player
        my_values['move'] = pit
        return {'value':leaf_value, 'path':[my_values]}        
    
    value = float('inf')
    ret_val = {}
    ret_val['path'] = []
    my_values['player'] = player
    my_values['move'] = pit
    write_out_alphabeta(player, pit, depth, value, alpha, beta)
    if parent_continues:
        child_depth = depth
    else:
        child_depth = depth + 1
        player = 1 if player == 2 else 2
    for index, s in enumerate(next_moves):
        if s:
            continue_flag = continue_move(state, index, 'max' if player == my_player else 'min')
            temp = value
            if depth == cutoff_depth and continue_flag:
                ret_val = alphabeta_min(s, child_depth, index+2, player, True, alpha, beta)
                value = min(value, ret_val['value'])
            elif continue_flag:
                ret_val = alphabeta_min(s, child_depth, index+2, player, True, alpha, beta)
                value = min(value, ret_val['value'])
            else:
                ret_val = alphabeta_max(s, child_depth, index+2, player, False, alpha, beta)
                value = min(value, ret_val['value'])
            if temp > value:
                subtree_path = ret_val['path'][:]
            if value <= alpha:
                write_out_alphabeta(passed_player, pit, depth, value, alpha, beta)
                subtree_path.append(my_values)
                return {'value':value, 'path':subtree_path}
            beta = min(beta, value)
            write_out_alphabeta(passed_player, pit, depth, value, alpha, beta)
    subtree_path.append(my_values)
    return {'value':value, 'path':subtree_path}

def minimax(state):
    moves = []
    paths = ''
    max_root = float('-inf')
    next_moves = actions(state, 'max')
    wfile.write('root'+',0,-Infinity\n')
    for index, s in enumerate(next_moves):
        if s:
            continue_flag = continue_move(state, index, 'max')
            if continue_flag:
                temp = minimax_max(s, 1, index+2, my_player, continue_flag)
            else:
                temp = minimax_min(s, 1, index+2, my_player, continue_flag)
            if temp['value'] > max_root:
                max_root = temp['value']
                paths = temp['path']
            wfile.write('root'+','+'0,'+str(max_root)+'\n')
    moves = paths
    moves.reverse()
    print_node = state
    for node in moves:
        if node['player'] != my_player:
            break
        children = actions(print_node, 'max')
        for index, s in enumerate(children):
            if s:
                if index+2 == node['move']:
                    print_node = s
                    
    p1_coins = 0
    p2_coins = 0
    for x in range(p1_mancala):
        p1_coins += print_node[x]
    for x in range(p1_mancala+1, p2_mancala):
        p2_coins += print_node[x]

    if p1_coins == 0:
        print_node = endgame(print_node,  1)
    elif p2_coins == 0:
        print_node = endgame(print_node, 2)

    writeout_next_file(print_node)

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

def terminal_case(state, depth, p_type, continued):
    if depth == cutoff_depth:
        if continued:
            return False
        else:
            return True
    elif depth < cutoff_depth:
        return False
    return True

def endgame(state, player):
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
    subtree_path = []
    my_values = {}
    passed_player = player
    player_char = 'B' if player == 1 else 'A'
    next_moves = actions(state, 'max')    

    coins = 0
    for x in range(p1_mancala):
        coins += state[x]
    if coins == 0:
        end_state = endgame(state, 1)
        leaf_value = evaluate(end_state)
        write_out(player, pit, depth, leaf_value)
        my_values['player'] = player
        my_values['move'] = pit
        return {'value':leaf_value, 'path':[my_values]}
    
    coins = 0
    for x in range(p1_mancala+1, p2_mancala):
        coins += state[x]
    if coins == 0:
        end_state = endgame(state, 2)
        leaf_value = evaluate(end_state)
        write_out(player, pit, depth, leaf_value)
        my_values['player'] = player
        my_values['move'] = pit
        return {'value':leaf_value, 'path':[my_values]}
    
    if terminal_case(state, depth, 'max', parent_continues):
        leaf_value = evaluate(state)
        my_values['player'] = player
        my_values['move'] = pit
        write_out(player, pit, depth, leaf_value)
        return {'value':leaf_value, 'path':[my_values]}

    value = float('-inf')
    write_out(player, pit, depth, value)
    
    if parent_continues:
        child_depth = depth
    else:
        child_depth = depth + 1
        player = 1 if player == 2 else 2
    my_values['player'] = passed_player
    my_values['move'] = pit
    ret_val = {}
    ret_val['path'] = []
    for index, s in enumerate(next_moves):
        if s:
            continue_flag = continue_move(state, index, 'max' if player == my_player else 'min')
            temp = value
            if depth == cutoff_depth and continue_flag:
                ret_val = minimax_max(s, child_depth, index+2, player, True)
                value = max(value, ret_val['value'])
            elif continue_flag:
                ret_val = minimax_max(s, child_depth, index+2, player, True)
                value = max(value, ret_val['value'])
            else:
                ret_val = minimax_min(s, child_depth, index+2, player, False)
                value = max(value, ret_val['value'])
            if temp < value:
                    subtree_path = ret_val['path'][:]
            write_out(passed_player, pit, depth, value)
    subtree_path.append(my_values)
    return {'value':value, 'path':subtree_path}

def minimax_min(state, depth, pit, player, parent_continues):
    subtree_path = []
    my_values = {}
    player_char = 'B' if player == 1 else 'A'
    passed_player = player
    next_moves = actions(state, 'min')
    coins = 0
    for x in range(p1_mancala):
        coins += state[x]
    if coins == 0:
        end_state = endgame(state,  1)
        leaf_value = evaluate(end_state)
        my_values['player'] = player
        my_values['move'] = pit
        write_out(player, pit, depth, leaf_value)
        return {'value':leaf_value, 'path':[my_values]}        
    
    coins = 0
    for x in range(p1_mancala+1, p2_mancala):
        coins += state[x]
    if coins == 0:
        end_state = endgame(state, 2)
        leaf_value = evaluate(end_state)
        write_out(player, pit, depth, leaf_value)
        my_values['player'] = player
        my_values['move'] = pit
        return {'value':leaf_value, 'path':[my_values]}        

    if terminal_case(state, depth, 'min', parent_continues):
        leaf_value = evaluate(state)
        my_values['player'] = player
        my_values['move'] = pit
        write_out(player, pit, depth, leaf_value)
        return {'value':leaf_value, 'path':[my_values]}        
    
    value = float('inf')
    ret_val = {}
    ret_val['path'] = []
    write_out(player, pit, depth, value)
    if parent_continues:
        child_depth = depth
    else:
        child_depth = depth + 1
        player = 1 if player == 2 else 2
    my_values['player'] = passed_player
    my_values['move'] = pit
    for index, s in enumerate(next_moves):
        if s:
            continue_flag = continue_move(state, index, 'max' if player == my_player else 'min')
            temp = value
            if depth == cutoff_depth and continue_flag:
                ret_val = minimax_min(s, child_depth, index+2, player, True)
                value = min(value, ret_val['value'])
            elif continue_flag:
                ret_val = minimax_min(s, child_depth, index+2, player, True)
                value = min(value, ret_val['value'])
            else:
                ret_val = minimax_max(s, child_depth, index+2, player, False)
                value = min(value, ret_val['value'])
            if temp > value:
                subtree_path = ret_val['path'][:]
            write_out(passed_player, pit, depth, value)
    subtree_path.append(my_values)
    return {'value':value, 'path':subtree_path}

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
            return False
        else:
            z = 1
            pos = 0
            for x in range(parent[p2_mancala-index-1]):
                if ((p2_mancala-index+x+z-1)%(length)) == p1_mancala:
                    z += 1
                pos = ((p2_mancala-index+x+z-1)%(length))
            if pos == p2_mancala:
                return True
            return False
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
            return False
        else:
            z = 1
            pos = 0
            for x in range(parent[p2_mancala-index-1]):
                if ((p2_mancala-index+x+z-1)%(length)) == p1_mancala:
                    z += 1
                pos = ((p2_mancala-index+x+z-1)%(length))
            if pos == p2_mancala:
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
wfile = open('traverse_log.txt', 'w')
rfile = sys.argv[2]
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

myChar = 'B'
oppChar = 'A'
opp_player = 2

if my_player == 2:
    myChar = 'A'
    oppChar = 'B'
    opp_player = 1

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

