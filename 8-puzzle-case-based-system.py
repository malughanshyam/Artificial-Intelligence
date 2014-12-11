# File Description      : 8-Puzzle Solver using Case Base System
# Author                  : Ghanshyam Malu

'''
Detailed Description : 
Program to solve 8-puzzle using Case Base approach:  
A* with Manhattan Distance Heuristic has been used for this. 
The similarity score / threshold is based on Manhattan Distance as well. 
Note : Threshold can be set to -1 to make the program run without leveraging Case Base
'''

import time, sys, os.path , math,random                     # Importing the modules used in the program

def makeNode(state, parent=None, depth=0, pathCost=0):
    '''Function to Create a Node'''
    return [state, parent, depth, pathCost]                 # Returns a Node with the 4 fields

def goalCheck(state,goalState):  
    '''Function to Test if Goal is found'''
    for i in range(0,3):
        for j in range(0,3):
            if state[0][i][j] != goalState[i][j]:           # Cross checks each Tile of the given State with the Goal State defined
                return False            
    return True
           
def displaySolutionPath(buildpath):
    '''Function to Display the found solution'''
    print "Solution Path"
    print "-"*20     
    for i in range(len(buildpath)):
        print_board(buildpath[i])       
           
def getSolutionPath(numRuns, queue):
    '''Function to Get the found solution'''
    recursive_path_build(queue)                             # Generate a list of the nodes for the solution based on the parents of each node
    buildpath.reverse()
    return buildpath

def recursive_path_build (queue):
    '''Recursive function to Build the path backwards from the Goal Node'''
    buildpath.append(queue[0])                              # Append the parent nodes of each node into the buildpath list
    if queue[1] == 0 :
        return    
    recursive_path_build(queue[1])  

def swap_tiles(oldstate, old_row, old_col, new_row, new_col):
    '''Function to Swap the tiles in a given Board based on Current x,y coordinates and Target x,y coordinates'''
    newstate = [x[:] for x in oldstate]                     # Copying 2d list to avoid modifying the original list during swapping
    temp= newstate[old_row][old_col]
    newstate[old_row][old_col]=newstate[new_row][new_col]
    newstate[new_row][new_col]=temp
    return newstate
       
def expandProcedure(frontier, remainingQueue, searchType):
    '''Function to Expand the First/Frontier Node and insert into the Remaining Queue'''
                                                            # Initializing new variables
    parentNode = frontier
    depth = frontier[2]
    pathCost=frontier[3] 
    newdepth = depth+1
    newpathCost = pathCost
    generatedNodes = []                                     # List to store the Generated Nodes

    for i in range(3):
        for j in range(3):
            if frontier[0][i][j] == 'blank':                # Finding the position of the Blank Tile
                blank_pos_row = i
                blank_pos_col = j

    #Generate the new possible nodes by moving blank tile in feasible directions 
    if blank_pos_row > 0 :
        new_generated_pos = swap_tiles(frontier[0],blank_pos_row,blank_pos_col,blank_pos_row - 1, blank_pos_col)
        if new_generated_pos not in visited:
            generatedNodes.append([new_generated_pos,parentNode,newdepth,newpathCost])

    if blank_pos_col > 0:
        new_generated_pos = swap_tiles(frontier[0],blank_pos_row,blank_pos_col,blank_pos_row, blank_pos_col - 1)
        if new_generated_pos not in visited:
            generatedNodes.append([new_generated_pos,parentNode,newdepth,newpathCost])

    if blank_pos_row < 2:
        new_generated_pos = swap_tiles(frontier[0],blank_pos_row,blank_pos_col,blank_pos_row + 1, blank_pos_col)
        if new_generated_pos not in visited:
            generatedNodes.append([new_generated_pos,parentNode,newdepth,newpathCost])

    if blank_pos_col < 2:
        new_generated_pos = swap_tiles(frontier[0],blank_pos_row,blank_pos_col,blank_pos_row, blank_pos_col + 1)
        if new_generated_pos not in visited:
            generatedNodes.append([new_generated_pos,parentNode,newdepth,newpathCost])
    
    if searchType == 'HEUR1' :
        remainingQueue=remainingQueue+generatedNodes
    elif searchType == 'HEUR2':
        remainingQueue=generatedNodes+remainingQueue         
    # The sorting of the RemainingQueue would be done by the Respective Heuristic Sorter functions                     
    return remainingQueue
    
