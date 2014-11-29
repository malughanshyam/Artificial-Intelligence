# File Description      : A player for othello_main_gamePlay program using Adversarial Search: Minimax with Alpha Beta Pruning
# Author                : Ghanshyam Malu

'''
Detailed Description : 
Solve Othello using the Minimax algorithm with Alpha Beta Pruning. 
Given a board and time limit, this program returns the next best move for the player

The following heuristic strategies are used: 
1. Evaporation           : Also known as "Give Away" strategy. Try to have more enemy stones and fewer own stones until the initial 40 turns.
2. Mobility              : Try to reduce the opponent's mobility and increase the mobility for self.
3. Positional Weights : Assign a weight for each position on the Othello board based on its strength.
The total heuristic score is the weighted sum of above three strategies 
Set the Depth Limit for MiniMax algorithm based on Time and Total number of turns played

Depth Limit is set based on the following rules: 

If #TotalTurns < 20 ----> Then, Depth : 2

If 20 <= #TotalTurns <= 50 : 
    If Time < 10 seconds ---> Then,  Depth : 2 
    Else Depth : 4

If #TotalTurns > 50 : 
    If Time < 15 seconds  --->Then, Depth : 4 
    Else Depth : 6
        
'''
 
import gamePlay, time
from copy import deepcopy
from gamePlay import newBoard

initialTimeStamp = 0                                # Global variables to handle the Time elapsed to avoid a humiliating loss by Timeout
currentTimeStamp = 0
timeBuffer = 1                                    

def opponent(player):
    '''Function to get the opponent of the Player'''
    if player == 'W':
        return 'B'                                  # If the player is White, Return Black as the Opponent
    else:
        return 'W'                                  # If the player is Black, Return White as the Opponent

def possibleChildMoves(board,color):
    '''Function to get the valid moves for a Board''' 
    moves = []                                      # List to maintain the possible valid moves
    orderedMovesValues = []                         # List to maintain the moves and their heuristic values
    orderedMoves = []                               # List to maintain the ordered moves
    for i in range(8):
        for j in range(8):
            if gamePlay.valid(board, color, (i,j)): # Check if the generated move is valid
                moves.append((i,j))                 # Append the move to the list

    for move in moves : 
            newBoard = deepcopy(board)                      # Create a copy of the current board
            gamePlay.doMove(newBoard,color,move)            # Play the move to check its heuristic value
            currHeurValue = heurValue(newBoard,color)       # Find the heuristic value of the move
            orderedMovesValues.append([currHeurValue,move]) # Append the move along with its heuristic value to a new list
    
    orderedMovesValues.sort(key=lambda x: x[0],reverse = True) # Sort the list in Descending order based on heuristic value

    for i in range(0,len(orderedMovesValues)):
        orderedMoves.append(orderedMovesValues[i][1])       # Extract the set of moves from the Ordered Heuristic List

    return orderedMoves                                     # Return the Ordered Moves
  
def mobility(board,color):
    '''Function to find the mobility of the current color/player on the Board''' 
    mobilityCount = 0                               # Counter to maintain the mobility
    for i in range(8):
        for j in range(8):
            if gamePlay.valid(board, color, (i,j)): # Check if the generated move is valid
                mobilityCount +=1                   # Increment the mobility count

    return mobilityCount                            # Return the mobility
    
def totalPlayed(board):
    '''Function to calculate the total number of White and Black pieces on the board'''
    value = 0
    for row in board:
        for elem in row:
            if elem != '.':                         # Check if the tile is not empty
                value += 1                          # Increment the Value if a tile is not empty
    return value

