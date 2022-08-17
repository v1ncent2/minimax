import numpy as np
import time


board = np.zeros((3,3))

def print_board(b):
    print('  a b c')
    for i in range (3):
        print(i, end = ' ')
        for j in range (3):
            if b[i][j] == 0:
                print('-', end = ' ')
            elif b[i][j] == 1:
                print('x', end = ' ')
            elif b[i][j] == -1:
                print('o', end = ' ')
            else:
                print('c', end = ' ')
        print()

def won(b, mark):
    if (b[0][0] != 0) and (b[0][0] == b[0][1]) and (b[0][1] == b[0][2]):
        return (b[0][0] == mark)
    elif (b[1][0] != 0) and (b[1][0] == b[1][1]) and (b[1][1] == b[1][2]):
        return (b[1][0] == mark)
    elif (b[2][0] != 0) and (b[2][0] == b[2][1]) and (b[2][1] == b[2][2]):
        return (b[2][0] == mark)
    elif (b[0][0] != 0) and (b[0][0] == b[1][0]) and (b[1][0] == b[2][0]):
        return (b[0][0] == mark)
    elif (b[0][1] != 0) and (b[0][1] == b[1][1]) and (b[1][1] == b[2][1]):
        return (b[0][1] == mark)
    elif (b[0][2] != 0) and (b[0][2] == b[1][2]) and (b[1][2] == b[2][2]):
        return (b[0][2] == mark)
    elif (b[0][0] != 0) and (b[0][0] == b[1][1]) and (b[1][1] == b[2][2]):
        return (b[0][0] == mark)
    elif (b[0][2] != 0) and (b[0][2] == b[1][1]) and (b[1][1] == b[2][0]):
        return (b[0][2] == mark)
    else:
        return False

def score_unwrap(b, mark, depth, alpha, beta):
    if won(b, -1):
        return -1
    elif won(b, 1):
        return 1
    elif (np.prod(b) != 0):
        return 0
    elif (depth == 0):
        return 0
    else:
        choices = []
        for i in range(3):
            for j in range(3):
                if (b[i][j] == 0):
                    choice = b.copy()
                    choice[i][j] = mark
                    if won(choice, mark): 
                        return mark
                    choices.append(choice)
        if mark == 1:
            curr_max = -1
            for c in choices:
                choice_score = score_unwrap(c, -1, depth-1, alpha, beta)
                curr_max = max(curr_max, choice_score)
                alpha = max(alpha, choice_score)
                if beta <= alpha:
                    break
            return curr_max
        else:
            curr_min = 1
            for c in choices:
                choice_score = score_unwrap(c, 1, depth-1, alpha, beta)
                curr_min = min(curr_min, choice_score)
                beta = min(beta, choice_score)
                if beta <= alpha:
                    break
            return curr_min   

def score(b, mark):
    return score_unwrap(b, mark, 9, -1, 1)

def user_input(mark):
    valid_row = False
    valid_col = False
    row = -1
    col = -1
    while not(valid_row and valid_col):
        uinput = input('Enter: ')
        if (len(uinput) > 1) and (uinput[1] in ['0', '1', '2']):
            valid_row = True
            if uinput[0] == 'a':
                col = 0
                valid_col = True
            elif uinput[0] == 'b':
                col = 1
                valid_col = True
            elif uinput[0] == 'c':
                col = 2
                valid_col = True
            else:
                print('Invalid1. ')
        else:
            print('Invalid2. ')
    row = int(uinput[1])
    if (board[row][col] == 0):
        board[row][col] = mark
    else: 
        print('Invalid3. ')
        user_input(mark)

def ai_input(mark):
    global board
    print('My turn...')
    choices = []
    for i in range(3):
        for j in range(3):
            if (board[i][j] == 0):
                choice = board.copy()
                choice[i][j] = mark
                choices.append(choice)
    best_choice = board.copy()
    if mark == 1:
        curr_max = -1
        for b in choices:
            if score(b, -1) >= curr_max:
                best_choice = b.copy()
                curr_max = score(b, -1)
        board = best_choice.copy()
    else:
        curr_min = 1
        for b in choices:
            if score(b, 1) <= curr_min:
                best_choice = b.copy()
                curr_min = score(b, 1)
        board = best_choice.copy()

while not (won(board, 1) or won(board, -1) or np.prod(board) != 0):
    print_board(board)
    if won(board,-1):
        print('o won')
        break
    if np.prod(board) != 0:
        print('tie')
        break
    print('score ' + str(score(board, 1)))
    ai_input(1)
    time.sleep(1)
    print_board(board)
    if won(board,1):
        print('x won')
        break
    if np.prod(board) != 0:
        print('tie')
        break
    print('score ' + str(score(board, -1)))
    user_input(-1)
    time.sleep(1)
    
