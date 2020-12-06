import pygame
import numpy as np

successes, failures = pygame.init()

WIDTH, HEIGHT = 720, 480

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [(255, 255, 255),
          (255, 0, 0),
          (0, 255, 0),
          (0, 0, 255),
          (128, 0, 255)]

NPLAYERS = 2
X = 4

current_player = 1
game_finished = False
winner = 0


class Board:
    def __init__(self, board_size=(6, 7), board_size_in_pixels=(480, 720), position=(0, 0)):
        self.position = position
        self.board_height = board_size[0]
        self.board_width = board_size[1]
        self.board_height_in_pixels = board_size_in_pixels[0]
        self.board_width_in_pixels = board_size_in_pixels[1]

        self.cell_height = board_size_in_pixels[0] / self.board_height
        self.cell_width = board_size_in_pixels[1] / self.board_width
        self.radius = min(self.cell_width, self.cell_height) / 4
        self.board = np.zeros(board_size).astype('int')
        self.board_columns = [pygame.Rect(j * self.cell_width, 0.0, self.cell_width, self.board_height_in_pixels) for j
                              in range(self.board_width)]

    def draw_board(self):
        for i in range(self.board_height):
            for j in range(self.board_width):
                color = COLORS[self.board[i][j]]
                x = self.position[1] + j * self.cell_width + self.cell_width / 2
                y = self.position[0] + i * self.cell_height + self.cell_height / 2
                pygame.draw.circle(screen, color, (x, y), self.radius)

    def column_clicked(self):
        position = pygame.mouse.get_pos()
        clicked_column_ind = [j for j, column in enumerate(self.board_columns) if column.collidepoint(position)]
        print(clicked_column_ind)
        if clicked_column_ind:
            return clicked_column_ind[0]

    def update_board(self):
        clicked_column_ind = self.column_clicked()
        if clicked_column_ind is None:
            return False
        clicked_column = self.board[:, clicked_column_ind]
        ind = 0
        while ind < len(clicked_column) and clicked_column[ind] == 0:
            ind += 1
        if ind != 0:
            self.board[ind - 1, clicked_column_ind] = current_player
            return True
        return False

    def check_player_win(self, player):
        # horizontal
        for i in range(self.board_height):
            for j in range(self.board_width - X + 1):
                if np.all(self.board[i, j:j + X] == player):
                    return True

        # vertical
        for i in range(self.board_height - X + 1):
            for j in range(self.board_width):
                if np.all(self.board[i:i + X, j] == player):
                    return True

        # diagonal
        for i in range(self.board_height - X + 1):
            for j in range(self.board_width - X + 1):
                el = self.board[i, j]
                flag = True
                for c in range(X):
                    if el != self.board[i + c, j + c] or self.board[i + c, j + c] != player:
                        flag = False
                if flag:
                    return True

        for i in range(X - 1, self.board_height):
            for j in range(self.board_width - X + 1):
                el = self.board[i, j]
                flag = True
                for c in range(X):
                    if el != self.board[i - c, j + c] or self.board[i - c, j + c] != player:
                        flag = False
                if flag:
                    return True

        return False


board = Board()

running = True
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game_finished:
            if board.update_board():
                current_player = current_player % NPLAYERS + 1
                for player in range(NPLAYERS):
                    win = board.check_player_win(player + 1)
                    if win:
                        game_finished = True
                        winner = player + 1
                        break

    if game_finished:
        myfont = pygame.font.SysFont('Comic Sans MS', 50)
        textsurface = myfont.render('Player {} wins'.format(winner), False, WHITE)
        screen.blit(textsurface, (WIDTH / 2 - 150, HEIGHT / 2 - 80))
    else:
        board.draw_board()
    pygame.display.update()  # Or pygame.display.flip()

quit()
