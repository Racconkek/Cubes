import unittest
import configs as c
from Cube import Cube
from Game_logic import GameLogic
import copy
from Game_3 import Game
from arg_parser import ArgParser
from Records_saver import RecordsSaver
from Saver import Saver, SavedInfo
import os
import pickle

def board_generator():
    board = []
    with open("board_template.txt", 'r') as file:
        counter = 0
        for line in file:
            board.append([])
            symbols = list(line)
            for i in range(len(symbols)):
                if symbols[i] == '1':
                    board[counter].append(Cube(i, counter, c.CELL_SIZE, c.BLUE))
                elif symbols[i] == '2':
                    board[counter].append(Cube(i, counter, c.CELL_SIZE, c.GREEN))
                elif symbols[i] == '0':
                    board[counter].append(Cube(i, counter, c.CELL_SIZE, c.WHITE, state=0))
            counter += 1
    return board

class GameLogicTests(unittest.TestCase):

    def test_init_game(self):
        game = GameLogic(c.SMALL, c.INFORMATION_FIELD, c.TIMEOUT, c.CELL_SIZE,
             c.COLORS_COUNT_2)
        self.assertIsNotNone(game.board)
        self.assertIsNotNone(game.font)
        self.assertIsNotNone(game.cubes_to_delete)
        self.assertIsNotNone(game.colors)

    def test_choose_cubes_empty(self):
        game = GameLogic(c.SMALL, c.INFORMATION_FIELD, c.TIMEOUT, c.CELL_SIZE,
                         c.COLORS_COUNT_2)
        chosen = copy.deepcopy(game.colored_cubes)
        game.board = board_generator()
        game.choose_cubes((-1, 0))
        self.assertEqual(chosen, game.colored_cubes)

    def test_choose_cubes_count(self):
        game = GameLogic(c.SMALL, c.INFORMATION_FIELD, c.TIMEOUT, c.CELL_SIZE,
                         c.COLORS_COUNT_2)
        game.board = board_generator()
        game.choose_cubes((20, 0))
        self.assertEqual(10, len(game.colored_cubes))

    def test_choose_cubes_deleted_cubes(self):
        game = GameLogic(c.SMALL, c.INFORMATION_FIELD, c.TIMEOUT, c.CELL_SIZE,
                         c.COLORS_COUNT_2)
        game.board = board_generator()
        game.choose_cubes((20, 0))
        game.choose_cubes((0, 0))
        self.assertEqual(0, len(game.colored_cubes))

    def test_choose_cubes_same_color(self):
        game = GameLogic(c.SMALL, c.INFORMATION_FIELD, c.TIMEOUT, c.CELL_SIZE,
                         c.COLORS_COUNT_2)
        game.board = board_generator()
        game.choose_cubes((20, 0))
        first = len(game.colored_cubes)
        game.choose_cubes((20, 20))
        second = len(game.colored_cubes)
        self.assertEqual(first, second)

    def test_choose_cubes_color_change(self):
        game = GameLogic(c.SMALL, c.INFORMATION_FIELD, c.TIMEOUT, c.CELL_SIZE,
                         c.COLORS_COUNT_2)
        game.board = board_generator()
        game.choose_cubes((20, 0))
        first_length = len(game.colored_cubes)
        first_color = game.current_color
        game.choose_cubes((40, 0))
        second_length = len(game.colored_cubes)
        second_color = game.current_color
        self.assertEqual(first_length, second_length - 1)
        self.assertFalse(first_color == second_color)

    def test_find_chosen_neighbors_empty(self):
        game = GameLogic(c.SMALL, c.INFORMATION_FIELD, c.TIMEOUT, c.CELL_SIZE,
                         c.COLORS_COUNT_2)
        game.board = board_generator()
        result = game.find_chosen_neighbors(-1, -1)
        self.assertEqual(0, len(result))

    def test_find_chosen_neighbors_full(self):
        game = GameLogic(c.SMALL, c.INFORMATION_FIELD, c.TIMEOUT, c.CELL_SIZE,
                         c.COLORS_COUNT_2)
        game.board = board_generator()
        result = game.find_chosen_neighbors(2, 2)
        result = game.find_chosen_neighbors(1, 1)
        self.assertEqual(10, len(result))

    def test_delete_cubes_empty(self):
        game = GameLogic(c.SMALL, c.INFORMATION_FIELD, c.TIMEOUT, c.CELL_SIZE,
                         c.COLORS_COUNT_2)
        game.board = board_generator()
        game.delete_cubes()
        self.assertEqual(0, len(game.colored_cubes))

    def test_delete_cubes_full(self):
        game = GameLogic(c.SMALL, c.INFORMATION_FIELD, c.TIMEOUT, c.CELL_SIZE,
                         c.COLORS_COUNT_2)
        game.board = board_generator()
        game.choose_cubes((40, 20))
        self.assertEqual(11, len(game.colored_cubes))
        game.delete_cubes()
        self.assertEqual(0, len(game.colored_cubes))

    def test_add_points(self):
        game = GameLogic(c.SMALL, c.INFORMATION_FIELD, c.TIMEOUT, c.CELL_SIZE,
                         c.COLORS_COUNT_2)
        game.add_points(4)
        self.assertEqual(2, game.points)

    def test_add_zero_points(self):
        game = GameLogic(c.SMALL, c.INFORMATION_FIELD, c.TIMEOUT, c.CELL_SIZE,
                         c.COLORS_COUNT_2)
        game.add_points(0)
        self.assertEqual(0, game.points)

    def test_need_move_left(self):
        game = GameLogic(c.SMALL, c.INFORMATION_FIELD, c.TIMEOUT, c.CELL_SIZE,
                         c.COLORS_COUNT_2)
        game.board = board_generator()
        result = game.need_move_left()
        self.assertEqual(0, result)

    def test_find_neighbors(self):
        game = GameLogic(c.SMALL, c.INFORMATION_FIELD, c.TIMEOUT, c.CELL_SIZE,
                         c.COLORS_COUNT_2)
        game.board = board_generator()
        result = game.find_neighbors(2, 2, c.BLUE)
        self.assertEqual(11, len(result))

    def test_has_steps(self):
        game = GameLogic(c.SMALL, c.INFORMATION_FIELD, c.TIMEOUT, c.CELL_SIZE,
                         c.COLORS_COUNT_2)
        game.board = board_generator()
        result = game.has_steps()
        self.assertTrue(result)

    def test_update_delete(self):
        game = Game(c.SMALL, c.INFORMATION_FIELD, c.TIMEOUT, c.CELL_SIZE,
                    c.COLORS_COUNT_2, RecordsSaver("records_test.txt"),
                    "Default")
        game.board = board_generator()
        game.choose_cubes((20,20))
        game.delete_cubes()
        game.update()
        self.assertEqual(0, game.board[1][1].state)


