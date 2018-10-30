#A* algorithm implementation for solving 8 puzzle problem

import numpy as np
import warnings
import sys


warnings.simplefilter(action='ignore', category=DeprecationWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

#global variables
global_node_counter=0
state_rep=[]
open_fringe=[]
closed_fringe=[]
goal_state=[]
initial_state=[]
goal_reached = False
current_heuristic = 0

#module to get input from user and load its state
def get_input():
    global global_node_counter, goal_state, initial_state, current_heuristic, closed_fringe
    if initial_state == []:
        print('Enter initial state: ')
        print('\n(One row at a time,with each element separated by a space)')
        initial_state = np.zeros((3,3))
        for i in range(3):
            initial_state[i] = input().split(' ')

        print('Enter goal state: ')
        print('\n(One row at a time,with each element separated by a space)')
        goal_state = np.zeros((3,3))
        for i in range(3):
            goal_state[i] = input().split(' ')
    
    #adding node in closed fringe
    closed_fringe.append({'id': global_node_counter, 'data': initial_state})
    global_node_counter += 1
    goal_cost = 0
    
    #toggle implementation for heuristic selected
    if current_heuristic == 1:
        heuristic_cost = no_of_misplaced_tiles(initial_state, goal_state)
    else:
        heuristic_cost = manhattan_distance(initial_state, goal_state)
    total_cost = goal_cost + heuristic_cost
    
    #adding node's data in state_represntation list
    state_rep.append({'id': 0,
                      'goal_cost': goal_cost,
                      'heuristic_cost': heuristic_cost,
                      'total_cost': total_cost,
                      'parent':None,
                      'value':initial_state})
    return state_rep[0]

#heuristic 1: number of misplaced tiles
def no_of_misplaced_tiles(node1, node2):
    misplaced_tiles=0
    for i in range(3):
        for j in range(3):
            if node1[i][j] != node2[i][j]:
                misplaced_tiles += 1
    return misplaced_tiles
    
#heuristic 2: manhattan distance
def manhattan_distance(node1, node2):
    sum = 0
    for i in range(3):
        for j in range(3):
            if node1[i][j] != node2[i][j]:
                num = node2[i][j]
                arr = []
                arr.append(i)
                arr.append(j)
                initarr = (locate_element(node1, num))
                arr = arr+initarr
                sum =sum + (find_distance(arr))
                
    return sum  

#helper module for finding distance in manhattan heuristic
def find_distance(arr):
    i = 0
    sum = 0
    while i <= 1:
        init = arr[i]
        goal = arr[i+2]
        if(init > goal):
            diff = (init - goal)
            sum = sum + diff
        else:
            diff = (goal - init)
            sum = sum + diff
                
        i=i+1
    return sum

#helper module for locating correct 
#position of element ingoal state                
def locate_element(node1, num):
    index = []
    for i in range(3):
        for j in range(3):
            if(node1[i][j] == num):
                index.append(i)
                index.append(j)
    return(index)
    
#module for expanding children nodes
def expand_node(node):
    zero_loc = np.where(node.get('value') == 0)
    i = zero_loc[0]
    j = zero_loc[1]
    children_nodes = []
    valid_children = []
    if 0<= (j-1) <= 2:
        child = node.get('value').copy()
        child[i,j], child[i,j-1] = child[i,j-1], child[i,j]
        children_nodes.append(child)
        
    if 0<= (j+1) <= 2:
        child = node.get('value').copy()
        child[i,j], child[i,j+1] = child[i,j+1], child[i,j]
        children_nodes.append(child)
        
    if 0<= (i-1) <= 2:
        child = node.get('value').copy()
        child[i,j], child[i-1,j] = child[i-1,j], child[i,j]
        children_nodes.append(child)
        
    if 0<= (i+1) <= 2:
        child = node.get('value').copy()
        child[i,j], child[i+1,j] = child[i+1,j], child[i,j]
        children_nodes.append(child)
        
    #removing child_nodes same as parent's parent node
    valid_children =  [ child for child in children_nodes 
                 if ( not (np.array_equal(child, node.get('parent'))))]
    
    update_state_representation(valid_children, node)

#module for storing node's data in state_represntation list
def update_state_representation(child_nodes, parent_node):
    global global_node_counter,open_fringe, current_heuristic
    for child in child_nodes:
        
        goal_cost = parent_node.get('goal_cost') + 1
        
        #toggle implementation for heuristic selected
        if current_heuristic == 1:
            heuristic_cost = no_of_misplaced_tiles(child, goal_state)
        else:
            heuristic_cost = manhattan_distance(child, goal_state)
            
        total_cost = goal_cost + heuristic_cost

        #removing duplicate nodes
        if state_rep != [] and open_fringe != []:
            for i in range(len(open_fringe)):
                if 0 == no_of_misplaced_tiles(open_fringe[i]['data'], child):
                    for j in range(len(state_rep)):
                        if state_rep[j]['id'] == open_fringe[i]['id']: 
                            if state_rep[j]['total_cost'] > total_cost:
                                del open_fringe[i]
                                del state_rep[j]
                                
                                #adding node in open fringe
                                generate_fringe_data(global_node_counter, child, goal_cost, heuristic_cost, total_cost, parent_node)

                            break
                        else:
                            #adding node in open fringe
                            generate_fringe_data(global_node_counter, child, goal_cost, heuristic_cost, total_cost, parent_node)

                            break
                    break
                else:
                    #adding node in open fringe
                    generate_fringe_data(global_node_counter, child, goal_cost, heuristic_cost, total_cost, parent_node)

                    break                      
        else:
            generate_fringe_data(global_node_counter, child, goal_cost, heuristic_cost, total_cost, parent_node)

        global_node_counter += 1

        if global_node_counter > 7000:
           print('Solution exceeds maximum node limit')
           sys.exit()

#module for appending fringe and state data 
def generate_fringe_data(global_node_counter, child, goal_cost, heuristic_cost, total_cost, parent_node):

    global open_fringe, state_rep

    open_fringe.append({'id': global_node_counter, 'data': child})
    state_rep.append({'id': global_node_counter,
                        'goal_cost': goal_cost,
                        'heuristic_cost': heuristic_cost,
                        'total_cost': total_cost,
                        'parent':parent_node,
                        'value':child})

#module for evaluating next best node 
def evaluate_next_choice():
    global open_fringe, closed_fringe
    
    #loading first node's value by default for comparison later
    best_node = [x for x in state_rep if x.get('id') == open_fringe[0].get('id')]
    best_node = best_node[0]    
    lowest_total_cost = best_node.get('total_cost')
    delete_node = open_fringe[0]
    
    for node_data in open_fringe:
        node = [x for x in state_rep if x.get('id') == node_data.get('id')]
        if lowest_total_cost > node[0].get('total_cost'):
            lowest_total_cost = node[0].get('total_cost')
            best_node = node[0]
            delete_node = node_data
    #removing the selected node from open fringe
    for i in range(len(open_fringe)):
        if open_fringe[i]['id'] == delete_node.get('id'):
            del open_fringe[i]
            break
    #adding the selected node to closed fringe
    closed_fringe.append({'id': best_node.get('id'), 'data': best_node.get('value')})
    return best_node

#module for displaying result
def generate_result(result_node):
    global open_fringe, closed_fringe, current_heuristic
    best_path = []
    total_cost = result_node.get('total_cost')
    
    #traversing up the tree to acquire parent node's in best path list
    while(result_node.get('id') != 0):
        best_path.append({'id': result_node.get('id'), 'value': result_node.get('value')})
        result_node = result_node.get('parent')
    best_path.append({'id': result_node.get('id'), 'value': result_node.get('value')})
            
    print('\nSolution for heuristic :::', current_heuristic)
    for node in reversed(best_path):
        print('\n Node ID: ',node.get('id'),'\n',node.get('value'))
        
    print('Total Path Cost: ', total_cost)
    print('Nodes left for expanding: ',len(open_fringe))
    print('Nodes generated: ', len(closed_fringe))

#module for initializing all global variables
def refresh_global_values():
    global global_node_counter, state_rep, open_fringe, closed_fringe
    global goal_reached, current_heuristic
    
    
    global_node_counter=0
    state_rep=[]
    open_fringe=[]
    closed_fringe=[]
    goal_reached = False
    current_heuristic = 0

#module for calculating output based on 'number of missing tiles' heuristic
def calculate_heuristic_1():
    global open_fringe, goal_reached, current_heuristic
    current_heuristic = 1
    node = get_input()
    expand_node(node)
    if 0 == node.get('heuristic_cost') :
        goal_reached = True
    while(goal_reached is not True and open_fringe != []):
        
        node=evaluate_next_choice()
        if 0 == node.get('heuristic_cost') :
            goal_reached = True
            break
        expand_node(node)
    
    if goal_reached is not True:
        print('No solution found.')
        
    else:
        generate_result(node) 

#module for calculating output based on 'manhattan distance' heuristic
def calculate_heuristic_2():
    global open_fringe, goal_reached, current_heuristic
    refresh_global_values()
    current_heuristic = 2
    node = get_input()
    expand_node(node)
    if 0 == node.get('heuristic_cost') :
        goal_reached = True
    while(goal_reached is not True and open_fringe != []):
        
        node=evaluate_next_choice()
        if 0 == node.get('heuristic_cost') :
            goal_reached = True
            break
        expand_node(node)
    
    if goal_reached is not True:
        print('No solution found.')
        
    else:
        generate_result(node) 

#starting point of execution 
if __name__ == '__main__':
    calculate_heuristic_1()
    calculate_heuristic_2()
