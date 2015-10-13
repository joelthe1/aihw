def minimax():
    return

def minimax_max(state, depth):
    if depth == cutoff_depth:
        return eval(state)
    value = float('-inf')
    

def actions(state, p_type):
    global my_player
    action_set = []
    if p_type == 'max':
        if my_player == 1:
            for x in range(p1_mancala):
                if state[x] != 0:
                    temp = state[:]
                    coins = temp[x]
                    temp[x] = 0
                    for y in range(coins):
                        if x+y+1 >= p2_mancala:
                            temp[p2_mancala - (x+y+1)] += 1
                        else:
                            temp[x+y+1] += 1
                    action_set.append(temp)

        elif my_player == 2:
            for x in range(p1_mancala + 1, p2_mancala):
                if state[x] != 0:
                    temp = state[:]
                    coins = temp[x]
                    temp[x] = 0
                    z = 1
                    for y in range(coins):
                        if x+y+z > p2_mancala:
                            if (x+y+z-p2_mancala-1) == p1_mancala:
                                print 'in here'
                                z += 1
                                temp[x+y+z-p2_mancala-1] += 1
                            else:
                                temp[x+y+z-p2_mancala-1] += 1                                
                        else:
                            temp[x+y+z] += 1
                    action_set.append(temp)
    print action_set
            
            
    
def eval(state):
    global p1_mancala, p2_mancala, my_player
    if my_player == 1:
        return state[p1_mancala] - state[p2_mancala]
    else:
        return state[p2_mancala] - state[p1_mancala]
    

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
print p1_mancala
print p2_mancala

actions(state, 'max')
