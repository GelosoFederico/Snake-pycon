"""
Starter Unit Tests using the built-in Python unittest library.
See https://docs.python.org/3/library/unittest.html

You can expand these to cover more cases!

To run the unit tests, use the following command in your terminal,
in the folder where this file exists:

    python tests.py -v

"""
import unittest

from server_logic import avoid_my_neck, create_empty_board, fill_board_with_snakes

def get_full_test_json():
    return {  "game": {    "id": "game-00fe20da-94ad-11ea-bb37",    "ruleset": {      "name": "standard",      "version": "v.1.2.3"    },    "timeout": 500  },  "turn": 14,  "board": {    "height": 11,    "width": 11,    "food": [      {"x": 5, "y": 5},       {"x": 9, "y": 0},       {"x": 2, "y": 6}    ],    "hazards": [      {"x": 3, "y": 2}    ],    "snakes": [      {        "id": "snake-508e96ac-94ad-11ea-bb37",        "name": "My Snake",        "health": 54,        "body": [          {"x": 0, "y": 0},           {"x": 1, "y": 0},           {"x": 2, "y": 0}        ],        "latency": "111",        "head": {"x": 0, "y": 0},        "length": 3,        "shout": "why are we shouting??",        "squad": ""      },       {        "id": "snake-b67f4906-94ae-11ea-bb37",        "name": "Another Snake",        "health": 16,        "body": [          {"x": 5, "y": 4},           {"x": 5, "y": 3},           {"x": 6, "y": 3},          {"x": 6, "y": 2}        ],        "latency": "222",        "head": {"x": 5, "y": 4},        "length": 4,        "shout": "I'm not really sure...",        "squad": ""      }    ]  },  "you": {    "id": "snake-508e96ac-94ad-11ea-bb37",    "name": "My Snake",    "health": 54,    "body": [      {"x": 0, "y": 0},       {"x": 1, "y": 0},       {"x": 2, "y": 0}    ],    "latency": "111",    "head": {"x": 0, "y": 0},    "length": 3,    "shout": "why are we shouting??",    "squad": ""  }}

class AvoidNeckTest(unittest.TestCase):
    def test_avoid_neck_all(self):
        """
        The possible move set should be all moves.

        In the starter position, a Battlesnake body is 'stacked' in a
        single place, and thus all directions are valid.
        """
        # Arrange
        test_head = {"x": 5, "y": 5}
        test_body = [{"x": 5, "y": 5}, {"x": 5, "y": 5}, {"x": 5, "y": 5}]
        possible_moves = ["up", "down", "left", "right"]

        # Act
        result_moves = avoid_my_neck(test_head, test_body, possible_moves)

        # Assert
        self.assertEqual(len(result_moves), 4)
        self.assertEqual(possible_moves, result_moves)

    def test_avoid_neck_left(self):
        # Arrange
        test_head = {"x": 5, "y": 5}
        test_body = [{"x": 5, "y": 5}, {"x": 4, "y": 5}, {"x": 3, "y": 5}]
        possible_moves = ["up", "down", "left", "right"]
        expected = ["up", "down", "right"]

        # Act
        result_moves = avoid_my_neck(test_head, test_body, possible_moves)

        # Assert
        self.assertEqual(len(result_moves), 3)
        self.assertEqual(expected, result_moves)

    def test_avoid_neck_right(self):
        # Arrange
        test_head = {"x": 5, "y": 5}
        test_body = [{"x": 5, "y": 5}, {"x": 6, "y": 5}, {"x": 7, "y": 5}]
        possible_moves = ["up", "down", "left", "right"]
        expected = ["up", "down", "left"]

        # Act
        result_moves = avoid_my_neck(test_head, test_body, possible_moves)

        # Assert
        self.assertEqual(len(result_moves), 3)
        self.assertEqual(expected, result_moves)

    def test_avoid_neck_up(self):
        # Arrange
        test_head = {"x": 5, "y": 5}
        test_body = [{"x": 5, "y": 5}, {"x": 5, "y": 6}, {"x": 5, "y": 7}]
        possible_moves = ["up", "down", "left", "right"]
        expected = ["down", "left", "right"]

        # Act
        result_moves = avoid_my_neck(test_head, test_body, possible_moves)

        # Assert
        self.assertEqual(len(result_moves), 3)
        self.assertEqual(expected, result_moves)

    def test_avoid_neck_down(self):
        # Arrange
        test_head = {"x": 5, "y": 5}
        test_body = [{"x": 5, "y": 5}, {"x": 5, "y": 4}, {"x": 5, "y": 3}]
        possible_moves = ["up", "down", "left", "right"]
        expected = ["up", "left", "right"]

        # Act
        result_moves = avoid_my_neck(test_head, test_body, possible_moves)

        # Assert
        self.assertEqual(len(result_moves), 3)
        self.assertEqual(expected, result_moves)

class MoveTest(unittest.TestCase):
    def test_create_board(self):
        board = create_empty_board(get_full_test_json()['board'])
        assert len(board) == 11
        for column in board:
            assert len(column) == 11

    def test_fill_board(self):
        board = create_empty_board(get_full_test_json()['board'])
        fill_board_with_snakes(board, get_full_test_json()['board'])
        assert board[0][0] == True
        assert board[1][0] == True
        assert board[2][0] == True
        assert board[5][4] == True
        assert board[5][3] == True
        assert board[6][3] == True
        assert board[6][2] == True
        assert board[3][2] == True


if __name__ == "__main__":
    unittest.main()
