import random
from typing import List, Dict, Tuple
import copy
"""
This file can be a nice home for your move logic, and to write helper functions.

We have started this for you, with a function to help remove the 'neck' direction
from the list of possible moves!
"""


def avoid_my_neck(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str]) -> List[str]:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'neck' direction removed
    """
    my_neck = my_body[1]  # The segment of body right after the head is the 'neck'

    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        possible_moves.remove("left")
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        possible_moves.remove("right")
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        possible_moves.remove("down")
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        possible_moves.remove("up")

    return possible_moves

def create_empty_board(data_board):
    full_board = []
    for column in range(data_board['width']):
        full_board.append([False] * data_board['height'])
    return full_board

def fill_board_with_snakes(board, data_board):
    for snake in data_board['snakes']:
        for point in snake['body']:
            board[point['x']][point['y']] = True
    for point in data_board['hazards']:
        board[point['x']][point['y']] = True

relative_movement = {
    'up': {'x':0, 'y':1},
    'down': {'x':0, 'y':-1},
    'right': {'x':1, 'y':0},
    'left': {'x':-1, 'y':0},
}

def in_board_limits(board, where_to):
    return not (where_to['x'] < 0 or where_to['x'] >= board['width'] \
        or where_to['y'] < 0 or where_to['y'] >= board['height'])

def remove_immediate_hazards(my_head, board, full_board_data, possible_moves):
    new_possible_moves = []
    for move in possible_moves:
        move_relative_movement = relative_movement[move]
        where_to = {
            "x": my_head['x'] + move_relative_movement['x'],
            "y": my_head['y'] + move_relative_movement['y'],
        }
        if in_board_limits(full_board_data, where_to) and not board[where_to['x']][where_to['y']]:
            new_possible_moves.append(move)


    return new_possible_moves

def remove_next_hazards(my_head, board, full_data, possible_moves, turns=1):
    # TODO The number of next turns should be passed here so this can do every turn with a cache
    # TODO Also the food positions may be necessary
    if turns == 0:
        return possible_moves
    possible_moves = remove_immediate_hazards(my_head, board, full_data['board'], possible_moves)
    new_possible_moves = []
    for move in possible_moves:
        next_possible_moves = ["up", "down", "left", "right"]
        # remove current hazards

        # remove future hazards
        move_relative_movement = relative_movement[move]
        new_head = {
            "x": my_head['x'] + move_relative_movement['x'],
            "y": my_head['y'] + move_relative_movement['y'],
        }
        new_full_data, new_board = get_next_turn_board(new_head, full_data)
        next_possible_moves = remove_next_hazards(new_head, new_board, new_full_data, next_possible_moves, turns-1)
        if next_possible_moves:
            new_possible_moves.append(move)
    return new_possible_moves

def move_player_to(new_head: dict, full_data: dict) -> None:
    for snake in full_data['board']['snakes']:
        if snake['id'] == full_data['you']['id']:
            # TODO check if you are eating
            snake['body'].insert(0, new_head)
            if new_head in full_data['board']['food']:
                index = full_data['board']['food'].index(new_head)
                del full_data['board']['food'][index]
                snake['length'] += 1
            else:
                del snake['body'][-1]
        #TODO check what other snakes do


def get_next_turn_board(new_head:dict, full_data:dict) -> Tuple[dict, dict]:
    # TODO At some point I'll cave in and make this function work correctly
    new_full_data = copy.deepcopy(full_data)
    move_player_to(new_head, new_full_data)
    board = create_empty_board(new_full_data['board'])
    fill_board_with_snakes(board, new_full_data['board'])

    return new_full_data, board 


def get_board_size(board):
    return {
        'width': board['width'],
        'height': board['height']
    }

def distance_between(a, b):
    return (a['x']-b['x'])**2 + (a['y']-b['y'])**2

def weight_by_sum(new_pos, food_data):
    weight = 0
    for food in food_data:
        distance = distance_between(new_pos, food) 
        if not distance:
            # if you can eat... DO IT (yeah it's not optimal I think but whatever)
            weight -= 10000000
        weight += distance_between(new_pos, food)
    return weight

def weight_by_min(new_pos, food_data):
    weight = 1
    if food_data:
        weight = distance_between(new_pos, food_data[0])
    for food in food_data:
        distance = distance_between(new_pos, food) 
        if distance < weight:
            weight = distance
    return weight

def weight_by_max(new_pos, food_data):
    weight = 1
    if food_data:
        weight = distance_between(new_pos, food_data[0])
    for food in food_data:
        distance = distance_between(new_pos, food) 
        if distance > weight:
            weight = distance
    return weight


def weight_for_food(head, possible_moves, food_data, data):
    weighted_possible_moves = []
    for move in possible_moves:
        move_relative_movement = relative_movement[move]
        new_pos = {
            "x": head['x'] + move_relative_movement['x'],
            "y": head['y'] + move_relative_movement['y'],
        }
        if should_get_food_now(data):
            weight = weight_by_min(new_pos, food_data)
        else:
            weight = weight_by_max(new_pos, food_data)

        weighted_possible_moves.append({'move': move, 'weight': weight})

    weighted_possible_moves = sorted(weighted_possible_moves, key= lambda x: x['weight'])
    return [x['move'] for x in weighted_possible_moves]
    
def should_get_food_now(data):
    # We make sure we are the biggest and we are not low on life
    low_on_life = data['you']['health'] < 50
    smol_snake = False
    for snake in data['board']['snakes']:
        if data['you']['length'] <= snake['length'] and snake['id'] != data['you']['id']:
            smol_snake = True
    return low_on_life or smol_snake





def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    board = create_empty_board(data['board'])
    fill_board_with_snakes(board, data['board'])
        
    my_head = data["you"]["head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}

    possible_moves = ["up", "down", "left", "right"]
    possible_moves_next = remove_next_hazards(my_head, board, data, possible_moves, 3)
    if len(possible_moves_next) == 0:
        possible_moves_next = possible_moves

    possible_moves_weighted = weight_for_food(my_head, possible_moves_next, data['board']['food'], data)

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    shout = 'Well I may have a ssssurprise for you'
    if possible_moves_weighted:
        move = possible_moves_weighted[0]
        shout = "It'ssss over my friend"
    else:
        move = 'up'
        shout = "Oh lord ssssspare my life"

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move, shout
