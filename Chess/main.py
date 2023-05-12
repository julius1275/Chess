import pygame

from data.classes.Board import Board

pygame.init()

WINDOW_SIZE = (600, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)

board = Board(WINDOW_SIZE[0], WINDOW_SIZE[1])


def draw(display):
    display.fill('white')
    board.draw(display)
    pygame.display.update()


if __name__ == '__main__':
    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            # Schließt das Spiel wenn auf 'x' gedrückt wird
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Maus clicks
                if event.button == 1:
                    board.handle_click(mx, my)
        if board.is_in_checkmate('black'):  # Schwarz Schachmatt
            print('Weiß gewinnt')
            running = False
        elif board.is_in_checkmate('white'):  # Weiß Schachmatt
            print('Schwarz gewinnt!')
            running = False
        # Erstellt den screen
        draw(screen)
