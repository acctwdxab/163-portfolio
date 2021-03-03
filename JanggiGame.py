# Dan Wu
# 3/2/2021
# Portfolio : Write a class named JanggiGame for playing an abstract board game called Janggi.

from typing import List, Tuple, Any

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


def is_valid_position(row: int, col: int):
    return 0 <= row <= 9 and 0 <= col <= 8


def _in_palace(row: int, col: int):
    if col < 3 or col > 5:
        return False
    return (0 <= row <= 2) or (7 <= row <= 9)


def _parse_square(square: str) -> (int, int):
    return int(square[1:]) - 1, COL_REPR.index(square[0])


class JanggiGame:
    """
    ==== Private Attributes ====
    _turn:
      RED or BLUE, represents whose turn to move
    _board:
      List[List[Piece]] used to store the piece on board
    """

    _turn: int
    _board: List[List[Any]]

    def __init__(self) -> None:
        self._turn = BLUE
        self._board = []
        self._init_board()

    def get_game_state(self) -> str:
        blue_general_exist = self._find_general(BLUE)
        red_general_exist = self._find_general(RED)

        if blue_general_exist and red_general_exist:
            return "UNFINISHED"

        if blue_general_exist:
            return "BLUE_WON"

        return "RED_WON"

    def is_in_check(self, player: str) -> bool:
        """ A general is in check if it could be captured on the opposing
        player's next move.
        """
        if player == 'red':
            general = self._find_general(RED)
            opponent_pieces = self._collect_all_piece(BLUE)
        else:
            general = self._find_general(BLUE)
            opponent_pieces = self._collect_all_piece(RED)

        to_row, to_col = general.get_pos()
        for piece in opponent_pieces:
            if piece.is_valid_move(self._board, to_row, to_col):
                return True
        return False

    def make_move(self, from_square: str,
                  to_square: str) -> bool:
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
        self._turn = RED if self._turn == BLUE else BLUE

    def _collect_all_piece(self, color: int) -> List[Any]:
        pieces = []
        for i in range(NUM_OF_ROW):
            for j in range(NUM_OF_COL):
                if self._board[i][j] \
                        and self._board[i][j].get_color() == color:
                    pieces.append(self._board[i][j])
        return pieces

    def _find_general(self, color: int):
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


class Piece:
    """ Piece of the game, there are seven kinds of pieces in Janggi game,
    every piece has a initial position and initial color which represent the
    player it belongs, and each type of piece has its own rules.

    This class is a abstract class, can not create a usable instance of this
    class.


    """

    _row: int
        """row index of this piece"""
    _col: int
        """column index of this piece"""
    _color: int
        """BLUE or RED, represent which player this piece belongs"""

    def __init__(self, row: int, col: int,
                 color: int) -> None:
        self._row = row
        self._col = col
        self._color = color

    def move_to(self, board: List[List[Any]], to_row: int,
                to_col: int) -> bool:
        if not is_valid_position(to_row, to_col):
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

    def is_valid_move(self, board: List[List[Any]], to_row: int,
                      to_col: int) -> bool:
        raise NotImplementedError

    def get_all_possible_move(self) -> List[List[Tuple]]:
        return [[]]

    def get_color(self) -> int:
        return self._color

    def in_palace(self) -> bool:
        return (0 <= self._row <= 2 or 7 <= self._row <= 9) \
               and 3 <= self._col <= 5

    def get_pos(self):
        return self._row, self._col


# 将
class General(Piece):

    def __init__(self, row: int, col: int, color: int) -> None:
        super().__init__(row, col, color)

    def is_valid_move(self, board: List[List[Any]],
                      to_row: int, to_col: int) -> bool:
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

    def get_all_possible_move(self) -> List[List[Tuple]]:
        return [[(-1, -1)], [(-1, 0)], [(-1, 1)], [(0, 1)],
                [(1, 1)], [(1, 0)], [(1, -1)], [(0, -1)]]


# 士
class Guard(Piece):

    def __init__(self, row: int, col: int, color: int) -> None:
        super().__init__(row, col, color)

    def is_valid_move(self, board: List[List[Any]],
                      to_row: int, to_col: int) -> bool:
        if not is_valid_position(to_row, to_col) \
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

    def get_all_possible_move(self) -> List[List[Tuple]]:
        return [[(-1, -1)], [(-1, 0)], [(-1, 1)], [(0, 1)],
                [(1, 1)], [(1, 0)], [(1, -1)], [(0, -1)]]


