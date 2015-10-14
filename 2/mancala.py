def minimax(state):
    moves = []
    next_moves = actions(state, 'max')
    print next_moves
    for index, s in enumerate(next_moves):
        if continue_move(state, s, 'max'):
            print 'in here'
            temp = minimax_max(s, 1)
        else:
            temp = minimax_min(s, 1)
        moves.append(temp)
        moves.append(s)
        print moves
    print moves

def minimax_max(state, depth):
    if depth == cutoff_depth:
        print 'max end'
        return evaluate(state, 'max')
    value = float('-inf')
    next_moves = actions(state, 'max')
    for s in next_moves:
        if continue_move(state, s, 'max'):
            print 'in the max continue'
            value = max(value, minimax_max(s, depth + 1))
        else:
            print 'in the max else'            
            value = max(value, minimax_min(s, depth + 1))
    return value

def minimax_min(state, depth):
    if depth == cutoff_depth:
        print 'min end'
        return evaluate(state, 'min')
    value = float('inf')
    next_moves = actions(state, 'min')
    print state
    for s in next_moves:
        if continue_move(state, s, 'min'):
            print 'in the min continue'            
            value = min(value, minimax_min(s, depth + 1))
        else:
            print 'in the min else.'            
            value = min(value, minimax_max(s, depth + 1))
    return value

def evaluate(state, p_type):
    if my_player == 1:
        return state[p1_mancala] - state[p2_mancala]
    elif my_player == 2:
        return state[p2_mancala] - state[p1_mancala]
    
def continue_move(parent, child, p_type):
    if p_type == 'max':
        if my_player == 1:
            print 'it is max 1'
            if ((child[p1_mancala] - parent[p1_mancala]) - (child[p1_mancala+1] - parent[p1_mancala+1])) == 1:
                print 'it is true'
                return True
            print 'it is false'
            return False
        elif my_player == 2:
            print 'it is max 2'
            if ((child[p2_mancala] - parent[p2_mancala]) - (child[0] - parent[0])) == 1:
                print 'it is true'
                return True
            print 'it is false'
            return False
    elif p_type == 'min':
        if my_player == 1:
            print 'it is min 1'            
            if ((child[p2_mancala] - parent[p2_mancala]) - (child[0] - parent[0])) == 1:
                print 'it is true'
                return True
                print 'it is false'
            return False
        elif my_player == 2:
            print 'it is min 2'            
            if ((child[p1_mancala] - parent[p1_mancala]) - (child[p1_mancala+1] - parent[p1_mancala+1])) == 1:
                print 'it is true'
                return True
                print 'it is false'
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
                            temp[(x+y+z)%(length)] += 1
                        else:
                            temp[(x+y+z)%(length)] += 1
                    action_set.append(temp)

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
                            temp[(x+y+z)%(length)] += 1
                        else:
                            temp[(x+y+z)%(length)] += 1
                    action_set.append(temp)
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
                            temp[(x+y+z)%(length)] += 1
                        else:
                            temp[(x+y+z)%(length)] += 1
                    action_set.append(temp)

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
                            temp[(x+y+z)%(length)] += 1
                        else:
                            temp[(x+y+z)%(length)] += 1
                    action_set.append(temp)
            action_set.reverse()
                        
#        print action_set
    return action_set
    
file = 'input.txt' #sys.argv[2]
with open(file) as inputFile:
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
p2_inp.append(p2_mancala_inp)
p2 = [int(x) for x in p2_inp]

state = p1 + p2
p2_mancala = len(state) - 1

print state
#print p1_mancala
#print p2_mancala

#actions(state, 'max')
#print evaluate(state, 'min')

minimax(state)
