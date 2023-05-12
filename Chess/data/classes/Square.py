import pygame


class Square:
    def __init__(chess, x, y, width, height):
        chess.x = x
        chess.y = y
        chess.width = width
        chess.height = height

        chess.abs_x = x * width
        chess.abs_y = y * height
        chess.abs_pos = (chess.abs_x, chess.abs_y)
        chess.pos = (x, y)
        chess.color = 'light' if (x + y) % 2 == 0 else 'dark'
        chess.draw_color = (213, 213, 200) if chess.color == 'light' else (50, 50, 50)
        chess.highlight_color = (189, 255, 116) if chess.color == 'light' else (0, 228, 10)
        chess.occupying_piece = None
        chess.coord = chess.get_coord()
        chess.highlight = False

        chess.rect = pygame.Rect(
            chess.abs_x,
            chess.abs_y,
            chess.width,
            chess.height
        )

    def get_coord(chess):
        columns = 'abcdefgh'
        return columns[chess.x] + str(chess.y + 1)

    def draw(chess, display):
        if chess.highlight:
            pygame.draw.rect(display, chess.highlight_color, chess.rect)
        else:
            pygame.draw.rect(display, chess.draw_color, chess.rect)

        if chess.occupying_piece != None:
            centering_rect = chess.occupying_piece.img.get_rect()
            centering_rect.center = chess.rect.center
            display.blit(chess.occupying_piece.img, centering_rect.topleft)
