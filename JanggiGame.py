
# 3/10/2021
# Project -  Create a JanggiGame, including the starting position of the pieces, and the 9×10 gameboard.



from typing import List, Any

RED = 1
BLUE = 2
NUM_OF_ROW = 10
NUM_OF_COL = 9
possible_move_in_palace = {
    (0, 3): [(1, 4), (2, 5)],
    (0, 5): [(1, 4), (2, 3)],
    (1, 4): [(0, 3), (0, 5), (2, 3), (2, 5)],
    (2, 3): [(1, 4), (0, 5)],
    (2, 5): [(1, 4), (0, 3)],

    (7, 3): [(8, 4), (9, 5)],
    (7, 5): [(8, 4), (9, 3)],
    (8, 4): [(7, 3), (7, 5), (9, 3), (9, 5)],
    (9, 3): [(8, 4), (7, 5)],
    (9, 5): [(8, 4), (7, 3)],
}
COL_REPR = 'abcdefghi'


def _is_valid_position(row, col):
    """to set the board length and width"""
    return 0 <= row <= 9 and 0 <= col <= 8


def _in_palace(row, col):
    """setting the palace size"""
    if col < 3 or col > 5:
        return False
    return (0 <= row <= 2) or (7 <= row <= 9)


def _parse_square(square):
    """setting the movement rules"""
    return int(square[1:]) - 1, COL_REPR.index(square[0])


class JanggiGame:
    """
    ==== Private Attributes ====
    _turn:
      RED or BLUE, represent whose turn to move
    _board:
      List[List[Piece]] used to store the piece on board
    """

    _turn: int
    _board: List[List[Any]]

    def __init__(self):
        self._turn = BLUE
        self._board = []
        self._init_board()

    def get_game_state(self):
        blue_general_exist = self._find_general(BLUE)
        red_general_exist = self._find_general(RED)

        if blue_general_exist and red_general_exist:
            return "UNFINISHED"

        if blue_general_exist:
            return "BLUE_WON"

        return "RED_WON"

    def is_in_check(self, player):
        """ takes as a parameter either 'red' or 'blue' and returns True if that player is in check,
        but returns False otherwise.
        """
        if player == 'red':
            """if self._turn == RED:
                return False"""
            general = self._find_general(RED)
            opponent_pieces = self._collect_all_piece(BLUE)
        else:
            """if self._turn == BLUE:
                return False"""
            general = self._find_general(BLUE)
            opponent_pieces = self._collect_all_piece(RED)

        to_row, to_col = general.get_pos()
        for piece in opponent_pieces:
            if piece.is_valid_move(self._board, to_row, to_col):
                return True
        return False

    def make_move(self, from_square, to_square):
        """To simulate the movement of pieces, that takes two parameters -
        strings that represent the square to move from and the square to move to."""
        # print(f'{from_square} {to_square}')
        if from_square == to_square:
            self._change_turn()
            return True
        from_row, from_col = _parse_square(from_square)
        # has no piece in from_square
        if not self._board[from_row][from_col]:
            return False

        piece_to_move = self._board[from_row][from_col]
        if piece_to_move.get_color() != self._turn:
            return False

        to_row, to_col = _parse_square(to_square)
        move_result = piece_to_move.move_to(self._board, to_row, to_col)
        if move_result:
            self._change_turn()
        return move_result

    def _change_turn(self):
        """To simulate the turn of players"""
        self._turn = RED if self._turn == BLUE else BLUE

    def _collect_all_piece(self, color):

        pieces = []
        for i in range(NUM_OF_ROW):
            for j in range(NUM_OF_COL):
                if self._board[i][j] \
                        and self._board[i][j].get_color() == color:
                    pieces.append(self._board[i][j])
        return pieces

    def _find_general(self, color):
        start_row = 0 if color == RED else 7
        end_row = 2 if color == RED else 9
        for i in range(start_row, end_row + 1):
            for j in range(3, 6):
                if self._board[i][j] \
                        and isinstance(self._board[i][j], General) \
                        and self._board[i][j].get_color() == color:
                    return self._board[i][j]
        return None

    def _init_board(self):
        """to simulate initiating chariot elephant horse guard general cannon all elements,
        starting position of the pieces, and the 9×10 gameboard."""
        for i in range(NUM_OF_ROW):
            self._board.append([None for i in range(NUM_OF_COL)])

        # init chariot
        self._board[0][0] = Chariot(0, 0, RED)
        self._board[0][8] = Chariot(0, 8, RED)
        self._board[9][0] = Chariot(9, 0, BLUE)
        self._board[9][8] = Chariot(9, 8, BLUE)
        # init elephant
        self._board[0][1] = Elephant(0, 1, RED)
        self._board[0][6] = Elephant(0, 6, RED)
        self._board[9][1] = Elephant(9, 1, BLUE)
        self._board[9][6] = Elephant(9, 6, BLUE)
        # init horse
        self._board[0][2] = Horse(0, 2, RED)
        self._board[0][7] = Horse(0, 7, RED)
        self._board[9][2] = Horse(9, 2, BLUE)
        self._board[9][7] = Horse(9, 7, BLUE)
        # init guard
        self._board[0][3] = Guard(0, 3, RED)
        self._board[0][5] = Guard(0, 5, RED)
        self._board[9][3] = Guard(9, 3, BLUE)
        self._board[9][5] = Guard(9, 5, BLUE)
        # init general
        self._board[1][4] = General(1, 4, RED)
        self._board[8][4] = General(8, 4, BLUE)
        # init Cannon
        self._board[2][1] = Cannon(2, 1, RED)
        self._board[2][7] = Cannon(2, 7, RED)
        self._board[7][1] = Cannon(7, 1, BLUE)
        self._board[7][7] = Cannon(7, 7, BLUE)
        # init soldier
        for i in range(NUM_OF_COL):
            if i % 2 == 0:
                self._board[3][i] = Soldier(3, i, RED)
                self._board[6][i] = Soldier(6, i, BLUE)

    def print_board(self):
        print(f"It's {'Blue' if self._turn == RED else 'Red'} turn.")
        line = "  |"
        for i in range(9):
            line += f"-0{i}-|"
        print(line)
        for row_number, row in zip(range(10), self._board):
            line = f"{row_number} |"
            for p in row:
                line += "-"
                if p is None:
                    line += "NN"
                else:
                    line += p.__str__()
                line += "-|"
            print(line)
        print()


