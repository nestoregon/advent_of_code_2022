"""
Solved using branch and bound algorithm.
Keeping a list of alive nodes and having an optimization function to prioritize alive nodes.
"""

from typing import List, Tuple
from dataclasses import dataclass

# TODO: arrows not used
MOVEMENTS_TO_ARROWS = {
    (0, 1): '>',  # right
    (1, 0): 'V',  # down
    (-1, 0): '^',  # up
    (0, -1): '<',  # left
}


@dataclass
class Node:
    x: int
    y: int
    iterations: int
    score: int


def read_input_as_lines(input_path: str) -> List[str]:
    with open(input_path) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    return lines


def get_map_height_from_letter(letter: str) -> int:
    if 'S' == letter: return 0
    if 'E' == letter: return 26
    return ord(letter) - 96


def locate_character(map: List[str], character: str) -> Tuple[int, int]:
    for x in range(len(map)):
        for y in range(len(map[0])):
            if map[x][y] == character:
                return x, y
    raise Exception(f'{character} not found in map')


def initialize_map_copy_with_value(map: List[str], value):
    return [[value for _ in range(len(map[0]))] for _ in range(len(map))]


def sort_nodes_based_on_score(nodes: List[Node], reverse=True) -> List[Node]:
    return sorted(nodes, key=lambda x: x.score, reverse=reverse)


def get_fewest_steps_to_reach_destination(map: List[str], start: str, end: str, uphill: bool):

    # initialize variables
    current_x, current_y = locate_character(map, start)
    value_matrix = initialize_map_copy_with_value(map, value=-1)
    value_matrix[current_x][current_y] = 1  # keeping track of node iteratinos
    min_value = None
    alive_nodes = [Node(current_x, current_y, 1, 1)]  # first node

    # keep looping until there is no more alives nodes
    while len(alive_nodes) > 0:

        # TODO: implement bounding algorithm!
        alive_nodes = sort_nodes_based_on_score(alive_nodes, uphill)
        node = alive_nodes.pop(0)  # check out most promising node!
        height = get_map_height_from_letter(map[node.x][node.y])  # get value of map

        # for each of the 4 directions
        for dx, dy in MOVEMENTS_TO_ARROWS:
            nx = node.x + dx
            ny = node.y + dy

            if nx < 0 or ny < 0 or nx >= len(map) or ny >= len(map[0]):
                continue  # not valid

            if value_matrix[nx][ny] != -1 and value_matrix[nx][ny] <= node.iterations:
                continue  # not valid

            new_height = get_map_height_from_letter(map[nx][ny])
            height_difference = new_height - height

            if uphill and height_difference > 1:
                continue  # We cannot climb more than 1 height

            if not uphill and height_difference < -1:
                continue  # We cannot go down more than 1 height

            value_matrix[nx][ny] = node.iterations

            # are we there yet?
            if map[nx][ny] == end:
                if min_value is None:
                    min_value = node.iterations
                else:
                    min_value = min(min_value, node.iterations)

            alive_nodes.append(
                Node(
                    x=nx,
                    y=ny,
                    iterations=node.iterations + 1,
                    score=new_height,
                )
            )

    return min_value


def main():
    map = read_input_as_lines('input.txt')
    value_uphill = get_fewest_steps_to_reach_destination(
        map,
        start='S',
        end='E',
        uphill=True,
    )

    value_downhill = get_fewest_steps_to_reach_destination(
        map,
        start='E',
        end='a',
        uphill=False,
    )

    print(f'Problem 1: {value_uphill}')
    print(f'Problem 2: {value_downhill}')


if __name__ == '__main__':
    main()