def misplaced_tile_counter(state,goalState):
    '''Function to count the Number of misplaced tiles compared to the Goal State'''
    misplaced_tile_count = 0                                # Misplaced Tile Count tracker

    for i in range(0,3):
        for j in range(0,3):
            if state[i][j] != goalState[i][j]:
                misplaced_tile_count+=1
                
    if misplaced_tile_count !=0:                            # Condition !=0 to avoid -1 when All the tiles are properly placed 
        misplaced_tile_count-= 1                            # Ignoring the Blank Space
        
    return misplaced_tile_count
  
def find_position_tile(tile,board):
    ''' Function to find the coordinates of a tile on the given board'''
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] == str(tile):                    # Find the position of a given Tile on the Board
                return (i,j)  
    return (-1,-1)  

def manhattan_dist_finder(state,goalState):
    '''Function to Find the Manhattan Distance of the Tiles for a given board'''
#     global goalState         
    manhattan_dist = 0
    count = 0
    for i in range(0,3):
        for j in range(0,3):

            if state[i][j] != goalState[i][j]:
                k,l=find_position_tile(goalState[i][j],state)
                distance = abs(k-i)+abs(l-j)                # Manhattan Distance = Sum of all tiles (abs(x-xi) + abs(y-yi))
                if state[i][j] != 'blank':
                    manhattan_dist+=distance                   
            count+=1
    return manhattan_dist

def heuristic_sorter1(queue,goalState):
    '''Function for Misplaced Tiles Count Heuristic''' 
    for item in queue :
        state = item[0]
        misplaced_tile_count = misplaced_tile_counter(state,goalState)
        item[3]= misplaced_tile_count                       # Changing the Path Cost of Each Item to f(n) = h(n)                   
    queue.sort(key=lambda x: x[3])                          # Sorting the list based on Heuristic Value f(n) i.e Misplaced Tiles Count
    return queue    

def heuristic_sorter2(queue,goalState):
    '''Function for Manhattan Distance Heuristic'''     
    for item in queue :
        state = item[0]
        manhattan_dist = manhattan_dist_finder(state,goalState)
        item[3]= manhattan_dist                             # Changing the Path Cost of Each Item to f(n) = h(n)                   
    queue.sort(key=lambda x: x[3])                          # Sorting the list based on Heuristic Value f(n) i.e Manhattan Distance
    return queue
 
def expandProcedureAstar(frontier,goalState):
    '''Function to Expand the First/Frontier Node and insert into the Remaining Queue'''
                                                            
    parentNode = frontier                                   # Initializing new variables
    depth = frontier[2]
    newdepth = depth+1
    generatedNodes = []                                     # List to store the Generated Nodes
    pathCostParent = frontier[3]

    for i in range(3):
        for j in range(3):
            if frontier[0][i][j] == 'blank':                # Finding the position of the Blank Tile
                blank_pos_row = i
                blank_pos_col = j

    #Generate the new possible nodes by moving blank tile in feasible directions 
    if blank_pos_row > 0 :
        new_generated_pos = swap_tiles(frontier[0],blank_pos_row,blank_pos_col,blank_pos_row - 1, blank_pos_col)
        if new_generated_pos not in visited:
            pathCost = newdepth + manhattan_dist_finder(new_generated_pos,goalState)  # Path cost f(n) = g(n) + h(n)
            generatedNodes.append([new_generated_pos,parentNode,newdepth,pathCost])

    if blank_pos_col > 0:
        new_generated_pos = swap_tiles(frontier[0],blank_pos_row,blank_pos_col,blank_pos_row, blank_pos_col - 1)
        if new_generated_pos not in visited:
            pathCost = newdepth + manhattan_dist_finder(new_generated_pos,goalState)  # Path cost f(n) = g(n) + h(n)
            generatedNodes.append([new_generated_pos,parentNode,newdepth,pathCost])

    if blank_pos_row < 2:
        new_generated_pos = swap_tiles(frontier[0],blank_pos_row,blank_pos_col,blank_pos_row + 1, blank_pos_col)
        if new_generated_pos not in visited:
            pathCost = newdepth + manhattan_dist_finder(new_generated_pos,goalState)  # Path cost f(n) = g(n) + h(n)
            generatedNodes.append([new_generated_pos,parentNode,newdepth,pathCost])

    if blank_pos_col < 2:
        new_generated_pos = swap_tiles(frontier[0],blank_pos_row,blank_pos_col,blank_pos_row, blank_pos_col + 1)
        if new_generated_pos not in visited:
            pathCost = newdepth + manhattan_dist_finder(new_generated_pos,goalState)  # Path cost f(n) = g(n) + h(n)
            generatedNodes.append([new_generated_pos,parentNode,newdepth,pathCost])
           
    generatedNodes.sort(key=lambda x: x[3])                                 # Sorting the list based on f(n)          
    return generatedNodes