class Piece:
    """ Piece of the game, there are seven kinds of pieces in Janggi game,
    every piece has a initial position and initial color which represent the
    player it belongs, and each type of piece has its own rules
    ==== Private Attributes ====
    _row:
      row number of this piece
    _col:
      column number of this piece
    _color:
      BLUE or RED, represent which player this piece belongs
    """

    _row: int
    _col: int
    _color: int

    def __init__(self, row, col, color):
        self._row = row
        self._col = col
        self._color = color

    def move_to(self, board: List[List[Any]], to_row: int,
                to_col: int) -> bool:
        if not _is_valid_position(to_row, to_col):
            return False

        # can not check your own piece
        if board[to_row][to_col] and \
                board[to_row][to_col].get_color() == self._color:
            return False

        if not self.is_valid_move(board, to_row, to_col):
            return False

        board[to_row][to_col] = self
        board[self._row][self._col] = None
        self._row = to_row
        self._col = to_col
        return True

    def is_valid_move(self, board, to_row, to_col):
        raise NotImplementedError

    def get_all_possible_move(self):
        return [[]]

    def get_color(self):
        return self._color

    def in_same_palace(self, to_row, to_col):
        if not _in_palace(self._row, self._col) or not _in_palace(to_row, to_col):
            return False
        if (0 <= self._row <= 2 and 7 <= to_row <= 9) or \
                (7 <= self._row <= 9 and 0 <= to_row <= 2):
            return False
        return True

    def get_pos(self):
        return self._row, self._col



class General(Piece):
    """The Piece class takes the rank, side, and the position of the piece as
inputs."""
    def __init__(self, row, col, color):
        super().__init__(row, col, color)

    def is_valid_move(self, board, to_row, to_col):
        if not _in_palace(to_row, to_col):
            return False

        # can not leave the palace
        if (self._color == RED and to_row > 2) \
                or (self._color == BLUE and to_row < 7):
            return False

        for m in self.get_all_possible_move():
            if self._row + m[0][0] == to_row and self._col + m[0][1] == to_col:
                return True

        return False

    def get_all_possible_move(self):
        return [[(-1, -1)], [(-1, 0)], [(-1, 1)], [(0, 1)],
                [(1, 1)], [(1, 0)], [(1, -1)], [(0, -1)]]

    def __str__(self):
        return f"G{'R' if self._color == RED else 'B'}"



