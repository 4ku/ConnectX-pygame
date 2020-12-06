import pygame
import numpy as np

successes, failures = pygame.init()

WIDTH, HEIGHT = 720, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [(255, 255, 255),
          (255, 0, 0),
          (0, 255, 0),
          (0, 0, 255),
          (128, 0, 255)]

NPLAYERS = 2
BOARD_SIZE = (6, 7)
X = 4

CELL_WIDTH = WIDTH / BOARD_SIZE[1]
CELL_HEIGHT = HEIGHT / BOARD_SIZE[0]

RADIUS = min(CELL_WIDTH, CELL_HEIGHT) / 4

current_player = 1
board = np.zeros(BOARD_SIZE).astype('int')

game_finished = False
winner = 0


pygame.font.init()

def draw_board():
    for i in range(BOARD_SIZE[0]):
        for j in range(BOARD_SIZE[1]):
            color = COLORS[board[i][j]]
            x = j * CELL_WIDTH + CELL_WIDTH / 2
            y = i * CELL_HEIGHT + CELL_HEIGHT / 2
            pygame.draw.circle(screen, color, (x, y), RADIUS)


def check_player_win(player):
    # horizontal
    for i in range(BOARD_SIZE[0]):
        for j in range(BOARD_SIZE[1] - X + 1):
            if np.all(board[i, j:j + X] == player):
                return True

    # vertical
    for i in range(BOARD_SIZE[0] - X + 1):
        for j in range(BOARD_SIZE[1]):
            if np.all(board[i:i + X, j] == player):
                return True

    # diagonal
    for i in range(BOARD_SIZE[0] - X + 1):
        for j in range(BOARD_SIZE[1] - X + 1):
            el = board[i, j]
            flag = True
            for c in range(X):
                if el != board[i + c, j + c] or board[i + c, j + c] != player:
                    flag = False
            if flag:
                return True

    for i in range(X-1, BOARD_SIZE[0]):
        for j in range(BOARD_SIZE[1] - X + 1):
            el = board[i, j]
            flag = True
            for c in range(X):
                if el != board[i - c, j + c] or board[i - c, j + c] != player:
                    flag = False
            if flag:
                return True

    return False

board_columns = [pygame.Rect(j * CELL_WIDTH, 0.0, CELL_WIDTH, HEIGHT) for j in range(BOARD_SIZE[1])]

running = True
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game_finished:
            pos = pygame.mouse.get_pos()
            clicked_column_ind = [j for j, column in enumerate(board_columns) if column.collidepoint(pos)]
            if not clicked_column_ind:
                continue
            clicked_column_ind = clicked_column_ind[0]
            clicked_column = board[:, clicked_column_ind]
            ind = 0
            while ind < len(clicked_column) and clicked_column[ind] == 0:
                ind += 1
            if ind != 0:
                board[ind - 1, clicked_column_ind] = current_player
                current_player = current_player % NPLAYERS + 1

            for player in range(NPLAYERS):
                win = check_player_win(player+1)
                if win:
                    game_finished = True
                    winner = player+1
                    break

    if game_finished:
        myfont = pygame.font.SysFont('Comic Sans MS', 50)
        textsurface = myfont.render('Player {} wins'.format(winner), False, WHITE)
        screen.blit(textsurface, (WIDTH/2 - 150, HEIGHT/2 - 80))
    else:
        draw_board()
    pygame.display.update()  # Or pygame.display.flip()

quit()
