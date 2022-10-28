import random
import re


class Board:

    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        self.board = self.make_new_board()
        self.assign_values_to_board()

        self.dug = set()

    def make_new_board(self):

        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            row = random.randint(0, self.dim_size-1)
            column = random.randint(0, self.dim_size-1)

            if board[row][column] == '*':
                continue

            board[row][column] = '*'
            bombs_planted += 1

        return board

    def assign_values_to_board(self):

        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neigh_bombs(r, c)

    def get_num_neigh_bombs(self, row, column):

        num_neigh_bombs = 0

        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, column-1), min(self.dim_size-1, column+1)+1):

                if r == row and c == column:
                    continue

                if self.board[r][c] == '*':
                    num_neigh_bombs += 1

        return num_neigh_bombs

    def dig(self, row, column):

        self.dug.add((row, column))

        if self.board[row][column] == '*':
            return False
        elif self.board[row][column] > 0:
            return True

        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, column-1), min(self.dim_size-1, column+1)+1):

                if (r, c) in self.dug:
                    continue

                self.dig(r, c)

        return True

    def __str__(self):

        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        for row in range(self.dim_size):
            for column in range(self.dim_size):
                if (row, column) in self.dug:
                    visible_board[row][column] = str(self.board[row][column])
                else:
                    visible_board[row][column] = ' '

        string_rep = ''

        widths = []
        for idx in range(self.dim_size):
            columnumns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columnumns, key = len)
                )
            )

        indices = [i for i in range(self.dim_size)]
        indices_row = '  '
        cells = []
        for idx, column in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (column))
        indices_row += ' '.join(cells)
        indices_row += ' \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, column in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (column))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep

def play(dim_size = 10, num_bombs = 10):

    board = Board(dim_size, num_bombs)

    safe = True

    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        user_input = re.split(',(\\s)*', input("Where would you like you to dig? Input as row,column:"))
        row, column = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or column < 0 or column >= dim_size:
            print('Invalid location. Try again.')
            continue

        safe = board.dig(row, column)
        if not safe:
            break

    if safe:
        print('YOU WIN!')
    else:
        print("GAME OVER:(")
        board.dug = [(r, c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

if __name__ == '__main__':
    play()

#