class Guard(Piece):
    """The Piece class takes the rank, side, and the position of the piece as
  inputs."""
    def __init__(self, row, col, color):
        super().__init__(row, col, color)

    def is_valid_move(self, board, to_row, to_col):
        if not _is_valid_position(to_row, to_col) \
                or not _in_palace(to_row, to_col):
            return False

        # can not leave the palace
        if (self._color == RED and to_row > 2) \
                or (self._color == BLUE and to_row < 7):
            return False

        for m in self.get_all_possible_move():
            if self._row + m[0][0] == to_row and self._col + m[0][1] == to_col:
                return True

        return False

    def get_all_possible_move(self):
        return [[(-1, -1)], [(-1, 0)], [(-1, 1)], [(0, 1)],
                [(1, 1)], [(1, 0)], [(1, -1)], [(0, -1)]]

    def __str__(self):
        return f"S{'R' if self._color == RED else 'B'}"



class Horse(Piece):
    """The Piece class takes the rank, side, and the position of the piece as
  inputs."""
    def __init__(self, row, col, color):
        super().__init__(row, col, color)

    def is_valid_move(self, board, to_row, to_col):

        for c_m in self.get_all_possible_move():
            r, c = self._row, self._col
            r, c = r + c_m[0][0], c + c_m[0][1]
            # invalid position or hindered by a piece
            if not _is_valid_position(r, c) or board[r][c]:
                continue
            r, c = r + c_m[1][0], c + c_m[1][1]
            if r == to_row and c == to_col:
                return True

        return False

    def get_all_possible_move(self):
        return [[(-1, 0), (-1, -1)], [(-1, 0), (-1, 1)],
                [(0, 1), (-1, 1)], [(0, 1), (1, 1)],
                [(1, 0), (1, 1)], [(1, 0), (1, -1)],
                [(0, -1), (-1, -1)], [(0, -1), (1, -1)]]

    def __str__(self):
        return f"H{'R' if self._color == RED else 'B'}"



class Elephant(Piece):
    """The Piece class takes the rank, side, and the position of the piece as
  inputs."""
    def __init__(self, row, col, color):
        super().__init__(row, col, color)

    def is_valid_move(self, board, to_row, to_col):

        for c_m in self.get_all_possible_move():
            r, c = self._row, self._col
            for m in c_m[:-1]:
                r, c = r + m[0], c + m[1]
                if not _is_valid_position(r, c) or board[r][c]:
                    continue
            r, c = r + c_m[-1][0], c + c_m[-1][1]
            if r == to_row and c == to_col:
                return True

        return False

    def get_all_possible_move(self):
        return [[(-1, 0), (-1, -1), (-1, -1)],
                [(-1, 0), (-1, 1), (-1, 1)],
                [(0, 1), (-1, 1), (-1, 1)],
                [(0, 1), (1, 1), (1, 1)],
                [(1, 0), (1, 1), (1, 1)],
                [(1, 0), (1, -1), (1, -1)],
                [(0, -1), (1, -1), (1, -1)],
                [(0, -1), (-1, -1), (-1, -1)]]

    def __str__(self):
        return f"E{'R' if self._color == RED else 'B'}"



