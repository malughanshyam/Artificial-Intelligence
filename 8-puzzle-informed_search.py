# File Description      : 8-Puzzle Solver using Informed Search
# Author                  : Ghanshyam Malu

'''
Detailed Description : 
Program to solve 8-puzzle using the Best-First Search for each of the following Heuristics:  
    1. Heuristic 1 (Misplaced Tiles Count Approach) 
    2. Heuristic 2 (Manhattan Distance Approach) 
    3. A* 
'''

import time, sys, os.path , math                            # Importing the modules used in the program

def makeNode(state, parent=None, depth=0, pathCost=0):
    '''Function to Create a Node'''
    return [state, parent, depth, pathCost]                 # Returns a Node with the 4 fields

def testProcedure(state):  
    '''Function to Test if Goal is found'''
    for i in range(0,3):
        for j in range(0,3):
            if state[0][i][j] != goalState[i][j]:           # Cross checks each Tile of the given State with the Goal State defined
                return False            
    return True
           
def outputProcedure(numRuns, queue):
    '''Function to Display the found solution'''
    print "Solution Path"
    print "-"*20 
    recursive_path_build(queue)                             # Generate a list of the nodes for the solution based on the parents of each node
    buildpath.reverse()
    for i in range(len(buildpath)):
        print_board(buildpath[i])

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
    
def misplaced_tile_counter(state):
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

def manhattan_dist_finder(state):
    '''Function to Find the Manhattan Distance of the Tiles for a given board'''
    global goalState         
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


def heuristic_sorter1(queue):
    '''Function for Misplaced Tiles Count Heuristic''' 
    for item in queue :
        state = item[0]
        misplaced_tile_count = misplaced_tile_counter(state)
        item[3]= misplaced_tile_count                       # Changing the Path Cost of Each Item to f(n) = h(n)                   
    queue.sort(key=lambda x: x[3])                          # Sorting the list based on Heuristic Value f(n) i.e Misplaced Tiles Count
    return queue    

def heuristic_sorter2(queue):
    '''Function for Manhattan Distance Heuristic'''     
    for item in queue :
        state = item[0]
        manhattan_dist = manhattan_dist_finder(state)
        item[3]= manhattan_dist                             # Changing the Path Cost of Each Item to f(n) = h(n)                   
    queue.sort(key=lambda x: x[3])                          # Sorting the list based on Heuristic Value f(n) i.e Manhattan Distance
    return queue

   
def expandProcedureAstar(frontier):
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
            pathCost = newdepth + manhattan_dist_finder(new_generated_pos)  # Path cost f(n) = g(n) + h(n)
            generatedNodes.append([new_generated_pos,parentNode,newdepth,pathCost])

    if blank_pos_col > 0:
        new_generated_pos = swap_tiles(frontier[0],blank_pos_row,blank_pos_col,blank_pos_row, blank_pos_col - 1)
        if new_generated_pos not in visited:
            pathCost = newdepth + manhattan_dist_finder(new_generated_pos)  # Path cost f(n) = g(n) + h(n)
            generatedNodes.append([new_generated_pos,parentNode,newdepth,pathCost])

    if blank_pos_row < 2:
        new_generated_pos = swap_tiles(frontier[0],blank_pos_row,blank_pos_col,blank_pos_row + 1, blank_pos_col)
        if new_generated_pos not in visited:
            pathCost = newdepth + manhattan_dist_finder(new_generated_pos)  # Path cost f(n) = g(n) + h(n)
            generatedNodes.append([new_generated_pos,parentNode,newdepth,pathCost])

    if blank_pos_col < 2:
        new_generated_pos = swap_tiles(frontier[0],blank_pos_row,blank_pos_col,blank_pos_row, blank_pos_col + 1)
        if new_generated_pos not in visited:
            pathCost = newdepth + manhattan_dist_finder(new_generated_pos)  # Path cost f(n) = g(n) + h(n)
            generatedNodes.append([new_generated_pos,parentNode,newdepth,pathCost])
           
    generatedNodes.sort(key=lambda x: x[3])                                 # Sorting the list based on f(n)          
    return generatedNodes


