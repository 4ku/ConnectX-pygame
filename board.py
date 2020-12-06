import pygame
import numpy as np

COLORS = [(255, 255, 255),
          (255, 0, 0),
          (0, 255, 0),
          (0, 0, 255),
          (128, 0, 255)]


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

    def draw_board(self, screen):
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

    def update_board(self, current_player):
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
