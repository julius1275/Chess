import pygame


class Piece:
    def __init__(chess, pos, color, board):
        chess.pos = pos
        chess.x = pos[0]
        chess.y = pos[1]
        chess.color = color
        chess.has_moved = False

    def move(chess, board, square, force=False):
        for i in board.squares:
            i.highlight = False

        if square in chess.get_valid_moves(board) or force:
            prev_square = board.get_square_from_pos(chess.pos)
            chess.pos, chess.x, chess.y = square.pos, square.x, square.y

            prev_square.occupying_piece = None
            square.occupying_piece = chess
            board.selected_piece = None
            chess.has_moved = True

            # Bauern umwandlung (Königin)
            if chess.notation == ' ':
                if chess.y == 0 or chess.y == 7:
                    from data.classes.pieces.Queen import Queen
                    square.occupying_piece = Queen(
                        (chess.x, chess.y),
                        chess.color,
                        board
                    )

            # Turm bewegen wenn Rochade
            if chess.notation == 'K':
                if prev_square.x - chess.x == 2:
                    rook = board.get_piece_from_pos((0, chess.y))
                    rook.move(board, board.get_square_from_pos((3, chess.y)), force=True)
                elif prev_square.x - chess.x == -2:
                    rook = board.get_piece_from_pos((7, chess.y))
                    rook.move(board, board.get_square_from_pos((5, chess.y)), force=True)

            return True
        else:
            board.selected_piece = None
            return False

    def get_moves(chess, board):
        output = []
        for direction in chess.get_possible_moves(board):
            for square in direction:
                if square.occupying_piece is not None:
                    if square.occupying_piece.color == chess.color:
                        break
                    else:
                        output.append(square)
                        break
                else:
                    output.append(square)
        return output

    def get_valid_moves(chess, board):
        output = []
        for square in chess.get_moves(board):
            if not board.is_in_check(chess.color, board_change=[chess.pos, square.pos]):
                output.append(square)

        return output

    # True für alle Figuren außer Bauern
    def attacking_squares(chess, board):
        return chess.get_moves(board)