def testAStar(init,goalState,limit):
    '''Function to Test the A Star algorithm using the Manhattan Distance approach'''
    global goalFound                                        # Using the keyword global to change the variables defined in Global Context 
    global visited
    global totalRuns
    global totalDepth

    closed_set = []                                         # Closed Set to store the Nodes

    root = makeNode(init, 0, 0, 0)                          # Initialize the Root Node
 
    open_set=[root,]                                        # Insert the Root into the Open Set

    open_set[0][3]=open_set[0][2]+ manhattan_dist_finder(open_set[0][0],goalState)    # Calculate the Path Cost for Root

    while len(open_set) > 0:                                # Repeat the below steps till there are no more nodes in Open Set
        
        open_set.sort(key=lambda x:x[3])                    # Sort the Open Set based on Path Key
        
        current_node = open_set[0]                          # Assign the first node of Open Set to Current Node
       
        if current_node[0] not in visited:                     
                visited.append(current_node[0])             # Add the Current Node to Visited if not already present
        
        totalRuns+=1                                        # Keep track of the Total Runs
        
        if goalCheck(current_node,goalState):                     # Check if the Current Node is the Goal State
            #print "Goal found !"
            goalFound = True
            totalDepth = current_node[2]
            buildpath=getSolutionPath(0, current_node)                # Display the solution found and return True
            return buildpath

        open_set = open_set[1:]                             # Removing first Node from Open Set
        
        closed_set.append(current_node)                     # Appending the Node to Closed Set

        closed_set.sort(key=lambda x:x[3])                  # Sorting the Closed set based on Path Cost

        children = expandProcedureAstar(current_node,goalState)       # Finding the Children of the Current Node

        for i in range(len(children)):                      # For every child do the following
        
            # Check if the Child is already in Closed Set, if yes then Continue
            if children[i] in closed_set :              
                continue
            
            tentativeGn= current_node[2]+ 1                 # Calculate a Tentative g(n) value for the child
 
            # Check if the Child is Not in Open Set or if the calculated tentative g(n) is less than the depth(g(n)) of the child 
            if children[i] not in open_set or tentativeGn < children[i][2]: 
                children[i][1]=current_node                 # If either is true, make the Child as the Current Node 
                children[i][2]=tentativeGn                  # Assign the tentative g(n) to the Child's Depth
                children[i][3]=children[i][2]+manhattan_dist_finder(children[i][0],goalState) # Path cost of Child as Depth[g(n)] + Manhattan Distance(ChildState)
    
                if children[i] not in open_set:
                    open_set.append(children[i])            # If child not in Open Set, insert it.
                    open_set.sort(key=lambda x:x[3])        # Sort the Open Set based on Path Cost

    return False

def makeState(nw, n, ne, w, c, e, sw, s, se):
    '''
    Generates and returns a (board) state based on the given arguments 
    nw | n | ne
    ----------
    w  | c | e
    ----------
    sw | s | se
    '''
    return [[str(nw), str(n), str(ne)], [str(w), str(c), str(e)], [str(sw), str(s), str(se)]]
    
def print_board(board):  
    '''Function to print the board in a readable format'''
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] != "blank":  
                print board[i][j].rjust(1),
            else:
                print "".rjust(1),                              # Replace Blank with a Null string while displaying
            if j != 2:
                print "|",
        print ""
        if i != 2 :
            print '-'*10                                        
    print""

