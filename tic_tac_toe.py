#File Description	: Tic Tac Toe Game with One Player as AI and the Other as Human User
#Author 			: Ghanshyam Malu


from operator import pos

#print the current board 
def print_board():  
    print "Board..."
    for i in range(0,3):
        for j in range(0,3):
            print map[2-i][j],
            if j != 2:
                print "|",
        print ""
    print""

#check if the game is over
def check_done():
    for i in range(0,3):
        if map[i][0] == map[i][1] == map[i][2] != " " \
        or map[0][i] == map[1][i] == map[2][i] != " ":
            print_board()
            if turn==computer_symbol: 
                print "Computer Won!!!"
            else:
                print "You Won!!!"
            return True
        
    if map[0][0] == map[1][1] == map[2][2] != " " \
    or map[0][2] == map[1][1] == map[2][0] != " ":
        print_board()
        if turn==computer_symbol: 
            print "Computer Won!!!"
        else:
            print "You Won!!!"
        return True

    if " " not in map[0] and " " not in map[1] and " " not in map[2]:
        print_board()
        print "Game Draw !!!"
        return True
    
    return False

#Function to Generate the Computer Moves
def move_generate():

# 1. Try to Win - Check if the Computer has 2 symbols in any of the horizontal, vertical or diagonal lines. If yes, place the third and finish the Game !
    for i in range(0,3):
        if map[i][0] == map[i][1] == computer_symbol and map[i][2] == " " :
            map[i][2] = computer_symbol
            return
        elif map[i][1] == map[i][2] == computer_symbol and map[i][0] == " " :
            map[i][0] = computer_symbol
            return
        elif map[i][2] == map[i][0] == computer_symbol and map[i][1] == " " :
            map[i][1] = computer_symbol
            return
        elif map[0][i] == map[1][i] == computer_symbol and map[2][i] == " " :
            map[2][i] = computer_symbol
            return
        elif map[1][i] == map[2][i] == computer_symbol and map[0][i] == " " :
            map[0][i] = computer_symbol
            return
        elif map[2][i] == map[0][i] == computer_symbol and map[1][i] == " " :
            map[1][i] = computer_symbol
            return 
        elif map[0][0] == map[1][1] == computer_symbol and map[2][2] == " " :      
            map[2][2] = computer_symbol
            return
        elif map[1][1] == map[2][2] == computer_symbol and map[0][0] == " " :      
            map[0][0] = computer_symbol
            return
        elif map[2][2] == map[0][0] == computer_symbol and map[1][1] == " " :      
            map[1][1] = computer_symbol
            return
        elif map[0][2] == map[1][1] == computer_symbol and map[2][0] == " " :      
            map[2][0] = computer_symbol
            return
        elif map[1][1] == map[2][0] == computer_symbol and map[0][2] == " " :      
            map[0][2] = computer_symbol
            return
        elif map[2][0] == map[0][2] == computer_symbol and map[1][1] == " " :      
            map[1][1] = computer_symbol
            return                        

# 2. Try not to Lose - Check if the User has 2 symbols in any of the horizontal, vertical or diagonal lines. If yes, block the User from winning the Game !
    for i in range(0,3):
        if map[i][0] == map[i][1] == user_symbol and map[i][2] == " " :
            map[i][2] = computer_symbol
            return
        elif map[i][1] == map[i][2] == user_symbol and map[i][0] == " " :
            map[i][0] = computer_symbol
            return
        elif map[i][2] == map[i][0] == user_symbol and map[i][1] == " " :
            map[i][1] = computer_symbol
            return
        elif map[0][i] == map[1][i] == user_symbol and map[2][i] == " " :
            map[2][i] = computer_symbol
            return
        elif map[1][i] == map[2][i] == user_symbol and map[0][i] == " " :
            map[0][i] = computer_symbol
            return
        elif map[2][i] == map[0][i] == user_symbol and map[1][i] == " " :
            map[1][i] = computer_symbol
            return 
        elif map[0][0] == map[1][1] == user_symbol and map[2][2] == " " :      
            map[2][2] = computer_symbol
            return
        elif map[1][1] == map[2][2] == user_symbol and map[0][0] == " " :      
            map[0][0] = computer_symbol
            return
        elif map[2][2] == map[0][0] == user_symbol and map[1][1] == " " :      
            map[1][1] = computer_symbol
            return
        elif map[0][2] == map[1][1] == user_symbol and map[2][0] == " " :      
            map[2][0] = computer_symbol
            return
        elif map[1][1] == map[2][0] == user_symbol and map[0][2] == " " :      
            map[0][2] = computer_symbol
            return
        elif map[2][0] == map[0][2] == user_symbol and map[1][1] == " " :      
            map[1][1] = computer_symbol
            return                

#3.	Avoid Double Threats : If the User has his symbols in the opposite corners, try to avoid a probable Double Threat by placing in one of the side grids.
    if map[0][0] == user_symbol and map[2][2]== user_symbol:
        if map[1][0] == " " :
            map[1][0] = computer_symbol
            return
        elif map[1][2] == " " :
            map[1][2] = computer_symbol
            return
        elif map[0][1] == " " :
            map[0][1] = computer_symbol
            return
        elif map[2][1] == " " :
            map[2][1] = computer_symbol
            return        
                
    if map[0][2] == user_symbol and map[2][0]== user_symbol:
        if map[1][0] == " " :
            map[1][0] = computer_symbol
            return
        elif map[1][2] == " " :
            map[1][2] = computer_symbol
            return
        elif map[0][1] == " " :
            map[0][1] = computer_symbol
            return
        elif map[2][1] == " " :
            map[2][1] = computer_symbol
            return        
            

