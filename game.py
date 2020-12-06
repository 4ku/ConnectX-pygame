import numpy as np


class Game:
    def __init__(self, board, nplayers=2, X=4):
        self.board = board
        self.nplayers = nplayers
        self.X = X
        self.current_player = 1
        self.winner = 0
        self.finished = False

    def next_player(self):
        self.current_player = self.current_player % self.nplayers + 1

    def check_connect(self):
        for player in range(self.nplayers):
            win = self.check_player_win(player + 1)
            if win:
                self.finished = True
                self.winner = player + 1
                break

    def check_player_win(self, player):
        X = self.X
        board = self.board

        # horizontal
        for i in range(board.board_height):
            for j in range(board.board_width - X + 1):
                if np.all(board.board[i, j:j + X] == player):
                    return True

        # vertical
        for i in range(board.board_height - X + 1):
            for j in range(board.board_width):
                if np.all(board.board[i:i + X, j] == player):
                    return True

        # diagonal
        for i in range(board.board_height - X + 1):
            for j in range(board.board_width - X + 1):
                el = board.board[i, j]
                flag = True
                for c in range(X):
                    if el != board.board[i + c, j + c] or board.board[i + c, j + c] != player:
                        flag = False
                if flag:
                    return True

        for i in range(X - 1, board.board_height):
            for j in range(board.board_width - X + 1):
                el = board.board[i, j]
                flag = True
                for c in range(X):
                    if el != board.board[i - c, j + c] or board.board[i - c, j + c] != player:
                        flag = False
                if flag:
                    return True

        return False