def similarityCheck(caseBase, initState, goalState):
    '''Function to check the similarity between the Problem Initial State - Case Base Initial State 
    and Case Base Goal State - Problem Goal State
    It also prints the Similarity Score Table in a tabular format for each case checked from the case base''' 
    global goalFound
    
    similarityScoreMasterList = []           
    print "Computing the similarity (based on Manhattan Distance) with the Initial and Goal State Pairs of the Case Base..."
    print
    print '%100s' %("*** "+"Similarity Score Table"+" ***")
    print "+"+"-"*160+"+"
    print '\t   %-55s%-42s%-25s%-30s' % ("\tCase Base Initial State","\tCase Base Goal State","Solution Path Length","Similarity Score")
    print "+"+"-"*160+"+"
        
    for eachPair in caseBase:
        simInit=manhattan_dist_finder(eachPair[0],initState)
        simGoal=manhattan_dist_finder(eachPair[1],goalState)
        simTotal = simInit+simGoal
        similarityScoreMasterList.append([eachPair,simTotal])
        print '   %-55s%-40s%15s%25s' % (str(eachPair[0][0]+eachPair[0][1]+eachPair[0][2]),str(eachPair[1][0]+eachPair[1][1]+eachPair[1][2]),str(eachPair[2]),str(simTotal))
        
    print "\n" 
    similarityScoreMasterList.sort(key=lambda x: x[1])    
    
    nearestSimilarPair = similarityScoreMasterList[0][0]
    nearestSimilarScore = similarityScoreMasterList[0][1]
    caseBaseTotalMoves =similarityScoreMasterList[0][0][2]
    caseBasePath = similarityScoreMasterList[0][0][3]
    
    simInit=manhattan_dist_finder(nearestSimilarPair[0],initState)
    simGoal=manhattan_dist_finder(nearestSimilarPair[1],goalState)
 
    return nearestSimilarPair,nearestSimilarScore,caseBaseTotalMoves,caseBasePath,simInit,simGoal         
        
