import numpy as np
import random
from past.builtins import xrange

number_of_queens = 0
prevcalcmin = 0
heuristic = list(0 for i in xrange(0,number_of_queens))
bestpositions = list(0 for i in xrange(0,number_of_queens))
successcount = 0
failcount = 0
conflict = 0
successsteps = 0
failsteps = 0
steps = 0
number_of_trials = 0
to_be_displayed = 0
counter = 0

#Function to initialize the variables
def initialize():
    global prevcalcmin, heuristic, bestpositions, successcount, counter, failcount,conflict, successsteps, failsteps, steps, number_of_trials, number_of_queens 
    
    prevcalcmin = 0
    heuristic = list(0 for i in xrange(0,number_of_queens))
    bestpositions = list(0 for i in xrange(0,number_of_queens))
    successcount = 0
    failcount = 0
    conflict = 0
    successsteps = 0
    failsteps = 0
    steps = 0
    number_of_trials = 0
    counter = 0
    
#Generates board of randomly placed queens
def createboard():
    i = 0
    board = []
    while( i < number_of_queens):
            randmint = random.randint(0, (number_of_queens - 1))
            if(randmint not in board):
                board.append(randmint)
                i+=1
    return board
    
#Main function for running iterations limited Steepest Ascent and Sideways approach
def steepest_sideways():    
    global conflict, successcount, failcount, prevcalcmin, counter
    approaches = ["steepestascent", "sideways"]
    for approach in approaches:
        initialize()
        if(approach == "steepestascent"):
            print("\033[1mStarting with The Steepest Ascent Approach: \033[0m")
        else:
            print("\033[1mStarting with The Side-ways Move Approach: \033[0m")
            print("counter: ", counter)
        while(counter != 100):
            i=0
            j=0
            board = []
            board = createboard()
            conflict = find_heuristic(board)
            prevcalcmin = conflict
            if(conflict == 0):
                successcount += 1
            else:
                if(approach == "steepestascent"):
                    board = steepestascentcheckboard(board)
                elif(approach == "sideways"):
                    board = sidewayscheckboard(board)
            counter += 1
        display_result()

        
#Main function to run the different approaches of Random restart
def random_restart():
    counter = 0
    global conflict, successcount, failcount, overalmin, successsteps, failsteps
    approaches = ["normal", "withoutsideways", "with sideways"]
    for approach in approaches:
        initialize()
        if(approach == "normal"):
            print("\033[1mStarting with The Normal Random Restart Approach: \033[0m ")
            result_board = randomstartnormal()
        elif(approach == "withoutsideways"):
            print("\033[1mStarting with The Random Restart Without Sideways Approach: \033[0m")
            result_board = restart_wo_sideways()
        else:
            print("\033[1mStarting with The Random Restart With Sideways Approach: \033[0m")
            result_board = restart_sideways()
        display_restart_result(result_board)
    
#Approach 1: of Random Restart
def randomstartnormal():
    counter = 0
    global conflict, number_of_trials
    board = createboard()
    conflict = find_heuristic(board)
    while(conflict != 0):
        number_of_trials += 1 
        counter += 1 
        board = createboard()
        conflict = find_heuristic(board)
    return board

#Approach 2: of Random Restart (Without Sideways)
def restart_wo_sideways():
    global conflict, number_of_trials
    board = createboard()
    conflict = find_heuristic(board)
    while(conflict != 0):
        number_of_trials += 1 
        board = steepestascentcheckboard(board)
        conflict = find_heuristic(board)
        if(conflict == 0):
            break           
        else:
            board = createboard()
            conflict = find_heuristic(board)
    return board

#Approach 3: of Random Restart (With Sideways)
def restart_sideways():
    global conflict, number_of_trials
    board = createboard()
    conflict = find_heuristic(board)
    while(conflict != 0):
        number_of_trials += 1 
        board = sidewayscheckboard(board)
        conflict = find_heuristic(board)
        if(conflict == 0):
            break           
        else:
            board = createboard()
            conflict = find_heuristic(board)
    return board
    

#Function to find the heuristics
def find_heuristic(check_board):
    conflict = 0
    global number_of_queens
    for i in range(number_of_queens):
        for j in range(i+1,number_of_queens):
            threat = abs(j-i)
            diagthreat =abs(check_board[i] - check_board[j])
            if(check_board[i] == check_board[j] or threat == diagthreat):
                conflict += 1
    return conflict

#Function to find the successors of a give board
def find_Successor(board):
    global heuristic, bestpositions
    for i in range(number_of_queens):
        check_board = board[:]
        minheuristic = find_heuristic(check_board)
        for j in range(number_of_queens):
            check_board[i] = j
            threat = find_heuristic(check_board)
            if(minheuristic >= threat):
                minheuristic = threat
                bestpositions[i] = j
        heuristic[i] = minheuristic

