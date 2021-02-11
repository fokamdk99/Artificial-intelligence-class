import random
from stan import State
import copy

def minimax(actual_state, depth, max_move, original_depth):
    #list of values
    w = []
    
    if((actual_state.terminal) or depth == 0):
        actual_state.get_state_value()
        return actual_state.value

    U = actual_state.get_successors()
    
    for ind, u in enumerate(U):
        w.append(minimax(u, depth-1, not max_move, original_depth))

    for ind, val in enumerate(U):
        val.get_state_value()
    
    
    if max_move:
        value = max(w)
    else:
        value = min(w)
    
    if depth == original_depth:
        if max_move:
            indices = [i for i, x in enumerate(w) if x == max(w)]
        else:
            indices = [i for i, x in enumerate(w) if x == min(w)]
        
        if len(indices) > 1:
            index = random.choice(indices)
        else:
            index =  indices[0]
        return index
        
    else:
        return value
        