def testCaseBasedSearch(listInitGoalPairs):
    '''Method to perform the Case Based Search for the given list of Initial - Goal State Pairs'''
    global similarityThreshold
    global caseBase
    
    performanceSheet = []                   # List to maintain the Performance Score of each problem pair                      
    count = 0;
    
    for eachPair in listInitGoalPairs:
        
        start_time = time.time()            # Track the Start Time
        totalTilesMovedSolution = 0
        count+=1
        
        #print eachPair        
        initState = makeState(*eachPair[0]) #Unpacking the list using *
        goalState = makeState(*eachPair[1]) #Unpacking the list using *
        
        initStateStr= str(initState[0]+initState[1]+initState[2])
        goalStateStr = str(goalState[0]+goalState[1]+goalState[2])
        problemID = str(count)
        
        # Print the current problem pair
        print "\nProblem #: "+problemID
        print"\tInitial State...\t"+initStateStr+ "\n\tGoal State......\t"+goalStateStr
        print        
        
        # If the case base is Empty, solve the problem from scratch. Update the case base with solution. Update step is added in puzzleSolve method
        if caseBase == []:
            print "Case Base is Empty!"
            print "Solving from Scratch..."
            flag,totalTilesMovedSolution,solutionPath = puzzleSolve(initState, goalState)
            if flag==True:
                displaySolutionPath(solutionPath)
                end_time = time.time()                                          # Track the End Time
                printCaseBase("Current Case Base")
        
                print
                print "+-"*90
                print "+-"*90
                print "+-"*90
                print
                
                time_elapsed =end_time-start_time                               # Calculate the Time Elapsed
                performanceSheet.append([problemID, initStateStr, goalStateStr, totalTilesMovedSolution, time_elapsed])    
                
            else: 
                print "Solution not found"
            continue
        
        
        # Check the case base for similar cases of the Problem Init and Goal State
        (nearestSimilarPair,nearestSimilarScore,caseBaseTotalMoves,caseBasePath,simInit,simGoal) = similarityCheck(caseBase, initState, goalState)
       
        # Similarity score is 0, An exact case has been found in the case base. 
        if nearestSimilarScore == 0:
            print "Exact case found in the Case Base"
            print "Retrieving the case"
            print "Total Tiles to be moved: "+str(caseBaseTotalMoves)
            #print "Complete Solution Path:" #+ str(caseBasePath)
            displaySolutionPath(caseBasePath)
            printCaseBase("Current Case Base")
            totalTilesMovedSolution=caseBaseTotalMoves
            
            print
            print "+-"*90
            print

            continue
        
        # Similarity score is less than the given threshold, adapt the case. 
        elif nearestSimilarScore > 0 and nearestSimilarScore < similarityThreshold:
           
            print "Case Base Pair with the best similarity score ("+ str(nearestSimilarScore)+") less than the threshold ("+str(similarityThreshold)+ ") chosen..."
            print "Adapting the case..."
            print "Initial State...\t"+str(nearestSimilarPair[0][0]+nearestSimilarPair[0][1]+nearestSimilarPair[0][2]) + \
                "\nGoal State......\t"+str(nearestSimilarPair[1][0]+nearestSimilarPair[1][1]+nearestSimilarPair[1][2])
            print
            print "Calculating the solution for (Current Problem Initial State --> Case Base Initial State)..."
            
            # Problem Initial state and Case Base Initial state are same
            if simInit == 0 :
                print "Current Problem Initial State and Case Base Initial State are same"
                flag_init=True
                tilesMoved_init=0
                solutionPath_init = []
            
            # Problem Initial state and Case Base Initial state are not same, find the solution for it    
            elif simInit <> 0 :
                flag_init,tilesMoved_init,solutionPath_init = puzzleSolve(initState, nearestSimilarPair[0])            
             
            print
            print "Calculating the solution for (Case Base Goal State --> Current Problem Goal State)..."        

            # Problem Goal state and Case Base Goal state are same           
            if simGoal == 0 :
                print "Case Base Goal State and Current Problem Goal State are same"
                print
                
                flag_goal=True
                tilesMoved_goal=0
                solutionPath_goal = []
                
            # Problem Goal state and Case Base Goal state are not same, find the solution for it                  
            elif simGoal <> 0 :
                flag_goal,tilesMoved_goal,solutionPath_goal = puzzleSolve(nearestSimilarPair[1], goalState) 
            
            # Solution for all found,
            if flag_goal==True and flag_init==True:
                totalTilesMovedSolution = tilesMoved_init+caseBaseTotalMoves+tilesMoved_goal
                completeSolutionPath_goal=solutionPath_init[:-1]+caseBasePath+solutionPath_goal[1:]
                
                print "-"*90
                print "Complete Solution for (Current Problem Initial State --> Current Problem Goal State)"
                print "-"*90
                print "Total Tiles to be moved: "+str(totalTilesMovedSolution)
                print
                # print "Complete Solution Path:" #+ str(completeSolutionPath_goal)
                # displaySolutionPath(completeSolutionPath_goal)
                
                # Display the appropriate output for Problem Init -> Case Base Init
                if solutionPath_init <> []:
                    print "\nCurrent Problem Initial State --> Previous State of Case Base Initial State "
                    displaySolutionPath(solutionPath_init[:-1])
                else : 
                    print "\nCurrent Problem Initial State --> Previous State of Case Base Initial State "
                    print "Current Problem Initial State and Case Base Initial State are same"

                # Display the appropriate output for Case Base Init -> Problem Goal               
                if solutionPath_goal <> []:
                    
                    print "\nCase Base Initial State --> Case Base Goal State"
                    displaySolutionPath(caseBasePath)
                    print "\nNext State of Case Base Goal State --> Current Problem Goal State "
                    displaySolutionPath(solutionPath_goal[1:])
                else:
                    print "\nCase Base Initial State --> Current Problem Goal State"
                    displaySolutionPath(caseBasePath)
                                 
                # Update the case base with the Complete Solution: (Current Problem Initial State --> Current Problem Goal State)
                caseBase.append([initState,goalState,totalTilesMovedSolution,completeSolutionPath_goal])
               
        # No case with Similarity less than the threshold found. Solve the problem from scratch       
        elif nearestSimilarScore >= similarityThreshold:
            print "No case having similarity less than the threshold ("+str(similarityThreshold)+ ") found in Case Base, hence solving from scratch.."
            flag,totalTilesMovedSolution,solutionPath = puzzleSolve(initState, goalState)
            if flag==True:
                displaySolutionPath(solutionPath)
            else: 
                print "Solution not found"
                continue
            

        end_time = time.time()                                          # Track the End Time

        # Print the case base 
        printCaseBase("Current Case Base")

        print
        print "+-"*90
        print "+-"*90
        print "+-"*90
        print
        
        time_elapsed =end_time-start_time                               # Calculate the Time Elapsed
        
        # Append the parameters in the Performance sheet for the current Problem
        performanceSheet.append([problemID, initStateStr, goalStateStr,totalTilesMovedSolution, time_elapsed])
        
    # Print Final Case Base and Other details at the end of all the problems    
    print
    printCaseBase("Final Case Base")
    print
    print "\n\nTotal Cases Processed in this run: ",str(count)
    print "Total Problems given: ",len(listInitGoalPairs)
    print "Similarity Threshold: ",str(similarityThreshold)
    
    printPerformanceSheet(performanceSheet)
    
  

