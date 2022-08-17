from chess import *
import time

tot = 0

board = Board()

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

def static_eval(b):
    total_score = 0
    for i in range(64):
        match str(b.piece_at(SQUARES[i])):
            case 'R':
                total_score += 5
            case 'N':
                total_score += 3
            case 'B':
                total_score += 3
            case 'Q':
                total_score += 9
            case 'P':
                total_score += 1
            case 'r':
                total_score -= 5
            case 'n':
                total_score -= 3
            case 'b':
                total_score -= 3
            case 'q':
                total_score -= 9
            case 'p':
                total_score -= 1
            case default:
                total_score += 0
    return total_score

def score_unwrap(b, player, depth, alpha, beta):
    global tot 
    tot += 1
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
        choices = []
        for move in board.legal_moves:
            choice = board.copy()
            choice.push(Move.from_uci(str(move)))
            choices.append(choice)
        if player == 'white':
            curr_max = float('-inf')
            for c in choices:
                choice_score = score_unwrap(c, -1, depth-1, alpha, beta)
                curr_max = max(curr_max, choice_score)
                alpha = max(alpha, choice_score)
                if beta <= alpha:
                    break
            return curr_max
        else:
            curr_min = float('inf')
            for c in choices: 
                choice_score = score_unwrap(c, 1, depth-1, alpha, beta)
                curr_min = min(curr_min, choice_score)
                beta = min(beta, choice_score)
                if beta <= alpha:
                    break
            return curr_min

def score(b, player):
    return score_unwrap(b, player, 3, float('-inf'), float('inf'))

def user_input(player):
    print(board.legal_moves)
    uinput = input('Enter: ')
    board.push_san(str(uinput))   

def ai_input(player):
    global board
    print("My turn...")
    choices = []
    for c in board.legal_moves:
        choice = board.copy()
        choice.push(Move.from_uci(str(c)))
        choices.append(choice)
    best_choice = board.copy()
    if player == 'white':
        curr_max = float('-inf')
        for b in choices:
            print_board(b)
            print(score(b, 'black'))
            if score(b, 'white') >= curr_max:
                best_choice = b.copy()
                curr_max = score(b, 'black')
            board = best_choice.copy()
        print(f'score: {curr_max}')
    else: 
        curr_min = float('inf')
        for b in choices:
            if score(b, 'black') <= curr_min:
                best_choice = b.copy()
                curr_min = score(b, 'white')
        board = best_choice.copy()
        print(f'score: {curr_min}')

print_board(board)
print()
while True:
    user_input('white')
    print_board(board)
    print()
    ai_input('black')
    print_board(board)
    print(f'evals: {tot}')
    print()




