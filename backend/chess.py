import copy

# Constants
EMPTY = '.'
WHITE = 'W'
BLACK = 'B'

# Piece values for evaluation
eval_values = {
    'K': 1000,  # King is highly valuable
    'Q': 9,
    'R': 5,
    'B': 3,
    'N': 3,
    'P': 1
}

class Piece:
    def __init__(self, color, type_):
        self.color = color
        self.type = type_  # 'K', 'Q', 'R', 'B', 'N', 'P'

    # def __str__(self):
    #     return self.color + self.type

    def __str__(self):
        symbols = {
            'K': {'W': '♔', 'B': '♚'},
            'Q': {'W': '♕', 'B': '♛'},
            'R': {'W': '♖', 'B': '♜'},
            'B': {'W': '♗', 'B': '♝'},
            'N': {'W': '♘', 'B': '♞'},
            'P': {'W': '♙', 'B': '♟︎'}
        }
        return symbols[self.type][self.color]    

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.init_pieces()
        self.turn = WHITE

    def init_pieces(self):
        # Place White pieces
        self.board[7][4] = Piece(WHITE, 'K')
        self.board[7][3] = Piece(WHITE, 'Q')
        self.board[7][0] = Piece(WHITE, 'R')
        self.board[7][7] = Piece(WHITE, 'R')
        self.board[7][2] = Piece(WHITE, 'B')
        self.board[7][5] = Piece(WHITE, 'B')
        self.board[7][1] = Piece(WHITE, 'N')
        self.board[7][6] = Piece(WHITE, 'N')

        for i in range(8):
            self.board[6][i] = Piece(WHITE, 'P')

        # Place Black pieces
        self.board[0][4] = Piece(BLACK, 'K')
        self.board[0][3] = Piece(BLACK, 'Q')
        self.board[0][0] = Piece(BLACK, 'R')
        self.board[0][7] = Piece(BLACK, 'R')
        self.board[0][2] = Piece(BLACK, 'B')
        self.board[0][5] = Piece(BLACK, 'B')
        self.board[0][1] = Piece(BLACK, 'N')
        self.board[0][6] = Piece(BLACK, 'N')

        for i in range(8):
            self.board[1][i] = Piece(BLACK, 'P')

    def print_board(self):
        for row in self.board:
            print(' '.join(str(cell) if cell else EMPTY for cell in row))
        print()

    def get_all_moves(self, color):# to find all legal moves for a particular peice helpful for expanding the game tree
        moves = []
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece and piece.color == color:
                    moves.extend(self.get_piece_moves(r, c))
        return moves
    
    def is_in_check(self, color):
        # Find king position
        king_pos = None
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece and piece.color == color and piece.type == 'K':
                    king_pos = (r, c)
                    break
        if not king_pos:
            return True  # No king? already captured

        # Check if opponent can move to king's position
        opponent_color = BLACK if color == WHITE else WHITE
        opponent_moves = self.get_all_moves(opponent_color)
        return any(move[1] == king_pos for move in opponent_moves)
    
    def game_over(self):
        white_king = any(
            piece for row in self.board for piece in row
            if piece and piece.color == WHITE and piece.type == 'K'
        )
        black_king = any(
            piece for row in self.board for piece in row
            if piece and piece.color == BLACK and piece.type == 'K'
        )

        if not white_king:
            return "checkmate"  # Black wins
        if not black_king:
            return "checkmate"  # White wins

        legal_moves = self.get_all_moves(self.turn)
        if not legal_moves:
            if self.is_in_check(self.turn):
                return "checkmate"
            else:
                return "stalemate"

        return None

    def get_piece_moves(self, r, c):#setting move directions for each peice as per rules
        piece = self.board[r][c]
        moves = []
        if piece.type == 'P':
            direction = -1 if piece.color == WHITE else 1
            if 0 <= r + direction < 8:
                if self.board[r + direction][c] is None:
                    moves.append(((r, c), (r + direction, c)))
                for dc in [-1, 1]:
                    nc = c + dc
                    if 0 <= nc < 8 and self.board[r + direction][nc] and self.board[r + direction][nc].color != piece.color:
                        moves.append(((r, c), (r + direction, nc)))

        elif piece.type == 'Q':
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                          (-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                while 0 <= nr < 8 and 0 <= nc < 8:
                    if self.board[nr][nc] is None:
                        moves.append(((r, c), (nr, nc)))
                    elif self.board[nr][nc].color != piece.color:
                        moves.append(((r, c), (nr, nc)))
                        break
                    else:
                        break
                    nr += dr
                    nc += dc

        elif piece.type == 'K':
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        if self.board[nr][nc] is None or self.board[nr][nc].color != piece.color:
                            moves.append(((r, c), (nr, nc)))

        elif piece.type == 'R':
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                while 0 <= nr < 8 and 0 <= nc < 8:
                    if self.board[nr][nc] is None:
                        moves.append(((r, c), (nr, nc)))
                    elif self.board[nr][nc].color != piece.color:
                        moves.append(((r, c), (nr, nc)))
                        break
                    else:
                        break
                    nr += dr
                    nc += dc

        elif piece.type == 'B':
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                while 0 <= nr < 8 and 0 <= nc < 8:
                    if self.board[nr][nc] is None:
                        moves.append(((r, c), (nr, nc)))
                    elif self.board[nr][nc].color != piece.color:
                        moves.append(((r, c), (nr, nc)))
                        break
                    else:
                        break
                    nr += dr
                    nc += dc

        elif piece.type == 'N':
            knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                            (1, -2), (1, 2), (2, -1), (2, 1)]
            for dr, dc in knight_moves:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    if self.board[nr][nc] is None or self.board[nr][nc].color != piece.color:
                        moves.append(((r, c), (nr, nc)))

        return moves

    def make_move(self, move):
        (r1, c1), (r2, c2) = move
        new_board = copy.deepcopy(self)
        new_board.board[r2][c2] = new_board.board[r1][c1]
        new_board.board[r1][c1] = None
        new_board.turn = BLACK if self.turn == WHITE else WHITE
        return new_board

    def evaluate(self):
        score = 0
        for row in self.board:
            for piece in row:
                if piece:
                    value = eval_values[piece.type]
                    score += value if piece.color == WHITE else -value
        return score

