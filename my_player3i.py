import random
import time
import math
from copy import deepcopy
from go_game import *

def readInput(n, path="input.txt"):

    with open(path, 'r') as f:
        lines = f.readlines()

        piece_type = int(lines[0])

        previous_board = [[int(x) for x in line.rstrip('\n')] for line in lines[1:n+1]]
        board = [[int(x) for x in line.rstrip('\n')] for line in lines[n+1: 2*n+1]]

        return piece_type, previous_board, board



def writeOutput(result, path="output.txt"):
    res = ""
    if result == "PASS":
        res = "PASS"
    else:
        res += str(result[0]) + ',' + str(result[1])

    with open(path, 'w') as f:
        f.write(res)



def find_stone_position(board, piece_type):
    #find positions of stones on the board
    placement = []
    for i in range(go.size):
        for j in range(go.size):
            if board[i][j] == piece_type:
                placement.append((i,j))
    return placement



def evaluate(board, color):
    #evaluation function: difference of no. of our stones and no. of opponent's stones
    scoreo, scorex = wins()

    if color == 1:
        score = scorex - scoreo
    if color == 2:
        score = scoreo - scorex
    return score

def wins():
    #return count
    score_of_2 = go.score(2)
    score_of_1 = go.score(1)
    return score_of_2 + go.komi, score_of_1


def find_empty_cell(board,player):
    #check valid moves for a player(go.board)
    possible_placements = []
    for i in range(go.size):
        for j in range(go.size):
            if go.valid_place_check(i, j, player, test_check = True):
                possible_placements.append((i,j))
    random.shuffle(possible_placements)
    return possible_placements

def empty_cells_moves(board,player):
    #check valid moves for a player(board we pass as parameter)
    possible_placements = []
    for i in range(go.size):
        for j in range(go.size):
            if go.valid_place_check_moves(board, i, j, player, test_check = True):
                possible_placements.append((i,j))
    random.shuffle(possible_placements)
    return possible_placements

def opp_find_empty_cell(opgo,board,player):
    #check valid moves for a player(for opponent)
    possible_placements = []
    for i in range(opgo.size):
        for j in range(opgo.size):
            if opgo.valid_place_check(i, j, player, test_check = True):
                possible_placements.append((i,j))
    random.shuffle(possible_placements)
    return possible_placements


def valid_move(x,y,player):
    #check if move is valid
    if (x,y) in find_empty_cell(board,player):
        return True
    else:
        return False

def set_move(board, x, y, player):
    #set the move on the board
    if valid_move(x,y, player):
        go.previous_board = deepcopy(board)
        board[x][y] = player
        go.board = board
        return board
    else:
        return board

def opp_valid_move(opgo, x,y,player):
    #check if move is valid(for opponent)
    if (x,y) in opp_find_empty_cell(opgo,board,player):
        return True
    else:
        return False

def opp_set_move(opgo, board, x, y, player):
    #set the move on the board(for opponent board)
    if opp_valid_move(opgo, x,y, player):
        opgo.previous_board = deepcopy(board)
        board[x][y] = player
        opgo.board = board
        return board
    else:
        return board

def minimax_min_node(board, color, depth, alpha, beta, start_time):
    new_board = deepcopy(board)
    cur_min = math.inf
    moves = find_empty_cell(new_board,color)

    end = time.time()
    if len(moves) == 0 or depth == 0 or end - start_time> 8.5:
        return (-1,-1), evaluate(new_board, color)
    else: 
        for i in moves:
            board_to_pass_each_time = deepcopy(board)
            new_board = set_move(board_to_pass_each_time, i[0], i[1], color)
            go.remove_died_pieces(3 - color)
            if color == 1:
                next_player = 2
            else:
                next_player = 1
            new_move, new_score = minimax_max_node(new_board, next_player, depth - 1, alpha, beta, start_time)
            if new_score < cur_min:
                cur_min = new_score
                best_move = i
            beta = min(new_score, beta) 
            if beta <= alpha:
                break
        return best_move, cur_min 

def minimax_max_node(board, color, depth, alpha, beta, start_time):
    end = time.time()
    new_board = deepcopy(board)
    cur_max = -math.inf
    #get our valid moves
    moves = find_empty_cell(new_board,color)
    #remove moves from valid moves which would be killed by opponent in the next round if they are placed
    stonestoremove = []
    for i in moves:
        go.board[i[0]][i[1]] = color
        opmoves = find_empty_cell(go.board, 3 - color)
        for j in opmoves:
            go.board[j[0]][j[1]] = 3 - color
            deadstones = go.find_died_pieces(color)
            go.board[j[0]][j[1]] = 0
            if i in deadstones:
                if i not in stonestoremove:
                    stonestoremove.append(i)
        go.board[i[0]][i[1]] = 0

    for x in stonestoremove:
        if x in moves:
            moves.remove(x)


    if len(moves) == 0 or depth == 0 or end - start_time> 8.5:
        return (-1,-1), evaluate(new_board, color)
    else: 
        for i in moves:
            board_to_pass_each_time = deepcopy(board)
            new_board = set_move(board_to_pass_each_time, i[0], i[1], color)
            go.remove_died_pieces(3 - color)
            if color == 1:
                next_player = 2
            else:
                next_player = 1
            new_move, new_score = minimax_min_node(new_board, next_player, depth - 1, alpha, beta, start_time)
            if new_score > cur_max:
                cur_max = new_score
                best_move = i
            alpha = max(new_score, alpha) 
            if beta <= alpha:
                break
        return best_move, cur_max

