import pygame

from data.classes.Square import Square
from data.classes.pieces.Rook import Rook
from data.classes.pieces.Bishop import Bishop
from data.classes.pieces.Knight import Knight
from data.classes.pieces.Queen import Queen
from data.classes.pieces.King import King
from data.classes.pieces.Pawn import Pawn


# Prüft Spiel Status
class Board:
    def __init__(chess, width, height):
        chess.width = width
        chess.height = height
        chess.tile_width = width // 8
        chess.tile_height = height // 8
        chess.selected_piece = None
        chess.turn = 'white'

        # Brett config
        chess.config = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]

        chess.squares = chess.generate_squares()

        chess.setup_board()

    def generate_squares(chess):
        output = []
        for y in range(8):
            for x in range(8):
                output.append(
                    Square(x, y, chess.tile_width, chess.tile_height)
                )
        return output

    def get_square_from_pos(chess, pos):
        for square in chess.squares:
            if (square.x, square.y) == (pos[0], pos[1]):
                return square

    def get_piece_from_pos(chess, pos):
        return chess.get_square_from_pos(pos).occupying_piece

    def setup_board(chess):
        for y, row in enumerate(chess.config):
            for x, piece in enumerate(row):
                if piece != '':
                    square = chess.get_square_from_pos((x, y))

                    # guckt welche Figur wo steht und teilt Farbe zu
                    if piece[1] == 'R':
                        square.occupying_piece = Rook(
                            (x, y), 'white' if piece[0] == 'w' else 'black', chess
                        )
                    # 'chess' wird als Argument angegeben -> Klasse ist board

                    elif piece[1] == 'N':
                        square.occupying_piece = Knight(
                            (x, y), 'white' if piece[0] == 'w' else 'black', chess
                        )

                    elif piece[1] == 'B':
                        square.occupying_piece = Bishop(
                            (x, y), 'white' if piece[0] == 'w' else 'black', chess
                        )

                    elif piece[1] == 'Q':
                        square.occupying_piece = Queen(
                            (x, y), 'white' if piece[0] == 'w' else 'black', chess
                        )

                    elif piece[1] == 'K':
                        square.occupying_piece = King(
                            (x, y), 'white' if piece[0] == 'w' else 'black', chess
                        )

                    elif piece[1] == 'P':
                        square.occupying_piece = Pawn(
                            (x, y), 'white' if piece[0] == 'w' else 'black', chess
                        )

    def handle_click(chess, mx, my):
        x = mx // chess.tile_width
        y = my // chess.tile_height
        clicked_square = chess.get_square_from_pos((x, y))

        if chess.selected_piece is None:
            if clicked_square.occupying_piece is not None:
                if clicked_square.occupying_piece.color == chess.turn:
                    chess.selected_piece = clicked_square.occupying_piece

        elif chess.selected_piece.move(chess, clicked_square):
            chess.turn = 'white' if chess.turn == 'black' else 'black'

        elif clicked_square.occupying_piece is not None:
            if clicked_square.occupying_piece.color == chess.turn:
                chess.selected_piece = clicked_square.occupying_piece

    def is_in_check(chess, color, board_change=None):
        output = False
        king_pos = None

        changing_piece = None
        old_square = None
        new_square = None
        new_square_old_piece = None

        if board_change is not None:
            for square in chess.squares:
                if square.pos == board_change[0]:
                    changing_piece = square.occupying_piece
                    old_square = square
                    old_square.occupying_piece = None
            for square in chess.squares:
                if square.pos == board_change[1]:
                    new_square = square
                    new_square_old_piece = new_square.occupying_piece
                    new_square.occupying_piece = changing_piece

        pieces = [
            i.occupying_piece for i in chess.squares if i.occupying_piece is not None
        ]

        if changing_piece is not None:
            if changing_piece.notation == 'K':
                king_pos = new_square.pos
        if king_pos == None:
            for piece in pieces:
                if piece.notation == 'K' and piece.color == color:
                    king_pos = piece.pos
        for piece in pieces:
            if piece.color != color:
                for square in piece.attacking_squares(chess):
                    if square.pos == king_pos:
                        output = True

        if board_change is not None:
            old_square.occupying_piece = changing_piece
            new_square.occupying_piece = new_square_old_piece

        return output

    def is_in_checkmate(chess, color):
        output = False

        for piece in [i.occupying_piece for i in chess.squares]:
            if piece != None:
                if piece.notation == 'K' and piece.color == color:
                    king = piece

        if king.get_valid_moves(chess) == []:
            if chess.is_in_check(color):
                output = True

        return output

    def draw(chess, display):
        if chess.selected_piece is not None:
            chess.get_square_from_pos(chess.selected_piece.pos).highlight = True
            for square in chess.selected_piece.get_valid_moves(chess):
                square.highlight = True

        for square in chess.squares:
            square.draw(display)
