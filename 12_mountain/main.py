from typing import List, Tuple
from dataclasses import dataclass

MOVEMENTS_TO_ARROWS = {
    (0, 1): '>',  # right
    (1, 0): 'V',  # down
    (-1, 0): '^',  # up
    (0, -1): '<',  # left
}


def get_distance_to_end(cx, cy, ex, ey):
    return abs(ex - cx) + abs(ey - cy)


def get_value_given_letter(letter: str) -> int:
    if 'S' == letter: return 0
    if 'E' == letter: return 26
    return ord(letter) - 96


@dataclass
class Node:
    x: int
    y: int
    iterations: int
    score: int

    def set_node_score(self, map: List[str], ex: int, ey: int):
        """Mix between how high you are and the distance to the end"""
        distance = get_distance_to_end(self.x, self.y, ex, ey)
        value = self.get_value_height(map)
        self.score = max([distance, value])

    def get_value_height(self, map):
        return 26 - get_value_given_letter(map[self.x][self.y])

    def get_node_optimistic(self, map: List[str], ex: int, ey: int) -> int:
        """Mix between how high you are and the distance to the end"""
        distance = get_distance_to_end(self.x, self.y, ex, ey)
        value = self.get_value_height(map)
        return min([distance, value])

    def set_node_score_height(self, height):
        self.score = height


def read_input_as_lines(input_path: str) -> List[str]:
    with open(input_path) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    return lines


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


def sort_nodes(nodes: List[Node], map: List[str], ex, ey) -> List[Node]:
    for node in nodes:
        node.set_node_score(map, ex, ey)
    return sorted(nodes, key=lambda x: x.score)


def sort_node_inverse(nodes, map):
    for node in nodes:
        node.set_node_score_height(map[node.x][node.y])
    return sorted(nodes, key=lambda x: x.score)


def remove_nodes(nodes: List[Node], map, value_matrix: List[List[int]], ex, ey):
    alive_nodes = []
    target = value_matrix[ex][ey]

    for node in nodes:
        if node.get_node_optimistic(map, ex, ey) < target:
            alive_nodes.append(node)

    return alive_nodes


def get_path_inverse(map: List[str]):
    sx, sy = locate_character(map, 'E')
    value_matrix = initialize_map(map, -1)

    cx, cy = sx, sy

    starting_node = Node(cx, cy, 1, -1)
    alive_nodes = [starting_node]
    value_matrix[cx][cy] = 1
    lowest_score = 100_000_000

    while len(alive_nodes) > 0:

        alive_nodes = sort_node_inverse(alive_nodes, map)

        # alive_nodes = remove_nodes(alive_nodes, value_matrix, ex, ey)  # sorting
        node = alive_nodes.pop(0)  # Expand most promising node
        value = get_value_given_letter(map[node.x][node.y])  # get value of map

        for dx, dy in MOVEMENTS_TO_ARROWS:
            nx = node.x + dx
            ny = node.y + dy

            if nx < 0 or ny < 0 or nx >= len(map) or ny >= len(map[0]):
                continue  # node not added

            if value_matrix[nx][ny] != -1 and value_matrix[nx][ny] <= node.iterations:
                continue  # not valid

            diff = get_value_given_letter(map[nx][ny]) - value
            if diff < -1:
                continue  # not valid

            value_matrix[nx][ny] = node.iterations
            if map[nx][ny] == 'a':
                if lowest_score > node.iterations:
                    lowest_score = node.iterations
                    print('End reached with score', node.iterations)

            alive_nodes.append(Node(
                x=nx,
                y=ny,
                iterations=node.iterations + 1,
                score=-1,
            ))

    return lowest_score


def get_path(map: List[str]):

    sx, sy = locate_character(map, 'S')
    ex, ey = locate_character(map, 'E')
    # visited = initialize_map(map, '.')
    value_matrix = initialize_map(map, -1)

    cx, cy = sx, sy

    starting_node = Node(cx, cy, 1, -1)
    alive_nodes = [starting_node]
    value_matrix[cx][cy] = 1

    while len(alive_nodes) > 0:

        alive_nodes = sort_nodes(alive_nodes, map, ex, ey)  # sorting

        # alive_nodes = remove_nodes(alive_nodes, value_matrix, ex, ey)  # sorting
        node = alive_nodes.pop(0)  # Expand most promising node
        value = get_value_given_letter(map[node.x][node.y])  # get value of map

        for dx, dy in MOVEMENTS_TO_ARROWS:
            nx = node.x + dx
            ny = node.y + dy

            if nx < 0 or ny < 0 or nx >= len(map) or ny >= len(map[0]):
                continue  # node not added

            if value_matrix[nx][ny] != -1 and value_matrix[nx][ny] <= node.iterations:
                continue  # not valid

            diff = get_value_given_letter(map[nx][ny]) - value
            if diff > 1:
                continue  # not valid

            value_matrix[nx][ny] = node.iterations

            if nx == ex and ny == ey:
                print('End reached with score', node.iterations)
                continue  # reached final point

            alive_nodes.append(Node(
                x=nx,
                y=ny,
                iterations=node.iterations + 1,
                score=-1,
            ))

    return value_matrix[ex][ey]


def main():
    map = read_input_as_lines('input.txt')
    value = get_path(map)
    value = get_path_inverse(map)
    print(value)


if __name__ == '__main__':
    main()