def select_move_minimax(board, color):
    start = time.time()
    best_move, score = minimax_max_node(board, color, max_depth, -math.inf, math.inf, start )
    i, j = best_move[0], best_move[1]

    return i,j, score

def opp_minimax_min_node(opgo,board, color, depth, alpha, beta, start_time):
    new_board = deepcopy(board)

    cur_min = math.inf
    moves = opp_find_empty_cell(opgo, new_board,color)

    end = time.time()
    if len(moves) == 0 or depth == 0 or end - start_time> 8.5:
        return (-1,-1), evaluate(new_board, color)
    else: 
        for i in moves:

            board_to_pass_each_time = deepcopy(board)
            new_board = opp_set_move(opgo,board_to_pass_each_time, i[0], i[1], color)
            opgo.remove_died_pieces(3 - color)
            if color == 1:
                next_player = 2
            else:
                next_player = 1
            new_move, new_score = opp_minimax_max_node(opgo,new_board, next_player, depth - 1, alpha, beta, start_time)
            if new_score < cur_min:
                cur_min = new_score
                best_move = i
            beta = min(new_score, beta) 
            if beta <= alpha:
                break
        return best_move, cur_min 

def opp_minimax_max_node(opgo, board, color, depth, alpha, beta, start_time):
    end = time.time()
    new_board = deepcopy(board)
    # board_to_pass_each_time = deepcopy(board)
    cur_max = -math.inf
    moves = opp_find_empty_cell(opgo, new_board,color)

    if len(moves) == 0 or depth == 0 or end - start_time> 8.5:
        return (-1,-1), evaluate(new_board, color)
    else: 
        for i in moves:

            board_to_pass_each_time = deepcopy(board)
            new_board = opp_set_move(opgo,board_to_pass_each_time, i[0], i[1], color)
            opgo.remove_died_pieces(3 - color)
            if color == 1:
                next_player = 2
            else:
                next_player = 1
            new_move, new_score = opp_minimax_min_node(opgo,new_board, next_player, depth - 1, alpha, beta, start_time)
            if new_score > cur_max:
                cur_max = new_score
                best_move = i
            alpha = max(new_score, alpha) 
            if beta <= alpha:
                break
        return best_move, cur_max


def opp_select_move_minimax(opgo, board, color):
    start = time.time()
    best_move, score = opp_minimax_max_node(opgo, board, color, max_depth_opponent, -math.inf, math.inf, start )
    i, j = best_move[0], best_move[1]

    return i,j, score




