# -*- coding: utf-8 -*-
"""Battle ship game. """

from __future__ import division
import random
import numpy as np

#----------------------------------------------------------------------------------------------

def empty_board(size):
    """Returns a sizexsize matrix filled
    with zeroes.

    >>> empty_board(3)
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    """
    return [size*[0] for _ in range(size)]


def board_size(board):
    """Returns the size of a square board.

    >>> board_size(empty_board(34))
    34
    """
    return len(board[0])


def check(board, step, pos, length):
    """ Checks if a ship of lengtg <length>
    can be done in a line or column of board, iterating
    in the direction <step>, starting from an
    initial position.

    >>> board = empty_board(4)
    >>> check(board, 1, (2, 1), 3)
    True
    >>> check(board, -1, (2, 1), 3)
    False
    >>> check(board, -1, (2, 1), 0)

    """
    row, col = pos
    board_row = board[row][:]
    idx = col
    counter = 0
    while counter < length:
        if idx < 0 or idx > len(board[0])-1:
            return False
        if board_row[idx]:
            return False
        idx += step
        counter += 1
    return True


def transpose(board):
    """ Tansposes a board.

    >>> board = [[1, 3], [2, 4]]
    >>> transpose(board)
    [[1, 2], [3, 4]]
    """
    boardt = []
    for idx  in range(0, board_size(board)):
        column = []
        for row in board:
            column.append(row[idx])
        boardt.append(column)
    return boardt


def check_row_right(board, pos, length):
    """Checks a row to the rigth.
    """
    return 'row', check(board, 1, pos, length), 1


def check_row_left(board, pos, length):
    """Checks a row to the left.
    """
    return 'row', check(board, -1, pos, length), -1


def check_col_right(board, pos, length):
    """Checks a column to the rigth.
    """
    row, col = pos
    new_pos = (col, row)
    return 'col', check(transpose(board), 1, new_pos, length), 1


def check_col_left(board, pos, length):
    """Checks a column to the left.
    """
    row, col = pos
    new_pos = (col, row)
    return 'col', check(transpose(board), -1, new_pos, length), -1


possible_choices = [check_row_right, check_row_left, check_col_right, check_col_left]


def check_positions(board, pos, length):
    """ Returns a list with all the check functions
    and the boolean value that each one returns given the
    input.

    >>> board = empty_board(10)
    >>> pos = (2, 3)
    >>> get_results(board, pos, 4)
    [['row', True, 1], ['row', True, -1], ['col', True, 1], ['col', False, -1]]
    >>> get_results(board, pos, 2)
    [['row', True, 1], ['row', True, -1], ['col', True, 1], ['col', True, -1]]
    """
    functions = []
    for function in possible_choices:
        location, result, step = function(board, pos, length)
        functions.append([location, result, step])
    return functions


def any_True(lst):
    """Given a input that represents a 2D array,
    checks if any of the sub-arrays contains the
    element True. """
    for sub_lst in lst:
        if True in sub_lst:
            return True
    return False


def get_True_options(functions):
    """Given a 2D array, returns another a new
    2D array containing lists with the [0] and [2]
    elements of the sub-lists of the input that
    contained True. """
    true_options = []
    for function in functions:
        if function[1]:
            true_options.append([function[0], function[2]])
    return true_options


class CreateBoard(object):
    def __init__(self, board_size, num_ships, max_length):
        self.board = empty_board(board_size)
        self.num_ships = num_ships
        self.max_length = max_length
        self.board_size = board_size

    def random_empty_spot(self, length, loc=None, startloc=None):
        """Find a random empty spot in from which a ship of
        length <length> can be made.

        >>> board = empty_board(4)
        >>> board[1][1] = 1
        >>> random_empty_spot(board)
        (3, 3)
        >>> print random_empty_spot([[1, 1], [1, 1]])
        None
        """
        board = self.board

        size = board_size(board)
        if startloc is None:
            startloc = random.randint(0, size-1), random.randint(0, size-1)
            loc = startloc
        else:
            if loc == startloc: return None

        pos_options = check_positions(board, loc, length)
        row, col = loc
        if not board[row][col]:
            if any_True(pos_options):
                True_options = random.choice(get_True_options(pos_options))
                return loc, True_options[0], True_options[1]
        if col < size-1:
            return self.random_empty_spot(length, (row, col+1), startloc)
        if row < size-1:
            return self.random_empty_spot(length, (row+1, 0), startloc)
        return self.random_empty_spot(length, (0, 0), startloc)

    def get_random_ship(self, length):
        """ Returns a random ship with length
        <length>"""
        board = self.board
        pos, ship_orientation, step = self.random_empty_spot(length)
        ship = []
        start_row, start_col = pos
        for ship_pos in range(length):
            ship.append((start_row, start_col))
            if ship_orientation is 'row':
                start_col += step
            else:
                start_row += step
        return ship

    def set_ship_on_board(self, ship):
        """ Sets a ship on a board.

        >>> board = empty_board(2)
        >>> set_ship_on_board(board, [(1, 0), (1, 1)])
        [[0, 0], [1, 1]]
        """
        board = self.board
        for pos in ship:
            row, col = pos
            board[row][col] = 1
        #return np.array(board)
        return board

    def set_all_ships(self):
        """ Sets a number of ships <num_ships> of length
        <ships_length> into board.
        """
        board = self.board
        num_ships = self.num_ships
        max_length = self.max_length
        ships = []
        for n in range(num_ships):
            ship = self.get_random_ship(random.randint(1, max_length))
            ships.append(ship)
            board = self.set_ship_on_board(ship)
        print ships, "# this is cheating"
        print '--------------------------------------------------------------------------'
        return ships