def testAStar(init,goal,limit):
    '''Function to Test the A Star algorithm using the Manhattan Distance approach'''
    global goalFound                                        # Using the keyword global to change the variables defined in Global Context 
    global visited
    global totalRuns
    global totalDepth

    closed_set = []                                         # Closed Set to store the Nodes

    root = makeNode(init, 0, 0, 0)                          # Initialize the Root Node
 
    open_set=[root,]                                        # Insert the Root into the Open Set

    open_set[0][3]=open_set[0][2]+ manhattan_dist_finder(open_set[0][0])    # Calculate the Path Cost for Root

    while len(open_set) > 0:                                # Repeat the below steps till there are no more nodes in Open Set
        
        open_set.sort(key=lambda x:x[3])                    # Sort the Open Set based on Path Key
        
        current_node = open_set[0]                          # Assign the first node of Open Set to Current Node
       
        if current_node[0] not in visited:                     
                visited.append(current_node[0])             # Add the Current Node to Visited if not already present
        
        totalRuns+=1                                        # Keep track of the Total Runs
        
        if testProcedure(current_node):                     # Check if the Current Node is the Goal State
            print "Goal found !"
            goalFound = True
            totalDepth = current_node[2]        
            outputProcedure(0, current_node)                # Display the solution found and return True
            return True

        open_set = open_set[1:]                             # Removing first Node from Open Set
        
        closed_set.append(current_node)                     # Appending the Node to Closed Set

        closed_set.sort(key=lambda x:x[3])                  # Sorting the Closed set based on Path Cost

        children = expandProcedureAstar(current_node)       # Finding the Children of the Current Node

        for i in range(len(children)):                      # For every child do the following
        
            # Check if the Child is already in Closed Set, if yes then Continue
            if children[i] in closed_set :              
                continue
            
            tentativeGn= current_node[2]+ 1                 # Calculate a Tentative g(n) value for the child
 
            # Check if the Child is Not in Open Set or if the calculated tentative g(n) is less than the depth(g(n)) of the child 
            if children[i] not in open_set or tentativeGn < children[i][2]: 
                children[i][1]=current_node                 # If either is true, make the Child as the Current Node 
                children[i][2]=tentativeGn                  # Assign the tentative g(n) to the Child's Depth
                children[i][3]=children[i][2]+manhattan_dist_finder(children[i][0]) # Path cost of Child as Depth[g(n)] + Manhattan Distance(ChildState)
    
                if children[i] not in open_set:
                    open_set.append(children[i])            # If child not in Open Set, insert it.
                    open_set.sort(key=lambda x:x[3])        # Sort the Open Set based on Path Cost

    return False

                               
def generalSearch(queue, limit, numRuns, searchType):
    '''Recursive function to solve the 8 puzzle using the algorithm based on the searchType'''
    
    global totalDepth                               # Using the keyword global to change the variables defined in Global Context
    global totalRuns
    global goalFound
    
     
    #If First node of the Queue has not been visited yet, insert it into the Visited queue
    if queue[0] not in visited:
        visited.append(queue[0][0])
    
    #If the Queue is empty, the search returns False
    if queue == []:
        return False
    
    #Check if the First Node in the Queue is the Solution. If yes, then call the outputProcedure to display the solution obtained.
    elif testProcedure(queue[0]):

        print "Goal found !"
        goalFound = True        
        outputProcedure(numRuns, queue[0])

        totalDepth = queue[0][2]                                    #Assign the total depth of the Solution Node
        totalRuns = numRuns                                         #Assign the total number of runs 
       
    #If solution is not found, check if the Limit has been reached.   
    elif limit == 0:
        totalDepth = queue[0][2]
        totalRuns = numRuns
        print "Limit reached!"
        print "Goal could not be found!"
          
    else:
        limit -= 1
        numRuns += 1
        
        queue = expandProcedure(queue[0], queue[1:len(queue)], searchType)
        
        if  searchType == 'HEUR1':
            queue=heuristic_sorter1(queue)                          # Sort the queue based on the Heuristic Function - Misplaced Tiles Count
        elif searchType == 'HEUR2':
            queue=heuristic_sorter2(queue)                          # Sort the queue based on the Heuristic Function - Manhattan Distance
            
        generalSearch(queue, limit, numRuns,searchType)             # Recursive call to General Search with the new expanded list 

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
    