# Alpha-Beta Pruning
#intially check if game is completed or Depth limit is reached.
#find all legal moves for whites and black
# For white maximizing score
    #intially max_eval is considered big negative because we want to find maximum score
    #we will be calling alpha beta recursively to take deeper moves,so at every move reult is better we remember that move.update alpha with best move found
#For black minimizing score
     #intially min_eval is considered big npositive because we want to find maximum score
    #we will be calling alpha beta recursively to take deeper moves,so at every move result is better we remember that move.update beta with best move found
#if beta becomes small or equal at any time we cut the search(prune) to save time

def alpha_beta(board, depth, alpha, beta, maximizing_player):
    white_king = any(piece for row in board.board for piece in row if piece and piece.color == WHITE and piece.type == 'K')
    black_king = any(piece for row in board.board for piece in row if piece and piece.color == BLACK and piece.type == 'K')

    if not white_king:
        return -10000, None
    if not black_king:
        return 10000, None
    if depth == 0:
        return board.evaluate(), None

    best_move = None
    all_moves = board.get_all_moves(WHITE if maximizing_player else BLACK)

    all_moves.sort(key=lambda m: 0 if board.board[m[1][0]][m[1][1]] else 1)

    if maximizing_player:
        max_eval = float('-inf')
        for move in all_moves:
            new_board = board.make_move(move)
            eval, _ = alpha_beta(new_board, depth - 1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move

    else:
        min_eval = float('inf')
        for move in all_moves:
            new_board = board.make_move(move)
            eval, _ = alpha_beta(new_board, depth - 1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

if __name__ == "__main__":
    b = Board()
    b.print_board()

    while True:
        if b.turn == WHITE:
            print("Your move!  state current position and future position you want to move")
            try:
                move_input = input("Enter your move (r1 c1 r2 c2): ")
                r1, c1, r2, c2 = map(int, move_input.strip().split())
                possible_moves = b.get_all_moves(WHITE)
                if ((r1, c1), (r2, c2)) in possible_moves:
                    b = b.make_move(((r1, c1), (r2, c2)))
                else:
                    print("Invalid move. Try again.")
                    continue
            except Exception:
                print("Invalid input. Try again.")
                continue

        else:
            print("random player turn")
            _, move = alpha_beta(b, 3, float('-inf'), float('inf'), False)
            if move is None:
                print("random player has no moves! You win!")
                break
            b = b.make_move(move)

        b.print_board()

        white_king = any(piece for row in b.board for piece in row if piece and piece.color == WHITE and piece.type == 'K')
        black_king = any(piece for row in b.board for piece in row if piece and piece.color == BLACK and piece.type == 'K')

        if not white_king:
            print("You lost! \U0001F480")
            break
        if not black_king:
            print("You won! \U0001F389")
            break   