def printCaseBase(header):
    ''' Method to print the Case Base in a tabular format'''
    
    print '%95s' %("*** "+header+" ***")
    print "+"+"-"*165+"+"
    print '   %-15s%-50s%-35s%-31s%-35s' % ("ID\t","\tInitial State","\tGoal State","Solution Path Length","Solution Path")
    print "+"+"-"*165+"+"
    
    caseID = 0
    for item in caseBase:
        caseID+=1
        #print '   %-55s%-40s%15s%42s' % (str(item[0][0]+item[0][1]+item[0][2]), str(item[1][0]+item[1][1]+item[1][2]),str(item[2]),"<..Hidden-Less-Space..>")
        print '  %3s    %-53s%-35s%13s%39s' % (str(caseID),str(item[0][0]+item[0][1]+item[0][2]), str(item[1][0]+item[1][1]+item[1][2]),str(item[2]),"<..Hidden-Less-Space..>")
        
    print 
     
def printPerformanceSheet(performanceSheet):
    ''' Method to print the Performance Sheet in a tabular format'''
    
    print '%95s' %("***Performance Summary***")
    print "+"+"-"*175+"+"
    print '   %-25s%-50s%-40s%-27s%-35s' % ("ProblemID\t","\tInitial State","\tGoal State","Solution Path Length","Time Taken (seconds)")
    print "+"+"-"*175+"+"
    
    for item in performanceSheet:
        #print '   %-55s%-40s%15s%42s' % (str(item[0][0]+item[0][1]+item[0][2]), str(item[1][0]+item[1][1]+item[1][2]),str(item[2]),"<..Hidden-Less-Space..>")
        print ' \t%-8s    %-53s%-62s%-18s%-39s' % (item[0],item[1],item[2],str(item[3]),str(item[4]))
        
    print 

    