def testInformedSearch1(init, goal, limit):
    '''Main function for the Informed Search 1 -> Heuristic 1 (Misplaced Tiles Count Approach) '''
    root = makeNode(init, 0, 0, 0)                              # Create a Root Node with the Initial State passed
    generalSearch([root,],limit , 1,searchType)                 # Start the search with the Root
    
    
def testInformedSearch2(init, goal, limit):
    '''Main function for the Informed Search 1 -> Heuristic 2 (Manhattan Distance Approach) '''
    root = makeNode(init, 0, 0, 0)                              # Create a Root Node with the Initial State passed
    generalSearch([root,],limit , 1,searchType)                 # Start the search with the Root

    
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


def initialize_test_case(userinitialstate):
    '''Function to initialize a Test Case for the Auto Test approach'''
    '''This function obtains the input from the Command Line Argument argv[1]'''
    # First group of test cases - should have solutions with depth <= 5        
    if userinitialstate == '1' :
        userdefinedstate = makeState(2, "blank", 3, 1, 5, 6, 4, 7, 8)
    elif userinitialstate == '2' :             
        userdefinedstate = makeState(1, 2, 3, "blank", 4, 6, 7, 5, 8)
    elif userinitialstate == '3' :   
        userdefinedstate = makeState(1, 2, 3, 4, 5, 6, 7, "blank", 8)
    elif userinitialstate == '4' :               
        userdefinedstate = makeState(1, "blank", 3, 5, 2, 6, 4, 7, 8)
    elif userinitialstate == '5' :               
        userdefinedstate = makeState(1, 2, 3, 4, 8, 5, 7, "blank", 6)

    # Second group of test cases - should have solutions with depth <= 10
    elif userinitialstate == '6' :     
        userdefinedstate = makeState(2, 8, 3, 1, "blank", 5, 4, 7, 6)
    elif userinitialstate == '7' :     
        userdefinedstate = makeState(1, 2, 3, 4, 5, 6, "blank", 7, 8)
    elif userinitialstate == '8' :     
        userdefinedstate = makeState("blank", 2, 3, 1, 5, 6, 4, 7, 8)
    elif userinitialstate == '9' :     
        userdefinedstate = makeState(1, 3, "blank", 4, 2, 6, 7, 5, 8)
    elif userinitialstate == '10' :     
        userdefinedstate = makeState(1, 3, "blank", 4, 2, 5, 7, 8, 6)

    # Third group of test cases - should have solutions with depth <= 20
    elif userinitialstate == '11' :     
        userdefinedstate = makeState("blank", 5, 3, 2, 1, 6, 4, 7, 8)
    elif userinitialstate == '12' :      
        userdefinedstate = makeState(5, 1, 3, 2, "blank", 6, 4, 7, 8)
    elif userinitialstate == '13' :         
        userdefinedstate = makeState(2, 3, 8, 1, 6, 5, 4, 7, "blank")
    elif userinitialstate == '14' :     
        userdefinedstate = makeState(1, 2, 3, 5, "blank", 6, 4, 7, 8)
    elif userinitialstate == '15' :     
        userdefinedstate = makeState("blank", 3, 6, 2, 1, 5, 4, 7, 8)

    # Fourth group of test cases - should have solutions with depth <= 50
    elif userinitialstate == '16' :     
        userdefinedstate = makeState(2, 6, 5, 4, "blank", 3, 7, 1, 8)
    elif userinitialstate == '17' :     
        userdefinedstate = makeState(3, 6, "blank", 5, 7, 8, 2, 1, 4)
    elif userinitialstate == '18' :     
        userdefinedstate = makeState(1, 5, "blank", 2, 3, 8, 4, 6, 7)
    elif userinitialstate == '19' :     
        userdefinedstate = makeState(2, 5, 3, 4, "blank", 8, 6, 1, 7)
    elif userinitialstate == '20' :     
        userdefinedstate = makeState(3, 8, 5, 1, 6, 7, 4, 2, "blank")
    
    return userdefinedstate

