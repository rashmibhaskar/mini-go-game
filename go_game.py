from copy import deepcopy
class GO:
    def __init__(self, n):
        self.size = n
        self.X_move = True
        self.died_pieces = []
        self.n_move = 0
        self.max_move = n * n - 1
        self.komi = n/2
        self.verbose = False

    def set_board(self, piece_type, previous_board, board):
        #setting the board and previous board for a particular piecetype
        for i in range(self.size):
            for j in range(self.size):
                if previous_board[i][j] == piece_type and board[i][j] != piece_type:
                    self.died_pieces.append((i, j))

        self.previous_board = previous_board
        self.board = board

    def compare_board(self, b1, b2):
        #compare if two boards are similar
        for i in range(self.size):
            for j in range(self.size):
                if b1[i][j] != b2[i][j]:
                    return False
        return True

    def copy_board(self):
        return deepcopy(self)

    def detect_neighbor(self, i, j):
        board = self.board
        neighbors = []
        # on the go.board, return neighbours of a position within the board
        if i > 0: neighbors.append((i-1, j))
        if i < len(board) - 1: neighbors.append((i+1, j))
        if j > 0: neighbors.append((i, j-1))
        if j < len(board) - 1: neighbors.append((i, j+1))
        return neighbors

#detect_neighbor
    def detect_neighbor_moves(self, board, i, j):
        neighbors = []
        # on the board that is passed as a parameter, return neighbours of a position within the board
        if i > 0: neighbors.append((i-1, j))
        if i < len(board) - 1: neighbors.append((i+1, j))
        if j > 0: neighbors.append((i, j-1))
        if j < len(board) - 1: neighbors.append((i, j+1))
        return neighbors

    def detect_neighbor_ally(self, i, j):
        #on the go.board, check the allies in neighbouring stones and return those positions for a particular stone
        board = self.board
        neighbors = self.detect_neighbor(i, j)
        allies = []
        # for each position in neighbour
        for x in neighbors:
            # if nrighbour has tha same color as the stone, then add it to allies
            if board[x[0]][x[1]] == board[i][j]:
                allies.append(x)
        return allies

#not there in go
    def detect_neighbor_ally_moves(self, board, i, j):
        #on the board that is passed as the parameter, check the allies in neighbouring stones and return those positions for a particular stone
        neighbors = self.detect_neighbor_moves(board, i, j)
        allies = []
        # for each position in neighbour
        for piece in neighbors:
            # if nrighbour has tha same color as the stone, then add it to allies
            if board[piece[0]][piece[1]] == board[i][j]:
                allies.append(piece)
        return allies

    def ally_dfs(self, i, j):
        #searching for ally stones using DFS
        stack = [(i, j)] 
        allies = []
        while stack:
            piece = stack.pop()
            allies.append(piece)
            neighbor_allies = self.detect_neighbor_ally(piece[0], piece[1])
            for ally in neighbor_allies:
                if ally not in stack and ally not in allies:
                    stack.append(ally)
        return allies

#not in go
    def ally_dfs_moves(self, board, i, j):
        #searching for ally stones using DFS
        stack = [(i, j)]
        allies = []
        while stack:
            piece = stack.pop()
            allies.append(piece)
            neighbor_allies = self.detect_neighbor_ally_moves(board, piece[0], piece[1])
            for ally in neighbor_allies:
                if ally not in stack and ally not in allies:
                    stack.append(ally)
        return allies

    def find_liberty(self, i, j):
        #check if a particular stone has liberty left
        board = self.board
        allies = self.ally_dfs(i, j)
        for x in allies:
            neighbors = self.detect_neighbor(x[0], x[1])
            for y in neighbors:
                if board[y[0]][y[1]] == 0:
                    return True
        return False

#not in go
    def find_liberty_moves(self, board, i, j):
        #check if a particular stone has liberty left
        allies = self.ally_dfs_moves(board, i, j)
        for x in allies:
            neighbors = self.detect_neighbor_moves(board, x[0], x[1])
            for y in neighbors:
                if board[y[0]][y[1]] == 0:
                    return True
        return False

    def find_died_pieces(self, piece_type):
        #find died pieces on the go.board
        board = self.board
        died_pieces = []
        for i in range(len(board)):
            for j in range(len(board)):
                # Check if there is a piece at this position:
                if board[i][j] == piece_type:
                    # The piece die if it has no liberty
                    if not self.find_liberty(i, j):
                        died_pieces.append((i,j))
        return died_pieces

#not in go
    def find_died_pieces_moves(self, board, piece_type):
        #find died pieces on the board passed as a parameter
        died_pieces = []
        for i in range(len(board)):
            for j in range(len(board)):
                # Check if there is a piece at this position:
                if board[i][j] == piece_type:
                    # The piece die if it has no liberty
                    if not self.find_liberty_moves(board, i, j):
                        died_pieces.append((i,j))
        return died_pieces


    def remove_died_pieces(self, piece_type):
        died_pieces = self.find_died_pieces(piece_type)
        if not died_pieces: return []
        self.remove_certain_pieces(died_pieces)
        return died_pieces


    def remove_certain_pieces(self, positions):
        board = self.board
        for piece in positions:
            board[piece[0]][piece[1]] = 0
        self.update_board(board)


    def valid_place_check(self, i, j, piece_type, test_check=False): 
        board = self.board
        verbose = self.verbose
        if test_check:
            verbose = False

        # Check if the place is in the board range
        if not (i >= 0 and i < len(board)):
            return False
        if not (j >= 0 and j < len(board)):
            return False
        
        # Check if the place already has a piece
        if board[i][j] != 0:
            return False
        
        # Copy the board for testing
        test_go = self.copy_board()
        test_board = test_go.board

        # Check if the place has liberty
        test_board[i][j] = piece_type
        test_go.update_board(test_board)
        if test_go.find_liberty(i, j):
            return True

        # If not, remove the died pieces of opponent and check again
        test_go.remove_died_pieces(3 - piece_type)
        if not test_go.find_liberty(i, j):
            return False

        # Check special case: repeat placement causing the repeat board state (KO rule)
        else:
            if self.died_pieces and self.compare_board(self.previous_board, test_go.board):
                return False
        return True

#not in go
    def valid_place_check_moves(self, board, i, j, piece_type, test_check=False):
        verbose = self.verbose
        if test_check:
            verbose = False

        # Check if the place is in the board range
        if not (i >= 0 and i < len(board)):
            return False
        if not (j >= 0 and j < len(board)):
            return False
        
        # Check if the place already has a piece
        if board[i][j] != 0:
            return False
        
        # Copy the board for testing
        test_go = self.copy_board()
        test_board = test_go.board

        # Check if the place has liberty
        test_board[i][j] = piece_type
        test_go.update_board(test_board)
        if test_go.find_liberty(i, j):
            return True

        # If not, remove the died pieces of opponent and check again
        test_go.remove_died_pieces(3 - piece_type)
        if not test_go.find_liberty(i, j):
            return False

        # Check special case: repeat placement causing the repeat board state (KO rule)
        else:
            if self.died_pieces and self.compare_board(self.previous_board, test_go.board):
                return False
        return True
        

    def update_board(self, new_board):  
        self.board = new_board


    def score(self, piece_type):
        board = self.board
        cnt = 0
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == piece_type:
                    cnt += 1
        return cnt