def X_empty_board(board):
    """ Receives a board filled with 0 and
    returns a new board filled with X.

    >>> board = empty_board(2)
    >>> X_empty_board(board)
    [['X', 'X'], ['X', 'X']]
    """
    new_board = []
    for row in board:
        new_board.append(['X' for elem in row])
    return new_board


def remove_elem(lst, elem):
    """ Removes an element from a list.

    >>> remove_elem([1, 2, 4], 4)
    [1, 2]
    """
    elem_idx = lst.index(elem)
    return lst[:elem_idx]+lst[elem_idx+1:]


def set_ships_dic(ships):
    """Sets a ships diccionary which keys are strings
    looking like "shipNUM", so each key has in
    its pocket a ship.

    >>> ships = [[(4, 3)], [(3, 3), (2, 3)], [(1, 3), (1, 2), (1, 1), (1, 0)]]
    >>> set_ships_dic(ships)
    {ship0:[(4, 3)], ship1:[(3, 3), (2, 3)], ship2:[(1, 3), (1, 2), (1, 1), (1, 0)]}
    """
    ships_dic = {}
    idx = 0
    for ship in ships:
        ships_dic['ship'+str(idx)] = ship
        idx += 1
    return ships_dic

class BattleShipGame(CreateBoard):
    def __init__(self, board_size, num_ships, max_length):
        CreateBoard.__init__(self, board_size, num_ships, max_length)
        self.play_board = X_empty_board(self.board)
        self.ships_dic = set_ships_dic(self.set_all_ships())

    def update_play_board(self, pos, letter):
        """ Changes the position pos for <letter> in the
        board <play_board>.
        """
        play_board = self.play_board
        row, col = pos
        play_board[row][col] = letter
        return play_board

    def ask(self):
        return raw_input("Enter a position: ")

    def check_answer(self, pos):
        """ Ckecks if the user hite a ship with his
        answer. If he has, removes from the hit ship's
        the hit position. If there aren't any positions left
        in the ship, returns True, None. If there are positions
        left, returns True, False. If any ship has been hit, returns
        False, None.
        """
        ships_dic = self.ships_dic
        for ship in ships_dic:
            if pos in ships_dic[ship]:
                ships_dic[ship] = remove_elem(ships_dic[ship], pos)
                if not ships_dic[ship]:
                    return True, None
                return True, True
        return False, None

    def tuple_answer(self, answer):
        """When the user is asked, he enters a string.
        This function converts this string into a tuple
        which elements are integrers.
        """
        answer = answer.split(', ')
        answer = [int(num) for num in answer]
        return tuple(answer)

    def play_battle_ship(self, play_board=None, ships_dic=None, num_ships=None, hitted=0):
        if play_board is None:
            play_board = self.play_board
            ships_dic = self.ships_dic
            num_ships = self.num_ships

        if hitted == num_ships:
            print
            return 'You win the battle!!'

        answer = self.ask()
        answer = self.tuple_answer(answer)
        if answer[0] > self.board_size or answer[1] > self.board_size:
            print "This board goes from 0 to " + str(self.board_size) + ". Try again:"
            print
            return self.play_battle_ship(play_board, ships_dic, num_ships, hitted)
        succes, ship = self.check_answer(answer)

        if succes is True:
            play_board = self.update_play_board(answer, 'S')
            if ship:
                print 'Ship hit!!'
            else:
                hitted += 1
                print 'You sunk the whole ship!!'

        else:
            play_board = self.update_play_board(answer, 'M')
            print 'Missed'
        print np.array(play_board)
        print
        return self.play_battle_ship(play_board, ships_dic, num_ships, hitted)

#---------------------------------------------------------------------------------------

def _doctest():
    import doctest
    random.seed(0)
    doctest.testmod()

if __name__ == '__main__':
    import sys
    if ('-h' in sys.argv) or ('--help' in sys.argv):
        print __doc__
        sys.exit(1)
    if ('-t' in sys.argv) or ('--test' in sys.argv):
        _doctest()
        sys.exit(1)
    game = BattleShipGame(6, 3, 4)
    print game.play_battle_ship()
    # play_battle_ship()
    # print set_ships_dic([[(3, 5)], [(3, 4), (2, 4), (1, 4), (0, 4)], [(2, 2)]])
    # print remove_elem_from_lst([1, 2, 4], 4)
