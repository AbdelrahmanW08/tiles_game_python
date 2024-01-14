"""
This program will run the game Tiles. Tiles is a game where there is a 4 by 4 board with 15 tiles.
Each tile will be numbered 1-15. As one tile, is missing, the tiles are able to move around.
The objective of the game is to move the tiles around until they are in the right order numeically (Left to right, top to bottom).
The board will be randomized at the start of each round and will be able to be replayed multiple times.
The game will ask for the user's name and store each user's score by name (+1 score for each board completed).
"""

# Importing necessary libraries
import random

def generate_board():
    '''
    Function to generate a random 4x4 2D Array which would represent the board, enumerated with one number "missing"
    '''
    board = [i for i in range(1,16)] + [' ']
    random.shuffle(board)
    board = [board[0:4], board[4:8], board[8:12], board[12:16]]
    return board

def print_board(file, board):
    '''
    Function to print the 2D Array in the form of a board onto the console
    '''
    print_both(file, "+----+----+----+----+")
    for i in range(4):
        print_both(file, f'| {board[i][0]: <2} | {board[i][1]: <2} | {board[i][2]: <2} | {board[i][3]: <2} |')
        print_both(file, "+----+----+----+----+")

def get_user_move(file, board):
    '''
    Function to get the number of the square the user wants to move
    '''

    # Runs until user inputs a correct number
    while True:
        move = input("Please enter the number you want to move: ")
        if not move.isdigit() or int(move) < 1 or int(move) > 15 or not is_adjacent(board, int(move)):
            print('Invalid move! Try again.')
        else:
            file.write(f"Please enter the number you want to move: {move}\n")
            return int(move)

def is_adjacent(board, move):
    '''
    Function to check if a given number is beside the empty square
    '''
    x1,y1 = get_pos(board, move)
    x2,y2 = get_pos(board, ' ')
    return (x1+y1 == x2+y2 + 1 and (x1==x2+1 or y1==y2+1)) or (x1+y1 == x2+y2 - 1 and (x1==x2-1 or y1==y2-1))

def get_pos(board, num):
    '''
    Function to get the x and y position of a number in the 2D Array
    '''
    for i in range(4):
        for j in range(4):
            if board[i][j] == num:
                return i, j

def swap(board, num):
    '''
    Function to swap the postion of a given number with the empty square in the 2D Array
    '''
    num_pos = get_pos(board, num)
    empty_pos = get_pos(board, ' ')
    board[empty_pos[0]][empty_pos[1]] = num
    board[num_pos[0]][num_pos[1]] = ' '

def board_completed(board):
    '''
    Function to check if the board is in correct sequence (1-15 from left to right, top to bottom)
    '''
    return board == [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,' ']]

def increment_score(name, filename):
    '''
    Function to increment users score by 1 in a file
    '''

    # Entering Try to catch any FileNotFound errors
    try: 
        
        # Read all names and scores in file
        with open(filename, "r") as file:
            scores = file.read().split('\n')[1:-1]

        # Find users name and increment their score
        f=True
        for i in range(len(scores)):
            if name in scores[i]:
                score = int(scores[i].split(':')[1].strip()) + 1
                scores[i] = name + ": " + str(score)
                f=False
        
        # If you can't find them, add them to the list
        if f:
            score = 1
            scores = scores + [f'{name}: {str(score)}']

        # Rewrite everyones names and scores to file
        with open(filename, "w") as file:
            file.write("Scores\n")
            for i in scores:
                file.write(i+'\n')
        return score
    except:

        # Make a new file if you can't find one
        with open(filename, "w") as file:
            file.write("Scores\n")
            file.write(f'{name}: 1')
        return 1

def get_name(file):
    '''
    Function to get user's name and excludes all non-alpha characters
    '''
    name = input("Please enter your name for scorekeeping: ").lower()
    file.write(f"Please enter your name for scorekeeping: {name}\n")
    newname=''
    for i in name:
        if i in "abcdefghijklmnopqrstuvwxyz":
            newname+=i
    return newname

def get_replay(file):
    '''
    Function to ask user if they want to replay the game
    '''

    # Runs until users inputs either 'y' or 'n'
    while True:
        replay = input("Would you like to play again (y/n)? ")
        if replay.lower() == 'y':
            file.write("Would you like to play again (y/n)? y\n")
            return True
        elif replay.lower() == 'n':
            file.write("Would you like to play again (y/n)? n\n")
            return False

def print_both(file, *args):
    '''
    Function to print both to console and to the output file
    '''
    toprint = ' '.join([str(arg) for arg in args])
    print(toprint)
    file.write(toprint+"\n")

def tilesgame():
    '''
    Main function to run the game
    '''

    # Initialize needed variables
    replay = True # Set to True to run game for first time
    output_file = open('cps109_a1_output.txt', 'w') # File to output everything to

    # Displays start of game and gets user's name
    print_both(output_file, "Welcome to the Tiles Game!")
    name = get_name(output_file)

    # Runs as long as user wants to keep playing
    while replay:

        # Generate a random board
        print_both(output_file, "The game will now begin.")
        board = generate_board()

        # Runs as long as the board is not yet completed
        while not board_completed(board):
            print_board(output_file, board)

            # Ask user for their move and make the change in the 2D Array
            move = get_user_move(output_file, board)
            swap(board, move)

            # Check if the board is completed
            if board_completed(board):

                # Congratulate user and increment their score
                print_board(output_file, board)
                print_both(output_file, f"Congratulations! You completed the board!")
                score = increment_score(name, 'scores.txt')
                print_both(output_file, f"{name.capitalize()}, your score is now: {score}")

                # Ask if they want to replay
                replay = get_replay(output_file)

    # Closing output file
    output_file.close()

if __name__ == "__main__":
    tilesgame()