#Function for Steepest Ascent Approach Hill Climbing
def steepestascentcheckboard(board):
    i=0
    global conflict, heuristic, prevcalcmin, bestpositions, counter, successcount, failcount, successsteps, failsteps, number_of_queens
    steps = 0
#     if(counter < 3):
#         print(" Example #: ",counter)
#         display_board(board,conflict)
    while(conflict != 0):
        steps += 1
        find_Successor(board)
        minheuristic = min(heuristic)
        if(minheuristic < prevcalcmin ):
            prevcalcmin = minheuristic
            if(minheuristic == 0):
                mincolumnvaluelist = [i for i, val in enumerate(heuristic) if (val == minheuristic)]
                mincolumnvalue = random.choice(mincolumnvaluelist)
                board[mincolumnvalue] = bestpositions[mincolumnvalue]
                conflict = find_heuristic(board)
                successcount += 1
                successsteps += steps
#                 if(counter < 3):
#                     display_board(board,conflict)
#                     print("Success!!")
            else:
                listitem = [i for i, val in enumerate(heuristic) if (val == minheuristic)]
                selected_queen = random.choice(listitem)         
                board[selected_queen] = bestpositions[selected_queen]
                conflict = find_heuristic(board)
                if(counter < 3):
                    display_board(board,conflict)
        else:
            failcount += 1
            failsteps += steps
#             if(counter < 3):
#                 display_board(board,conflict)
#                 print("Failure Occured.")
            break
    return board

#Function for Sideways Hill Climbing
def sidewayscheckboard(board):
    keeptrack = 0
    steps = 0
    global conflict, heuristic, counter, prevcalcmin, bestpositions, successcount, failcount, successsteps, failsteps, number_of_queens
#     if(counter < 3):
#         print(" Example #: ",counter)
#         display_board(board,conflict)
    while(conflict != 0):
        steps += 1
        find_Successor(board)
        minheuristic = min(heuristic)
        if(minheuristic == prevcalcmin and keeptrack == 0):
            keeptrack = 0                   
        if(minheuristic < prevcalcmin or (minheuristic == prevcalcmin and keeptrack <= 100)):
            if(minheuristic < prevcalcmin):
                prevcalcmin = minheuristic
            else:
                keeptrack += 1
            if(minheuristic == 0):
                mincolumnvaluelist = [i for i, val in enumerate(heuristic) if (val == minheuristic)]
                mincolumnvalue = random.choice(mincolumnvaluelist)
                board[mincolumnvalue] = bestpositions[mincolumnvalue]
                conflict = find_heuristic(board)
                successcount += 1
                successsteps += steps
#                 if(counter < 3):
#                     display_board(board,conflict)
#                     print("Success!!\n")
            else:
                listitem = [i for i, val in enumerate(heuristic) if (val == minheuristic)]
                selected_queen = random.choice(listitem)     
                board[selected_queen] = bestpositions[selected_queen]
                conflict = find_heuristic(board)
#                 if(counter < 3):
#                     display_board(board,conflict)
        else:
            failcount += 1
            failsteps += steps
#             if(counter < 3):
#                 display_board(board,conflict)
#                 print("Failure Occured.\n")
            break
        
            
    return board

#Function to display the boards generated while running Steepest Ascent and Sideways Hill Climbing Approach
def display_board(board, conflict):
    for i in range(number_of_queens):
        print(board[i], end = " ")
    print("h(n): ", conflict)
        
#Function to display the result of Steepest Ascent and Sideways Hill Climbing Approach
def display_result():
    global successcount, failcount
    print("Successcount : ", successcount)
    print("Failcount: ", failcount)
    print("successsteps: ", successsteps)
    print("failsteps: ", failsteps)
    if (successcount > 0):
        print("Average Success-steps = ", int((successsteps/successcount)))
    print("Average Fail-steps = ", int((failsteps/failcount)))
    print("\n")

#Function to display the output of Random Restart
def display_restart_result(board):
    global number_of_trials
    print("Goal state found!!")
    for row in range(len(board)):
        line = ""
        for column in range(len(board)):
            if(board[row] == column):
                line += "Q "
            else:
                line += "_ "
        print(line)         
        print("\n") 
    print("Number of Trials : ", number_of_trials)
    print("\n")

    
#Main function 
if __name__ == '__main__':
    global number_of_queens
    number_of_queens = int(input("Enter the number of queens:"))
    print("\n")
    steepest_sideways()
    random_restart()