def heurValue(board,color):
    '''Function to determine a heuristic value for a given board'''
    countGoodnessWeight = 80
    posGoodnessWeight = 60
        
    totalPlayedStones = totalPlayed(board)              # Find the total number of turns played
    
    # Strategy - 1 : Evaporation
    enemyStones,friendlyStones = 0,0                    # Counter for the current players and the opponent's tiles
    for row in board:
        for elem in row:
            if elem == color:                           # Check if the piece on the tile belongs to the current player
                friendlyStones += 1                     # Increment the counter
            elif elem == opponent(color):               # Check if the piece on the tile belongs to the opponent player
                enemyStones -= 1                        # Decrement the counter
    
    earlyGame =  totalPlayedStones < 40                 # Check if its the early phase of the game 
    
    if earlyGame : 
        countGoodness = countGoodnessWeight * (enemyStones - friendlyStones) # If yes, follow evaporation strategy
    else: 
        countGoodness = countGoodnessWeight * (friendlyStones - enemyStones) # Else, follow reverse of evaporation

    # Strategy - 2 : Positional Weights
    posWeight = 0                                   # Variable to maintain the weight of the board based on the position matrix
    eval_board = [
    [99,  -8,  8,  6,  6,  8,  -8, 99],
    [-8, -24, -4, -3, -3, -4, -24, -8],
    [ 8,  -4,  7,  4,  4,  7,  -4,  8],
    [ 6,  -3,  4,  0,  0,  4,  -3,  6],
    [ 6,  -3,  4,  0,  0,  4,  -3,  6],
    [ 8,  -4,  7,  4,  4,  7,  -4,  8],
    [-8, -24, -4, -3, -3, -4, -24, -8],
    [99,  -8,  8,  6,  6,  8,  -8, 99]]             # Positional Matrix with the appropriate weights for each tiles

    for i in range(8):
        for j in range(8):
            if board[i][j] == color:                # If the piece on the tile belongs to the current player
                posWeight+=eval_board[i][j]         # Increment the variable with the positional weight
            elif board[i][j] == opponent(color):    # If the piece on the tile belongs to the opponent player
                posWeight-=eval_board[i][j]         # Decrement the variable with the positional weight
                
    positionalGoodness = posGoodnessWeight * posWeight  # Weighted Positional Goodness Score is calculated 

    # Strategy - 3 : Mobility
    friendlyMobilityCount = mobility(board, color)      # Find the total number of valid moves for the current player
    enemyMobilityCount = mobility(board,opponent(color))# Find the total number of valid moves for the opponent player
    mobilityGoodness = (-100 * enemyMobilityCount)+(100 * friendlyMobilityCount) # Weighted score of the mobility 
 
    # Calculate and return the total heuristic score
    totalHeuristicValue = countGoodness + positionalGoodness + mobilityGoodness 
    return totalHeuristicValue