# 马
class Horse(Piece):

    def __init__(self, row: int, col: int, color: int) -> None:
        super().__init__(row, col, color)

    def is_valid_move(self, board: List[List[Any]],
                      to_row: int, to_col: int) -> bool:

        for c_m in self.get_all_possible_move():
            r, c = self._row, self._col
            r, c = r + c_m[0][0], c + c_m[0][1]
            # invalid position or hindered by a piece
            if not is_valid_position(r, c) or board[r][c]:
                continue
            r, c = r + c_m[1][0], c + c_m[1][1]
            if r == to_row and c == to_col:
                return True

        return False

    def get_all_possible_move(self) -> List[List[Tuple]]:
        return [[(-1, 0), (-1, -1)], [(-1, 0), (-1, 1)],
                [(0, 1), (-1, 1)], [(0, 1), (1, 1)],
                [(1, 0), (1, 1)], [(1, 0), (1, -1)],
                [(0, -1), (-1, -1)], [(0, -1), (1, -1)]]


# 象
class Elephant(Piece):

    def __init__(self, row: int, col: int, color: int) -> None:
        super().__init__(row, col, color)

    def is_valid_move(self, board: List[List[Any]],
                      to_row: int, to_col: int) -> bool:

        for c_m in self.get_all_possible_move():
            r, c = self._row, self._col
            for m in c_m[:-1]:
                r, c = r + m[0], c + m[1]
                if not is_valid_position(r, c) or board[r][c]:
                    continue
            r, c = r + c_m[-1][0], c + c_m[-1][1]
            if r == to_row and c == to_col:
                return True

        return False

    def get_all_possible_move(self) -> List[List[Tuple]]:
        return [[(-1, 0), (-1, -1), (-1, -1)],
                [(-1, 0), (-1, 1), (-1, 1)],
                [(0, 1), (-1, 1), (-1, 1)],
                [(0, 1), (1, 1), (1, 1)],
                [(1, 0), (1, 1), (1, 1)],
                [(1, 0), (1, -1), (1, -1)],
                [(0, -1), (1, -1), (1, -1)],
                [(0, -1), (-1, -1), (-1, -1)]]


# 车
class Chariot(Piece):

    def __init__(self, row: int, col: int, color: int) -> None:
        super().__init__(row, col, color)

    def is_valid_move(self, board: List[List[Any]],
                      to_row: int, to_col: int) -> bool:
        # same row:
        if self._row == to_row:
            step = 1 if self._col < to_col else -1
            for i in range(self._col+step, to_col, step):
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


# 炮
class Cannon(Piece):

    def __init__(self, row: int, col: int, color: int) -> None:
        super().__init__(row, col, color)

    def is_valid_move(self, board: List[List[Any]],
                      to_row: int, to_col: int) -> bool:
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

        if not self.in_palace() or not _in_palace(to_row, to_col):
            return False

        possible_mov = possible_move_in_palace[(self._row, self._col)]
        if (to_row, to_col) not in possible_mov:
            return False

        if abs(self._row - to_row) < 2:
            return False

        if not board[(self._row + to_row) // 2][(self._col + to_col) // 2]:
            return False

        return True


# 卒
class Soldier(Piece):

    def __init__(self, row: int, col: int, color: int) -> None:
        super().__init__(row, col, color)

    def is_valid_move(self, board: List[List[Any]],
                      to_row: int, to_col: int) -> bool:
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

        if not self.in_palace() or not _in_palace(to_row, to_col):
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


if __name__ == '__main__':
    game = JanggiGame()
    move_result = game.make_move('c1', 'e3')  # should be False because it's not Red's turn
    move_result = game.make_move('a7', 'b7')
    blue_in_check = game.is_in_check('blue')  # should return False
    game.make_move('a4', 'a5')  # should return True
    state = game.get_game_state()  # should return UNFINISHED
    game.make_move('b7', 'b6')  # should return True
    game.make_move('b3', 'b6')  # should return False because it's an invalid move
    game.make_move('a1', 'a4')  # should return True
    game.make_move('c7', 'd7')  # should return True
    game.make_move('a4', 'a4')  # this will pass the Red's turn and return True

