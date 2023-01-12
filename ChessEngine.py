from chess import *
import time
import random

# create board object
board = Board()

# keeps track of how many times eval function is called
evals = 0

# increase MAX_DEPTH to increase depth of search (slower performance)
MAX_DEPTH = 3

# REQUIRES: b is a valid board object
# ENSURES:  prints the 8 x 8 board correctly with unicode symbols

def print_board(b):
    for i in range(64):
        if (i % 8) == 0:
            print()
            print(8 - i//8, end = ' ')
        match str \
              (b.piece_at( \
              SQUARES[int(((63-i) // 8 + 1) * 8 - ((63 - i) % 8 + 1))])):
            case 'r':
                print('♖ ', end = '')
            case 'n':
                print('♘ ', end = '')
            case 'b':
                print('♗ ', end = '')
            case 'q':
                print('♕ ', end = '') 
            case 'k':
                print('♔ ', end = '')
            case 'p':
                print('♙ ', end = '')
            case 'R':
                print('♜ ', end = '')
            case 'N':
                print('♞ ', end = '')
            case 'B':
                print('♝ ', end = '')
            case 'Q':
                print('♛ ', end = '')
            case 'K':
                print('♚ ', end = '')
            case 'P':
                print('♟ ', end = '')
            case default:
                print('. ', end = '')
    print()
    print('  a b c d e f g h ')

# heat map structure
start_map = {
    'P': [  # Pawn
        0,  0,  0,  0,  0,  0,  0,  0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
         5,  5, 10, 25, 25, 10,  5,  5,
         0,  0,  0, 20, 20,  0,  0,  0,
         5, -5,-10,  0,  0,-10, -5,  5,
         5, 10, 10,-20,-20, 10, 10,  5,
         0,  0,  0,  0,  0,  0,  0,  0
    ],
    'N': [  # Knight
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50
    ],
    'B': [  # Bishop
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -20,-10,-10,-10,-10,-10,-10,-20
    ],
   'R': [  # Rook
        0,  0,  0,  0,  0,  0,  0,  0,
         5, 10, 10, 10, 10, 10, 10,  5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
         0,  0,  0,  5,  5,  0,  0,  0
    ],
    'Q': [  # Queen
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5,  5,  5,  5,  0,-10,
         -5,  0,  5,  5,  5,  5,  0, -5,
          0,  0,  5,  5,  5,  5,  0, -5,
        -10,  5,  5,  5,  5,  5,  0,-10,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20
    ],
    'K': [  # King
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -10,-20,-20,-20,-20,-20,-20,-10,
         20, 20,  0,  0,  0,  0, 20, 20,
         20, 30, 10,  0,  0, 10, 30, 20
    ]
}

heat_map = {}

# mirrors heat map for black
for i in start_map:
    heat_map[i] = start_map[i]
    rev_map = start_map[i].copy()
    rev_map.reverse()
    heat_map[i.lower()] = rev_map

# evaluates board structure using both heat map and piece value 
# (divide by 100 for standard chess evaluation)
#
# REQUIRES: b is a valid board object
# ENSURES:  returns the correct board evaluation

def static_eval(b):
    global evals
    evals += 1
    total_score = 0
    for i in range(64):
        match str(b.piece_at(SQUARES[i])):
            case 'R':
                total_score += 500
                total_score += heat_map['R'][i]
            case 'N':
                total_score += 300
                total_score += heat_map['N'][i]
            case 'B':
                total_score += 300
                total_score += heat_map['B'][i]
            case 'Q':
                total_score += 900
                total_score += heat_map['Q'][i]
            case 'P':
                total_score += 100
                total_score += heat_map['p'][i]
            case 'r':
                total_score -= 500
                total_score -= heat_map['r'][i]
            case 'n':
                total_score -= 300
                total_score -= heat_map['n'][i]
            case 'b':
                total_score -= 300
                total_score -= heat_map['b'][i]
            case 'q':
                total_score -= 900
                total_score -= heat_map['q'][i]
            case 'p':
                total_score -= 100
                total_score -= heat_map['p'][i]
            case default:
                total_score += 0
    return total_score

# alpha beta pruning is used here, this is a wrapper function for score
def score_unwrap(b, player, depth, alpha, beta):
    if b.is_stalemate() or b.can_claim_threefold_repetition() or \
       b.is_insufficient_material():
        return 0       
    elif b.is_checkmate():
        if b.result() == '1-0':
            return float('inf')
        else:
            return float('-inf')
    elif (depth == 0):
        return static_eval(b)
    else:
        if player == 'white':
            curr_max = float('-inf')
            for move in b.legal_moves:
                b.push(Move.from_uci(str(move)))
                choice_score = score_unwrap(b, 'black', depth-1, alpha, beta)
                curr_max = max(curr_max, choice_score)
                alpha = max(alpha, choice_score)
                if beta <= alpha:
                    b.pop()
                    break
                b.pop()
            return curr_max
        else:
            curr_min = float('inf')
            for move in b.legal_moves:
                b.push(Move.from_uci(str(move)))
                choice_score = score_unwrap(b, 'white', depth-1, alpha, beta)
                curr_min = min(curr_min, choice_score)
                beta = min(beta, choice_score)
                if beta <= alpha:
                    b.pop()
                    break
                b.pop()
            return curr_min

def score(b, player):
    return score_unwrap(b, player, MAX_DEPTH, float('-inf'), float('inf'))

# makes sure input is in the uci format
def user_input(player):
    choices = []
    for move in board.legal_moves:
        choices.append(move)
    print(choices)
    my_move = input("Enter your move: ")
    try:
        board.push(Move.from_uci(my_move))
    except:
        print("Invalid choice. ")
        user_input(player)

# generates all choices and scores them, picks the one with the highest score
def ai_input(player):
    global board
    global evals
    evals = 0
    print("My turn...")
    choices = []
    for c in board.legal_moves:
        choice = board.copy()
        choice.push(Move.from_uci(str(c)))
        choices.append(choice)
    best_choice = board.copy()
    start = time.time()
    if player == 'white':
        curr_max = float('-inf')
        for b in choices:
            curr_score = score(b, 'black')
            if curr_score >= curr_max:
                best_choice = b.copy()
                curr_max = curr_score
        board = best_choice.copy()
        print(f'score: {curr_max}')
    else: 
        curr_min = float('inf')
        for b in choices:
            curr_score = score(b, 'white')
            if curr_score <= curr_min:
                best_choice = b.copy()
                curr_min = curr_score
        board = best_choice.copy()
        print(f'score: {curr_min}')
    end = time.time()
    print(f'decision took {end - start} seconds')
    print(f'static evaluations: {evals}')
    print(f'kops: {evals / (1000 * (end - start))}')


print_board(board)
print()

# main loop
while True:
    #change to user_input('white') to have user play white
    ai_input('white')
    print_board(board)
    print()
    #change to ai_input('black') to have ai play black
    user_input('black')
    print_board(board)
    print()