def nextMove(board, color, timeDuration, reversed = False):
    '''Function called to play the next move from gamePlay.py'''
    global initialTimeStamp                         # Changing the scope to Global for the variable
    global currentTimeStamp                         # Changing the scope to Global for the variable
    global timeBuffer                               # Changing the scope to Global for the variable

    if timeDuration > 1:                            # Resetting the Time Buffer based on the Time duration passed from Game Play
        timeBuffer = 1
    initialTimeStamp = time.time()                  # Capturing the time stamp at the moment nextMove is called
    
    childMoves = possibleChildMoves(board, color)   # Get the possible valid moves for the board
    if len(childMoves) == 0:                        # If there are no more valid moves, return Pass
        return "pass"
    if len(childMoves) == 1 :                       # If there is only One valid move, return it
        return childMoves[0]
    totalPlayedTiles = totalPlayed(board)           # Find the total number of pieces on the board. 
    
    # Based on the total number pieces on the board, determine the depth limit for the minimax
    if totalPlayedTiles < 20:                       # If the total number of turns is less than 20, set the depth limit to 2
        depthLimit = 2
    #If the total turns is in the range of 20 and 50, set the limit to 4 or 2 based on time
    elif totalPlayedTiles >= 20 and totalPlayedTiles < 50: 
        if timeDuration < 10:                       # If the remaining time is less than 10 seconds, set the depth limit to 2. Else, 4
            depthLimit = 2
        else:                
            depthLimit = 4
    #If the total turns is greater than 50, set the limit to 6 or 4 based on time
    else :                              
        if timeDuration < 15:                       # If the remaining time is less than 15 seconds, set the depth limit to 4. Else, 6
            depthLimit = 4
        else:                
            depthLimit = 6
                
    bestScore = 0                                   # Initialize the best score to 0
    bestMove = childMoves[0]                        # Initialize the best move to be the first move of the list
     
    for move in childMoves:                         # For every valid move, perform the following
    
        currentTimeStamp = time.time()                      # Capture the current time stamp
        timeElapsed = currentTimeStamp - initialTimeStamp   # Find the time elapsed since the call from Game Play
        if timeElapsed > (timeDuration - timeBuffer):       # Check if the time elapsed is more than the allowed duration minus buffer
            return bestMove
        
        newBoard = deepcopy(board)                  # Make a copy of the current board
        gamePlay.doMove(newBoard,color,move)        # Play the move to check if its best using the upcoming operations
        
        # Call the Minimax - Alpha Beta Pruning algorithm with Depth Limit, Alpha, Beta, Opponent Player and Maximizing Flag as False
        score = miniMaxAlphaBeta(newBoard, depthLimit-1,-10000,10000, opponent(color) , False, timeDuration)  
        if  score > bestScore:                      # If the returned score is better than the best Score, update the Best Score and Move
            bestMove = move
            bestScore = score
            
    return bestMove                                 # Return the best move

def miniMaxAlphaBeta(board , depth ,alpha,beta, color, maximizingPlayer,timeDuration):
    '''Minimax algorithm to find the best move''' 

    currentTimeStamp = time.time()                              # Capturing the current time stamp
    timeElapsed = currentTimeStamp - initialTimeStamp           # Calculating the time elapsed since the call from Game Play

    if depth == 0 or timeElapsed > (timeDuration - timeBuffer): # Check if the Depth has reached the limit
        currHeurValue = heurValue(board, color)                 # If yes, return the heuristic value of the current board
        return currHeurValue

    childMoves = possibleChildMoves(board, color)   # Get the possible valid moves for the board

    if len(childMoves)==0:                          # Check if there are no more valid moves
        currHeurValue = heurValue(board, color)     # If yes, return the heuristic value of the current board
        return currHeurValue

    if maximizingPlayer == True:                    # Run if its Maximizing Players turn
        for move in childMoves:                     # For every valid move, do the following
            newBoard = deepcopy(board)              # Create a copy of the current board
            gamePlay.doMove(newBoard,color,move)    # Play the move to check if its best using the upcoming operations

            # Call the Minimax - Alpha Beta Pruning algorithm with the Depth, Alpha, Beta, Inverted Color and Maximizing Flag as False
            result = miniMaxAlphaBeta(newBoard, depth-1,alpha,beta, opponent(color), False,timeDuration)

            alpha = max(alpha, result)              # Get the maximum of the alpha and result
            if alpha >= beta:                       # Check if Alpha >= Beta
                break                               # Prune, if True
        return alpha                                # Return Alpha
        
    if maximizingPlayer == False:                   # Run if its Minimizing Players turn
        for move in childMoves:                     # For every valid move, do the following
            newBoard = deepcopy(board)              # Create a copy of the current board
            gamePlay.doMove(newBoard,color,move)    # Play the move to check if its best using the upcoming operations 
            
            # Call the Minimax - Alpha Beta Pruning algorithm with the Depth, Alpha, Beta, Inverted Color and Maximizing Flag as True               
            result = miniMaxAlphaBeta(newBoard, depth-1,alpha,beta, opponent(color), True,timeDuration)

            beta = min(beta,result)                 # Get the maximum of the alpha and result
            if beta <= alpha:                       # Check if Alpha >= Beta
                break                               # Prune, if True
        return beta                                 # Return Beta
