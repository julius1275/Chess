import pygame

pygame.init()

WINDOW_SIZE = (300, 200)
screen = pygame.display.set_mode(WINDOW_SIZE)
font = pygame.font.SysFont('Arial', 30)


def draw_game_over(winner):
    # Game Over Screen
    screen.fill('white')
    winner_text = font.render(f'{winner} wins!', True, 'black')
    screen.blit(winner_text, (50, 50))

    # Play again und Quit buttons
    play_again_text = font.render('Play Again', True, 'black')
    play_again_rect = play_again_text.get_rect(center=(150, 100))
    pygame.draw.rect(screen, 'lightgray', play_again_rect, border_radius=5)
    screen.blit(play_again_text, play_again_rect)

    quit_text = font.render('Quit', True, 'black')
    quit_rect = quit_text.get_rect(center=(150, 150))
    pygame.draw.rect(screen, 'lightgray', quit_rect, border_radius=5)
    screen.blit(quit_text, quit_rect)

    # Game score
    score_text = font.render('Game Score', True, 'black')
    screen.blit(score_text, (50, 180))
    white_score_text = font.render(f'White: {white_score}', True, 'black')
    screen.blit(white_score_text, (150, 180))
    black_score_text = font.render(f'Black: {black_score}', True, 'black')
    screen.blit(black_score_text, (220, 180))

    pygame.display.update()


white_score = 0
black_score = 0


def game_over(winner):
    global white_score, black_score

    draw_game_over(winner)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_again_rect.collidepoint(mouse_pos):
                    # nochmal
                    return True
                elif quit_rect.collidepoint(mouse_pos):
                    # ende
                    pygame.quit()
                    quit()

        pygame.time.wait(10)

    # Game score update
    if winner == 'White':
        white_score += 1
    elif winner == 'Black':
        black_score += 1