def generateTestProblems(numTestCases):
    '''Method to generate Init and Goal State problem pairs based on the Number passed
    If the argument is 0, use the Hard Coded Problems
    Else, generate random Init and Goal State pairs'''
    
    listInitGoalPairs = []
    
    if numTestCases ==0 :
        
        # First group of test cases - should have solutions with depth <= 5
        listInitGoalPairs.append([[2, "blank", 3, 1, 5, 6, 4, 7, 8],[1, 2, 3, 4, 5, 6, 7, 8, 'blank']]) 
        listInitGoalPairs.append([[1, 2, 3, "blank", 4, 6, 7, 5, 8],[1, 2, 3, 4, 5, 6, 7, 8, 'blank']]) 
        listInitGoalPairs.append([[1, 2, 3, 4, 5, 6, 7, "blank", 8],[1, 2, 3, 4, 5, 6, 7, 8, 'blank']])         
        listInitGoalPairs.append([[1, "blank", 3, 5, 2, 6, 4, 7, 8],[1, 2, 3, 4, 5, 6, 7, 8, 'blank']])         
        listInitGoalPairs.append([[1, 2, 3, 4, 8, 5, 7, "blank", 6],[1, 2, 3, 4, 5, 6, 7, 8, 'blank']]) 
        
        # Second group of test cases - should have solutions with depth <= 10        
        listInitGoalPairs.append([[2, 8, 3, 1, "blank", 5, 4, 7, 6],[1, 2, 3, 4, 5, 6, 7, 8, 'blank']])         
        listInitGoalPairs.append([[1, 2, 3, 4, 5, 6, "blank", 7, 8],[1, 2, 3, 4, 5, 6, 7, 8, 'blank']])         
        listInitGoalPairs.append([["blank", 2, 3, 1, 5, 6, 4, 7, 8],[1, 2, 3, 4, 5, 6, 7, 8, 'blank']])         
        listInitGoalPairs.append([[1, 3, "blank", 4, 2, 6, 7, 5, 8],[1, 2, 3, 4, 5, 6, 7, 8, 'blank']])         
        listInitGoalPairs.append([[1, 3, "blank", 4, 2, 5, 7, 8, 6],[1, 2, 3, 4, 5, 6, 7, 8, 'blank']]) 
        
        # Third group of test cases - should have solutions with depth <= 20            
        listInitGoalPairs.append([["blank", 5, 3, 2, 1, 6, 4, 7, 8],[1, 2, 3, 4, 5, 6, 7, 8, 'blank']])         
        listInitGoalPairs.append([[5, 1, 3, 2, "blank", 6, 4, 7, 8],[1, 2, 3, 4, 5, 6, 7, 8, 'blank']])         
        listInitGoalPairs.append([[2, 3, 8, 1, 6, 5, 4, 7, "blank"],[1, 2, 3, 4, 5, 6, 7, 8, 'blank']])         
        listInitGoalPairs.append([[1, 2, 3, 5, "blank", 6, 4, 7, 8],[1, 2, 3, 4, 5, 6, 7, 8, 'blank']])         
        listInitGoalPairs.append([["blank", 3, 6, 2, 1, 5, 4, 7, 8],[1, 2, 3, 4, 5, 6, 7, 8, 'blank']])         
    
        # Fourth group of test cases - should have solutions with depth <= 50
        listInitGoalPairs.append([[2, 6, 5, 4, "blank", 3, 7, 1, 8],[1, 2, 3, 4, 5, 6, 7, 8, 'blank']])         
        listInitGoalPairs.append([[3, 6, "blank", 5, 7, 8, 2, 1, 4],[1, 2, 3, 4, 5, 6, 7, 8, 'blank']])         
        listInitGoalPairs.append([[1, 5, "blank", 2, 3, 8, 4, 6, 7],[1, 2, 3, 4, 5, 6, 7, 8, 'blank']])         
        listInitGoalPairs.append([[2, 5, 3, 4, "blank", 8, 6, 1, 7],[1, 2, 3, 4, 5, 6, 7, 8, 'blank']])         
        listInitGoalPairs.append([[3, 8, 5, 1, 6, 7, 4, 2, "blank"],[1, 2, 3, 4, 5, 6, 7, 8, 'blank']])    

    else : 
        
        masterListofStates = []
        masterListofStates.append([2, "blank", 3, 1, 5, 6, 4, 7, 8])
        masterListofStates.append([1, 2, 3, "blank", 4, 6, 7, 5, 8])
        masterListofStates.append([1, 2, 3, 4, 5, 6, 7, "blank", 8])
        masterListofStates.append([1, "blank", 3, 5, 2, 6, 4, 7, 8])
        masterListofStates.append([1, 2, 3, 4, 8, 5, 7, "blank", 6])
        masterListofStates.append([2, 8, 3, 1, "blank", 5, 4, 7, 6])
        masterListofStates.append([1, 2, 3, 4, 5, 6, "blank", 7, 8])
        masterListofStates.append(["blank", 2, 3, 1, 5, 6, 4, 7, 8])
        masterListofStates.append([1, 3, "blank", 4, 2, 6, 7, 5, 8])
        masterListofStates.append([1, 3, "blank", 4, 2, 5, 7, 8, 6])
        masterListofStates.append(["blank", 5, 3, 2, 1, 6, 4, 7, 8])
        masterListofStates.append([5, 1, 3, 2, "blank", 6, 4, 7, 8])
        masterListofStates.append([2, 3, 8, 1, 6, 5, 4, 7, "blank"])
        masterListofStates.append([1, 2, 3, 5, "blank", 6, 4, 7, 8])
        masterListofStates.append(["blank", 3, 6, 2, 1, 5, 4, 7, 8])
        masterListofStates.append([2, 6, 5, 4, "blank", 3, 7, 1, 8])
        masterListofStates.append([3, 6, "blank", 5, 7, 8, 2, 1, 4])
        masterListofStates.append([1, 5, "blank", 2, 3, 8, 4, 6, 7])
        masterListofStates.append([2, 5, 3, 4, "blank", 8, 6, 1, 7])
        masterListofStates.append([3, 8, 5, 1, 6, 7, 4, 2, "blank"])
        masterListofStates.append([2, "blank", 3, 1, 5, 6, 4, 7, 8])
        masterListofStates.append([1, 2, 3, 4, 8, 5, 7, "blank", 6])
        masterListofStates.append(["blank", 2, 3, 1, 5, 6, 4, 7, 8])
        masterListofStates.append([1, "blank", 3, 5, 2, 6, 4, 7, 8])
        masterListofStates.append([1, 3, "blank", 4, 2, 6, 7, 5, 8])
        
        problemCount = 0
        while problemCount <> numTestCases:
            randInit = random.choice(masterListofStates)
            randGoal = random.choice(masterListofStates)
            if randInit <> randGoal and [randInit,randGoal] not in listInitGoalPairs:
                listInitGoalPairs.append([randInit,randGoal])
                problemCount+=1
        
    testCaseBasedSearch(listInitGoalPairs)   