class Chariot(Piece):
    """The Piece class takes the rank, side, and the position of the piece as
  inputs."""
    def __init__(self, row, col, color):
        super().__init__(row, col, color)

    def is_valid_move(self, board, to_row, to_col):
        # same row:
        if self._row == to_row:
            step = 1 if self._col < to_col else -1
            for i in range(self._col + step, to_col, step):
                if board[to_row][i]:
                    return False
            return True

        # same column
        if self._col == to_col:
            step = 1 if self._row < to_row else -1
            for i in range(self._row + step, to_row, step):
                if board[i][to_col]:
                    return False
            return True

        if not self.in_same_palace(to_row, to_col):
            return False

        if (self._row, self._col) not in possible_move_in_palace:
            return False

        possible_pos = possible_move_in_palace[(self._row, self._col)]
        if (to_row, to_col) not in possible_pos:
            return False

        if abs(self._row - to_row) < 2:
            return True

        if board[(self._row + to_row) // 2][(self._col + to_col) // 2]:
            return False

        return True

    def __str__(self):
        return f"C{'R' if self._color == RED else 'B'}"



class Cannon(Piece):
    """The Piece class takes the rank, side, and the position of the piece as
  inputs."""
    def __init__(self, row, col, color):
        super().__init__(row, col, color)

    def is_valid_move(self, board, to_row, to_col):
        to_piece = board[to_row][to_col]
        if to_piece and (to_piece.get_color() == self._color
                         or isinstance(to_piece, Cannon)):
            return False

        has_piece_between = False

        if self._row == to_row:
            step = -1 if to_col < self._col else 1
            for i in range(self._col + step, to_col, step):
                if board[to_row][i] and isinstance(board[to_row][i], Cannon):
                    return False
                if not has_piece_between and board[to_row][i]:
                    has_piece_between = True
                    continue
            return has_piece_between

        if self._col == to_col:
            step = -1 if to_row < self._row else 1
            for i in range(self._row + step, to_row, step):
                if board[i][to_col] and isinstance(board[i][to_col], Cannon):
                    return False
                if not has_piece_between and board[i][to_col]:
                    has_piece_between = True
                    continue
            return has_piece_between

        if not self.in_same_palace(to_row, to_col):
            return False

        if (self._row, self._col) not in possible_move_in_palace:
            return False

        possible_mov = possible_move_in_palace[(self._row, self._col)]
        if (to_row, to_col) not in possible_mov:
            return False

        if abs(self._row - to_row) < 2:
            return False

        if not board[(self._row + to_row) // 2][(self._col + to_col) // 2]:
            return False

        return True

    def __str__(self):
        return f"P{'R' if self._color == RED else 'B'}"



class Soldier(Piece):
    """The Piece class takes the rank, side, and the position of the piece as
  inputs."""
    def __init__(self, row, col, color):
        super().__init__(row, col, color)

    def is_valid_move(self, board, to_row, to_col):
        to_piece = board[to_row][to_col]
        if to_piece and to_piece.get_color() == self._color:
            return False

        if self._row == to_row:
            return abs(to_col - self._col) == 1

        if self._col == to_col:
            # can not move backward
            if (self._color == RED and to_row < self._row) or \
                    (self._color == BLUE and to_row > self._row):
                return False

            return abs(to_row - self._row) == 1

        if not self.in_same_palace(to_row, to_col):
            return False

        if (self._row, self._col) not in possible_move_in_palace:
            return False

        possible_mov = possible_move_in_palace[(self._row, self._col)]
        if (to_row, to_col) not in possible_mov:
            return False

        if abs(self._row - to_row) > 1:
            return False

        if (self._color == RED and to_row < self._row) or \
                (self._color == BLUE and to_row > self._row):
            return False

        return True

    def __str__(self):
        return f"Z{'R' if self._color == RED else 'B'}"


if __name__ == '__main__':
    """game = JanggiGame()
    move_result = game.make_move('c1', 'e3')  # should be False because it's not Red's turn
    move_result = game.make_move('a7', 'b7')
    blue_in_check = game.is_in_check('blue')  # should return False
    game.make_move('a4', 'a5')  # should return True
    state = game.get_game_state()  # should return UNFINISHED
    game.make_move('b7', 'b6')  # should return True
    game.make_move('b3', 'b6')  # should return False because it's an invalid move
    game.make_move('a1', 'a4')  # should return True
    game.make_move('c7', 'd7')  # should return True
    game.make_move('a4', 'a4')  # this will pass the Red's turn and return True"""

    game = JanggiGame()
    game.print_board()

    moves = []
    for i in range(19):
        m = input()
        moves.append(m)

    for m in moves:
        ms = m.split(" ")
        game.make_move(ms[0], ms[1])
        game.print_board()
    print("\n")
    print(game.is_in_check('blue'))