class RecordsSaverTests(unittest.TestCase):

    def test_init(self):
        saver = RecordsSaver("records_test.txt")
        self.assertEqual("name", saver.records[0].name)
        self.assertEqual(222, saver.records[0].points)

    def test_add_records(self):
        saver = RecordsSaver("records_test.txt")
        saver.add_records(100, "doctor")
        self.assertEqual("doctor", saver.records[1].name)
        self.assertEqual(100, saver.records[1].points)
        self.restore_records()

    def restore_records(self):
        store = "name 222\nVika 55\nVika 51\nname 43\nhehe 34"
        with open("records_test.txt", "w") as file:
            file.write(store)


class SaverTests(unittest.TestCase):

    def test_save(self):
        Saver.save(SavedInfo(board_generator(), 10), "test_user")
        file_path = os.path.join(os.path.dirname(__file__), 'saves', str("test_user" + '.cube'))
        result = os.path.isfile(file_path)
        self.assertTrue(result)
        os.remove(file_path)

    def test_has_load(self):
        Saver.save(SavedInfo(board_generator(), 10), "test_user")
        file_path = os.path.join(os.path.dirname(__file__), 'saves', str("test_user" + '.cube'))
        result = Saver.load("test_user")
        self.assertEqual(10, result.points)
        os.remove(file_path)

    def test_no_load(self):
        result = Saver.load("test_user")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()