#4.	Grab the Middle Grid if available
    if   map[1][1] == " ":
        map[1][1] = computer_symbol
        return

#5.	If the User has played a corner, Grab the Opposite Corner if available
    if map[0][0] == user_symbol and map[2][2]== " ":
        map[2][2] = computer_symbol
        return
    elif map[0][2] == user_symbol and map[2][0] == " ":
        map[2][0] = computer_symbol
        return 
    elif map[2][2] == user_symbol and map[0][0] == " ":
        map[0][0] = computer_symbol
        return 
    elif map[2][0] ==user_symbol and map[0][2]== " ":
        map[0][2] = computer_symbol
        return 

#6. Grab the corner grid if available
    if map[0][0] == " ":
        map[0][0] = computer_symbol
        return
    elif map[0][2] == " ":
        map[0][2] = computer_symbol
        return 
    elif map[2][2] == " ":
        map[2][2] = computer_symbol
        return 
    elif map[2][0] == " ":
        map[2][0] = computer_symbol
        return 
                      
#7. Grab the side grid if available        
    if map[0][1] == " ":
        map[0][1] = computer_symbol
        return 
    elif map[1][0] == " ":
        map[1][0] = computer_symbol
        return
    elif map[1][2] == " ":
        map[1][2] = computer_symbol
        return 
    elif map[2][1] == " ":
        map[2][1] = computer_symbol
        return 
    
        
def mark_pos(pos,turn):
    Y = pos/3
    X = pos%3
    if X != 0:
        X -=1
    else:
         X = 2
         Y -=1
        
    if map[Y][X] != " ":
        print "Position already filled !\n"
    else:
        map[Y][X] = turn
        done = check_done()

        if done == False:
            if turn == "X":
                turn = "O"
            else:
                turn = "X"

    return turn

#--------------------------------
#Game Starts 
#--------------------------------
print "\n----------------"
print "Tic - Tac - Toe"
print "----------------\n"

#Variable to store User preferred symbol
user_symbol = raw_input("Select your symbol : X or O....  ").upper()

while user_symbol != 'X' and user_symbol != 'O' :
    print "Invalid Input !!"
    user_symbol = raw_input("Select your symbol : X or O....  ").upper()

if user_symbol == 'X' :
    computer_symbol = 'O'
else:
    computer_symbol = 'X'

print '\nAll Set !! \nComputer Plays:', computer_symbol ,' and You will Play:', user_symbol,'\n'

#Game starts with X
turn = 'X'

#List to store the Board
map = [[" "," "," "],
       [" "," "," "],
       [" "," "," "]]

#Variable to check if the User wants to Start a New Game after the current one is over
game_stop=False

#Variable to check if the Current Game is done
done = False


while game_stop != True:
    print_board()    
    if turn==computer_symbol :
        print "Computer's turn..."
        move_generate()
        """pos = move_generate()
        moved = False
        turn=mark_pos(pos,turn)"""
    else:        
        print "Your Turn..."
        print
        moved = False
        while moved != True:
            print "Please type a digit between 1 to 9 for the corresponding position... "
            print "7|8|9"
            print "4|5|6"
            print "1|2|3"
            print
    
            try:
                pos = input("Select: ")
                if pos <=9 and pos >=1:
                    Y = pos/3
                    X = pos%3
                    if X != 0:
                        X -=1
                    else:
                         X = 2
                         Y -=1
                        
                    if map[Y][X] != " ":
                        print "Position already filled !\n"
                    else:
                        map[Y][X] = turn
                        moved = True
                    
            except:
                print "You need to add a numeric value\n"
    
#Checking if the Game is Over. If no, switch the turns. If yes, Prompt the user to Start a New Game     
    done = check_done()
    
    if done == False:
        if turn == "X":
            turn = "O"
        else:
            turn = "X"
    else:
        user_choice = raw_input("Start a New Game? Y/N....").upper()
        
        while user_choice !='Y' and user_choice !='N' :
            print "Please enter Y or N..."
            user_choice = raw_input("Start a New Game? Y/N....").upper()            
        
        #User doesn't want to Start a New Game. End of Program
        if user_choice == 'N': 
            print "Good Bye...!!"
            game_stop = True 
        
        #User wants to Start a New Game. Initialize the variables
        else:  
            user_symbol = raw_input("Select your symbol : X or O....  ").upper()
            
            while user_symbol != 'X' and user_symbol != 'O' :
                print "Invalid Input !!"
                user_symbol = raw_input("Select your symbol : X or O....  ").upper()
            
            if user_symbol == 'X' :
                computer_symbol = 'O'
            else:
                computer_symbol = 'X'
            
            print '\nAll Set !! \nComputer Plays:', computer_symbol ,' and You will Play:', user_symbol,'\n'
            
            turn = 'X'
            
            map = [[" "," "," "],
                   [" "," "," "],
                   [" "," "," "]]
            
                  