def puzzleSolve(initState, goalState):
    '''Solve the 8 puzzle problem with the given Init State and Goal State
    Also, append the solution to the case base'''
    
    # Global Variables
    global buildpath,visited,goalFound,totalDepth,caseBase
    buildpath = []                                                  # List to maintain the Path for the Obtained Solution
    visited = []                                                    # List to maintain the Visited States/Nodes
    goalFound = False                                               # Flag to check if the Solution is Found

    # Variables Initialization                                         
    limit = 1000                                                    # Initializing the limit in case the user doesn't define it
    totalRuns = 0
    totalDepth = 0
    tilesMovedSolution=0
        
                                            # Track the Start Time
    solutionPath=testAStar(initState, goalState, limit)   
      
    #Format and display the appropriate Output
    if goalFound:
        tilesMovedSolution = len(buildpath)-1
        #displaySolutionPath(solutionPath)
        # Update the case base with the solution
        caseBase.append([initState,goalState,tilesMovedSolution,buildpath])
        print "Solution Found!"
        print "Tiles moved for this solution : ", tilesMovedSolution
        print "Case Base updated with the new solution"
        print
        return True,tilesMovedSolution,solutionPath
    else:
        print "Solution Not Found!"
        return False,-1
    

#Main Program               
        
if __name__ == '__main__' :

    # Global Variables
    buildpath = []                                      # List to maintain the Path for the Obtained Solution
    visited = []                                        # List to maintain the Visited States/Nodes
    goalFound = False                                   # Flag to check if the Solution is Found
    caseBase = []
    # Variables Initialization    
    searchType=''                                       
    limit = 1000                                        # Initializing the limit in case the user doesn't define it
    totalRuns = 0
    totalDepth = 0
    similarityThreshold = 8

    
    # Formatting the Welcome Screen for the user
    print "\n\n"
    print "*"*100
    print "\t\t\t\t8-Puzzle Solver using Case Base"
    print "*"*100
    
    while True:
        try:
            numProblems = int(raw_input("Enter the number of problems to be generated (Enter 0 to use hardcoded problems)... "))
            similarityThreshold = int(raw_input("Enter the threshold for the Similarity Score [using Manhattan Distance] (Enter -1 to solve without using Case base)... "))
            break
        except ValueError:
            print "Oops!  That was no valid number.  Try again..."
        
    generateTestProblems(numProblems)
    
    