def retrieve_action(go, piece_type):   
    empty_spaces = []
    for i in range(go.size):
        for j in range(go.size):
            if go.board[i][j] == 0:
                empty_spaces.append((i,j))

    killcount = dict()
    for i in empty_spaces:
        go.board[i[0]][i[1]] = piece_type
        died_pieces = go.find_died_pieces(3-piece_type)
        go.board[i[0]][i[1]] = 0
        if len(died_pieces) >= 1:
            killcount[i] = len(died_pieces)

    sorted_killcount = sorted(killcount, key = killcount.get, reverse = True)

    for i in sorted_killcount:
        testboard = deepcopy(go.board)
        testboard[i[0]][i[1]] = piece_type
        died_stone = go.find_died_pieces_moves(testboard, 3 - piece_type)
        for x in died_stone:
            testboard[x[0]][x[1]] = 0
        if i !=None and go.previous_board != testboard:
            return i
    

    ####################################################################################################################################
    #MOVES TO REMOVE 
    ####################################################################################################################################
    moves = find_empty_cell(go.board,piece_type)

    moves_to_remove = []
    for i in moves:
        go.board[i[0]][i[1]] = piece_type
        oppmove = empty_cells_moves(go.board, 3-piece_type)
        for j in oppmove:
            go.board[j[0]][j[1]] = 3 - piece_type
            died_pieces = go.find_died_pieces(piece_type)
            go.board[j[0]][j[1]] = 0
            if i in died_pieces:
                moves_to_remove.append(i)
        go.board[i[0]][i[1]] = 0

    for x in moves_to_remove:
        if x in moves:
            moves.remove(x)

    if len(moves) == 0:
        return "PASS"
    ####################################################################################################################################
    #DEFENSE
    ####################################################################################################################################

    save_moves = dict()
    opponent_moves = []
    for i in range(go.size):
        for j in range(go.size):
            if go.board[i][j] == 0:
                opponent_moves.append((i,j))

    for i in opponent_moves:
        go.board[i[0]][i[1]] = 3-piece_type
        our_dead_stones = go.find_died_pieces(piece_type)
        go.board[i[0]][i[1]] = 0
        if len(our_dead_stones) >=1:
            save_moves[i] = len(our_dead_stones)

    sorted_save_moves = sorted(save_moves, key = save_moves.get, reverse = True)


    for i in sorted_save_moves:
        if i != None and i in moves:
            return i

    ####################################################################################################################################

    position_of_opponent = find_stone_position(go.board, 3-piece_type)
    empty_x = []
    neighbours = []

    for i in position_of_opponent:
        neighbors = [(i[0]+board[0], i[1]+board[1]) for board in 
                    [(-1,0), (1,0), (0,-1), (0,1)] 
                    if ( (0 <= i[0]+board[0] < go.size) and (0 <= i[1]+board[1] < go.size))]
        for x in neighbors:
            neighbours.append(x)


    #now we check if the neighbours are empty and add them in a list
    for i in neighbours:
        if board[i[0]][i[1]]==0:
            empty_x.append(i)
    
    #now we place our moves, and check for change in the opponent's liberties
    for x in moves:
        #place our move
        testboard = deepcopy(go.board)
        testboard[x[0]][x[1]] = piece_type
        #remove died pieces if any
        died_stone = go.find_died_pieces_moves(testboard, 3 - piece_type)
        for m in died_stone:
            testboard[m[0]][m[1]] = 0
        #now check the liberty of the opponent
        position_of_opponent = find_stone_position(testboard, 3 - piece_type)
        empty_y = []
        neighbours = []

        for i in position_of_opponent:
            neighbors = [(i[0]+board[0], i[1]+board[1]) for board in 
                        [(-1,0), (1,0), (0,-1), (0,1)] 
                        if ( (0 <= i[0]+board[0] < go.size) and (0 <= i[1]+board[1] < go.size))]
            for n in neighbors:
                neighbours.append(n)

        for z in neighbours:
            if board[z[0]][z[1]] == 0:
                empty_y.append(z)

        if len(empty_x) - len(empty_y) >=1:
            return x

    ####################################################################################################################################
    #INITIAL MOVES 
    ####################################################################################################################################

    if len(moves) >= 15:
        if (2,2) in moves:
            return (2,2)
        if (1,1) in moves:
            return (1,1)
        if (1,3) in moves:
            return (1,3)
        if (3,1) in moves:
            return (3,1)
        if (3,3) in moves:
            return (3,3)
        if (2,0) in moves:
            return (2,0)
        if (2,4) in moves:
            return (2,4)
        if (0,2) in moves:
            return (0,2)
        if (4,2) in moves:
            return (4,2)

    ####################################################################################################################################
    #OPPONENT'S MOVE USING MINMAX AND PLAY ACCORDINGLY
    ####################################################################################################################################
        
    opp_board = deepcopy(go.board)
    opp_previous_board = deepcopy(go.previous_board)

    opgo = GO(5)
    opgo.set_board(3-piece_type, opp_previous_board, opp_board)

    movei, movej, score = opp_select_move_minimax(opgo, opp_board, 3-piece_type)
    x, y = movei, movej
    go.board[x][y] = 3 - piece_type

    empty_spaces = []
    for i in range(go.size):
        for j in range(go.size):
            if go.board[i][j] == 0:
                empty_spaces.append((i,j))


    killcount = dict()
    for i in empty_spaces:
        go.board[i[0]][i[1]] = piece_type
        died_pieces = go.find_died_pieces(3-piece_type)
        go.board[i[0]][i[1]] = 0
        if len(died_pieces) >= 1:
            print('taking out more than 1 opponents')
            killcount[i] = len(died_pieces)

    killcount_remove = []
    sorted_killcount = sorted(killcount, key = killcount.get, reverse = True)
    go.board[x][y] = 0

    if len(sorted_killcount) != 0:
        for i in sorted_killcount:
            go.board[i[0]][i[1]] == piece_type
            opmoves = empty_cells_moves(go.board, 3- piece_type)
            for j in opmoves:
                go.board[j[0]][j[1]] = 3 - piece_type
                died_pieces = go.find_died_pieces_moves(go.board, piece_type)
                go.board[j[0]][j[1]] = 0
                if i in died_pieces:
                    killcount_remove.append(i)
            go.board[i[0]][i[1]] = 0

        for x in killcount_remove:
            if x in sorted_killcount:
                sorted_killcount.remove(x)


        for i in sorted_killcount:
            if i in moves:
                return i

    ####################################################################################################################################
    #MINMAX
    ####################################################################################################################################

    movei, movej, score = select_move_minimax(go.board, piece_type)
    x, y = movei, movej
    return(x,y)



N = 5
max_depth = 4
max_depth_opponent = 1
piece_type, previous_board, board = readInput(N)
go = GO(N)
go.set_board(piece_type, previous_board, board)
action = retrieve_action(go, piece_type)
print(action,"jkjkjk")
if action == None:
    action = "PASS"
writeOutput(action)