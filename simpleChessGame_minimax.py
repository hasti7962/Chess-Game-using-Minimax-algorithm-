import chess
import math

board = chess.Board()
depth = 3  #for minimax algorithm

piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

moves = []  # To save move's sequence

while not board.is_game_over():
    print(board)

    if board.turn:  # White(Human)
        print("Enter your move as two natural numbers (from-to squares):")
        legal_moves = list(board.legal_moves)
        print("Legal moves:")
        for move in legal_moves:
            print(f"{move.from_square} -> {move.to_square}")

        move = None
        while move not in legal_moves:
            try:
                from_square = int(input("From square (0-63): "))
                to_square = int(input("To square (0-63): "))
                move = chess.Move(from_square, to_square)
            except ValueError:
                print("Invalid input. Enter numbers between 0 and 63.")
            if move not in legal_moves:
                print("Illegal move, try again.")
        board.push(move)
        moves.append(f"{len(moves) + 1}. {from_square}->{to_square}")

    else:  # Black(AI)
        print("AI is thinking...")

        best_value = -math.inf
        alpha = -math.inf
        beta = math.inf

        for move in board.legal_moves:
            board.push(move)

            def minimax(board, depth, alpha, beta, maximizing):
                if depth == 0 or board.is_game_over():
                    if board.is_checkmate():
                        return 10000 if board.turn else -10000
                    elif board.is_stalemate() or board.is_insufficient_material():
                        return 0
                    value = 0
                    for piece_type in piece_values:
                        value += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
                        value -= len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]
                    return value

                if maximizing:
                    max_eval = -math.inf
                    for move in board.legal_moves:
                        board.push(move)
                        #Evaluate Move
                        max_eval = max(max_eval, minimax(board, depth - 1, alpha, beta, False))
                        board.pop()
                        alpha = max(alpha, max_eval)
                        if beta <= alpha:
                            break
                    return max_eval
                else:
                    min_eval = math.inf
                    for move in board.legal_moves:
                        board.push(move)
                        min_eval = min(min_eval, minimax(board, depth - 1, alpha, beta, True))
                        board.pop()
                        beta = min(beta, min_eval)
                        if beta <= alpha:
                            break
                    return min_eval

            move_value = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            if move_value > best_value:
                best_value = move_value
                best_move = move

        board.push(best_move)
        moves.append(f"{len(moves) + 1}. AI {best_move.from_square}->{best_move.to_square}")
        print(f"AI plays: {best_move}")

    print("\nMoves so far:")
    for move in moves:
        print(move)

print("Bakhtiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii!")
print(board.result())
