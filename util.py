from os import path

#read the input file that contains the current board and previous board
def readInput(n, dir="input.txt"):
    with open(dir, 'r') as f:
        lines = f.readlines()
        #read in player type of “1” or “2” indicating which color you play (Black=1, White=2)
        piece_type = int(lines[0])
        #the previous state of the game board (Black=1, White=2, Unoccupied=0) after your last move
        previous_board = []
        for line in lines[1:n+1]:
            tmp = []
            for x in line.rstrip('\n'):
                tmp.append(int(x))
            previous_board.append(tmp)
        #the current state of the game board
        board = []
        for line in lines[n+1: 2*n+1]:
            tmp = []
            for x in line.rstrip('\n'):
                tmp.append(int(x))
            board.append(tmp)
    return piece_type, previous_board, board

#read the output file that contains the next move
def readOutput(dir="output.txt"):
    with open(dir, 'r') as f:
        position = f.readline().strip().split(',')
        #pass a move when a move yields no benefit
        if position[0] == "PASS":
            return "PASS", -1, -1
        #otherwise read the coords to place the chess
        x = int(position[0])
        y = int(position[1])
    return "MOVE", x, y

#write to the output file, either PASS or a coords
def writeOutput(action, result, dir="output.txt"):
    res = ""
    if action == "PASS":
    	res = "PASS"
    elif action == "MOVE":
	    res += str(result[0]) + ',' + str(result[1])
    else:
        res += str(result[0]) + ',' + str(result[1])
        print("TERMINAL")
    with open(dir, 'w') as f:
        f.write(res)

#check if the board is at the initial state (all zeros)
def initialState(board, n):
    for i in range(n):
        for j in range(n):
            if board[i][j] != 0:
                return False
    return True

#read in file that keeps track of n_moves, 1('X') or 2('O')
def readNumMoves(board, n, piece_type, dir="moves.txt"):
    n_moves = -999
    #if the file doesnt exist, we will create one, or initial state of board
    if not path.exists(dir) or initialState(board, n):
        with open(dir, 'w') as f:
            if piece_type == 1:
                n_moves = 0             #current n_moves
            elif piece_type == 2:
                n_moves = 1            #current n_moves
            else:
                print("Wrong piece type")
            _n_moves = n_moves + 2               #n_moves when you next read the file
            f.write(str(_n_moves))
    #if the path/file exists, then we read the current n_moves and rewrite for future read
    else:
        with open(dir, 'r') as f:
            lines = f.readlines()
            n_moves = int(lines[0])
            f.close()
        with open(dir, 'w') as f:
            _n_moves = n_moves + 2
            f.write(str(_n_moves))
    return n_moves
            
            
        
    





















