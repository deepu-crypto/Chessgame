from flask import Flask, request, jsonify
from flask_cors import CORS
from chess import Board, alpha_beta  # Replace with your actual script name

app = Flask(__name__)
CORS(app)

game = Board()

@app.route("/start", methods=["GET"])
def start():
    global game
    game = Board()
    return jsonify({"board": serialize_board(game), "turn": game.turn})

@app.route("/move", methods=["POST"])
def move():
    global game
    data = request.json
    r1, c1, r2, c2 = data["r1"], data["c1"], data["r2"], data["c2"]
    move = ((r1, c1), (r2, c2))
    if move in game.get_all_moves(game.turn):
        game = game.make_move(move)
        return jsonify({
            "board": serialize_board(game),
            "turn": game.turn,
            "gameOver": game.game_over()
        })
    else:
        return jsonify({"error": "Invalid move"}), 400

@app.route("/ai-move", methods=["POST"])
def ai_move():
    global game
    _, move = alpha_beta(game, 3, float('-inf'), float('inf'), False)
    if move:
        game = game.make_move(move)
    return jsonify({
        "board": serialize_board(game),
        "turn": game.turn,
        "gameOver": game.game_over()
    })

@app.route("/legal-moves", methods=["POST"])
def legal_moves():
    global game
    data = request.json
    r, c = data["r"]
    piece = game.board[r][c]
    if piece and piece.color == game.turn:
        moves = game.get_piece_moves(r, c)
        destinations = [m[1] for m in moves]
        return jsonify({"moves": destinations})
    return jsonify({"moves": []})

def serialize_board(board_obj):
    board = []
    for row in board_obj.board:
        board.append([str(piece) if piece else "." for piece in row])
    return board

if __name__ == "__main__":
    app.run(debug=True)