#Main Program               
if __name__ == '__main__' :

    # Global Variables
    buildpath = []                                      # List to maintain the Path for the Obtained Solution
    visited = []                                        # List to maintain the Visited States/Nodes
    goalFound = False                                   # Flag to check if the Solution is Found

    # Variables Initialization    
    searchType=''                                       
    limit = 1000                                        # Initializing the limit in case the user doesn't define it
    totalRuns = 0
    totalDepth = 0
    testCaseNum = '2'                                   # Initialize the Test Case number, in case the User doesn't specify in the next block.
    
    # Defining the Goal State
    goalState = makeState(1, 2, 3, 4, 5, 6, 7, 8, "blank") 
    #goalState = makeState(1, 2, 3, 8, "blank", 4, 7, 6, 5)    # Alternate Goal State 

    # Formatting the Welcome Screen for the user
    print "\n\n"
    print "*"*90
    print "\t\t\t\t\t8-Puzzle Solver"
    print "*"*90
    
    #Handling the Command Line Input
    if len(sys.argv)==4:                                            # Check if the number of arguments given are 4
        userinitialstate = sys.argv[1].strip()                      # Second argument = Test Case #
        userdefinedstate = initialize_test_case(userinitialstate)   # Map the Test Case Number given to a defined State in the Test Cases
        searchType = sys.argv[2].strip().upper()                    # Third argument = Search Type <HEUR1|HEUR2|ASTAR>
        limit = int(sys.argv[3])                                    # Forth Argument = Limit given

    #If none or partial command line arguments given :  
    while searchType != 'HEUR1' and searchType != 'HEUR2' and searchType != 'ASTAR':
        if len(sys.argv)==2 and int(sys.argv[1]) in range(1,21):
            userinitialstate = sys.argv[1].strip()                  # Assign the Test Case Number
        else:
            userinitialstate = testCaseNum                          # If none given, Initialize it based on the testCaseNum variable                        

        userdefinedstate = initialize_test_case(userinitialstate)   # Map the Test Case Number given to a defined State in the Test Cases

        print "\nTip: You can also run this program as follows : \npython ", os.path.basename(sys.argv[0].strip()), "<testcase# in [1|..|20]> <HEUR1|HEUR2|ASTAR> <LIMIT>\n"
    
        userchoice = raw_input("Choose the approach to be used...  \n"
              "1. Heuristic 1 (Misplaced Tiles Count Approach) \n"\
              "2. Heuristic 2 (Manhattan Distance Approach) \n"\
              "3. A* Search...  :").strip()
        if userchoice == '1':
            searchType = 'HEUR1'
        elif userchoice == '2':
            searchType = 'HEUR2'     
        elif userchoice == '3':
            searchType = 'ASTAR'
        else:
            print "Invalid Arguments"       
    
    initialState = userdefinedstate

    start_time = time.time()                                        # Track the Start Time

    if searchType == 'HEUR1':
        testInformedSearch1(initialState, goalState, limit)
    elif searchType == 'HEUR2':
        testInformedSearch2(initialState, goalState, limit)   
    elif searchType == 'ASTAR':    
        testAStar(initialState, goalState, limit)

    end_time = time.time()                                          # Track the End Time
    
    time_elapsed =end_time-start_time                               # Calculate the Time Elapsed
    totalNodes = len(visited)
    branching_factor = math.pow(totalNodes, 1/float(totalDepth))
    
    #Format and display the appropriate Output
    print "-"*20
    print "Summary"
    print "-"*20
    
    if goalFound:
        print "Puzzle Solved!"
        print "Tiles moved in the above Solution : ", len(buildpath)-1
    else:
        print "Puzzle Unsolved!"
    
    print "Time Elapsed\t\t: %.3f seconds" %time_elapsed
    print "Total Runs\t\t: ", totalRuns
    print "Visited Nodes\t\t: ", totalNodes
    print "Depth\t\t\t: ", totalDepth
    print "Effective Branching Factor\t: %.2f" %branching_factor
