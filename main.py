import pygame
from board import Board
from game import Game

successes, failures = pygame.init()

WIDTH, HEIGHT = 720, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

board = Board(board_size=(6, 7), board_size_in_pixels=(480, 720), position=(0, 0))
game = Game(board, nplayers=2, X=4)

running = True
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game.finished:
            if game.board.update_board(game.current_player):
                game.next_player()
                game.check_connect()

    if game.finished:
        myfont = pygame.font.SysFont('Comic Sans MS', 50)
        textsurface = myfont.render('Player {} wins'.format(game.winner), False, WHITE)
        screen.blit(textsurface, (WIDTH / 2 - 150, HEIGHT / 2 - 80))
    else:
        board.draw_board(screen)
    pygame.display.update()  # Or pygame.display.flip()
quit()
