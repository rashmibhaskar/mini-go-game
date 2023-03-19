from copy import deepcopy

class OPGO:
    def __init__(self, n):
        self.size = n
        self.X_move = True
        self.died_pieces = [] 
        self.n_move = 0 
        self.max_move = n * n - 1 
        self.komi = n/2 
        self.verbose = False 


    def set_board(self, piece_type, previous_board, board):
        #setting the board, previous board with initial piecetype
        for i in range(self.size):
            for j in range(self.size):
                if previous_board[i][j] == piece_type and board[i][j] != piece_type:
                    self.died_pieces.append((i, j))

        self.previous_board = previous_board
        self.board = board

    def compare_board(self, b1, b2):
        #comparing if 2 boards are the same or not. return false if not equal to each other
        for i in range(self.size):
            for j in range(self.size):
                if b1[i][j] != b2[i][j]:
                    return False
        return True

    def copy_board(self):
        #creating a copy of the board to test without altering the go.board
        return deepcopy(self)

    def detect_neighbor(self, i, j):

        board = self.board
        neighbors = []
        # Detect borders and add neighbor coordinates
        if i > 0: neighbors.append((i-1, j))
        if i < len(board) - 1: neighbors.append((i+1, j))
        if j > 0: neighbors.append((i, j-1))
        if j < len(board) - 1: neighbors.append((i, j+1))
        return neighbors

    def detect_neighbor_ally(self, i, j):
        board = self.board
        neighbors = self.detect_neighbor(i, j)  # Detect neighbors
        group_allies = []
        # Iterate through neighbors
        for piece in neighbors:
            # Add to allies list if having the same color
            if board[piece[0]][piece[1]] == board[i][j]:
                group_allies.append(piece)
        return group_allies

    def ally_dfs(self, i, j):
        stack = [(i, j)]  # stack for DFS serach
        ally_members = []  # record allies positions during the search
        while stack:
            piece = stack.pop()
            ally_members.append(piece)
            neighbor_allies = self.detect_neighbor_ally(piece[0], piece[1])
            for ally in neighbor_allies:
                if ally not in stack and ally not in ally_members:
                    stack.append(ally)
        return ally_members

    def find_liberty(self, i, j):
        board = self.board
        ally_members = self.ally_dfs(i, j)
        for member in ally_members:
            neighbors = self.detect_neighbor(member[0], member[1])
            for piece in neighbors:
                # If there is empty space around a piece, it has liberty
                if board[piece[0]][piece[1]] == 0:
                    return True
        # If none of the pieces in a allied group has an empty space, it has no liberty
        return False

    def find_died_pieces(self, piece_type):
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


    def opp_valid_place_check(self, i, j, piece_type, test_check=False):
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
        

    def update_board(self, new_board):
        self.board = new_board


    def score(self, piece_type):
        #finding the number of stones on the board for a particular piecetype
        board = self.board
        cnt = 0
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == piece_type:
                    cnt += 1
        return cnt  