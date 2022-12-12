"""
Solved using branch and bound algorithm.
Keeping a list of alive nodes and having an optimization function to prioritize alive nodes.
"""

from typing import List, Tuple
from dataclasses import dataclass

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


def get_value_given_letter(letter: str) -> int:
    if 'S' == letter: return 0
    if 'E' == letter: return 26
    return ord(letter) - 96


def locate_character(map: List[str], character: str) -> Tuple[int, int]:
    for x, line in enumerate(map):
        if character not in line:
            continue
        for y in range(len(map[0])):
            if map[x][y] == character:
                return x, y
    raise Exception(f'{character} not found')


def initialize_map(map: List[str], value):
    length_x = len(map)
    length_y = len(map[0])

    visited = []
    for _ in range(length_x):
        row = []
        for _ in range(length_y):
            row.append(value)
        visited.append(row)

    return visited


def sort_nodes(nodes: List[Node], reverse=True) -> List[Node]:
    return sorted(nodes, key=lambda x: x.score, reverse=reverse)


def get_path(map: List[str], start_char: str, end_char: str, uphill: bool):

    # initialize variables
    current_x, current_y = locate_character(map, start_char)
    value_matrix = initialize_map(map, -1)
    starting_node = Node(current_x, current_y, 1, 1)
    alive_nodes = [starting_node]
    value_matrix[current_x][current_y] = 1  # keeping track of node iteratinos
    min_value = None

    # keep looping until there is no more alives nodes
    while len(alive_nodes) > 0:

        # TODO: implement bounding algorithm!
        alive_nodes = sort_nodes(alive_nodes, uphill)  # sorting
        node = alive_nodes.pop(0)  # check out most promising node!
        value = get_value_given_letter(map[node.x][node.y])  # get value of map

        # for each of the 4 directions
        for dx, dy in MOVEMENTS_TO_ARROWS:
            nx = node.x + dx
            ny = node.y + dy

            if nx < 0 or ny < 0 or nx >= len(map) or ny >= len(map[0]):
                continue  # not valid

            if value_matrix[nx][ny] != -1 and value_matrix[nx][ny] <= node.iterations:
                continue  # not valid

            new_value = get_value_given_letter(map[nx][ny])
            diff = new_value - value
            if uphill and diff > 1:
                continue  # not valid
            if not uphill and diff < -1:
                continue  # not valid

            value_matrix[nx][ny] = node.iterations

            # is it the end?
            if map[nx][ny] == end_char:
                if min_value is None:
                    min_value = node.iterations
                else:
                    min_value = min(min_value, node.iterations)

            alive_nodes.append(
                Node(
                    x=nx,
                    y=ny,
                    iterations=node.iterations + 1,
                    score=new_value,
                )
            )

    return min_value


def main():
    map = read_input_as_lines('input.txt')

    value_a = get_path(map, 'S', 'E', uphill=True)
    print(f'Problem 1: {value_a}')

    value_b = get_path(map, 'E', 'a', uphill=False)
    print(f'Problem 2: {value_b}')


if __name__ == '__main__':
    main()
