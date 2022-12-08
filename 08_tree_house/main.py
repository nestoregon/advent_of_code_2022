from dataclasses import dataclass
from typing import List


@dataclass
class Point:
    x: int
    y: int

    def is_point_valid(self, tree_map: List[List[int]]):
        if self.x not in range(len(tree_map[0])):
            return False
        if self.y not in range(len(tree_map)):
            return False
        return True


def convert_input_to_int(input):
    mapping = []
    for row in input:
        row_int = []
        for letter in row:
            row_int.append(int(letter))
        mapping.append(row_int)
    return mapping


def read_input_as_lines(input_path: str) -> List[str]:
    with open(input_path) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    return lines


def is_visible(
    point: Point,
    tree_map: List[List[int]],
    direction_x: int,
    direction_y: int,
    tree_height: int,
):

    new_point = Point(point.x + direction_x, point.y + direction_y)

    if not new_point.is_point_valid(tree_map):
        return True

    if tree_map[new_point.x][new_point.y] < tree_height:
        return is_visible(new_point, tree_map, direction_x, direction_y, tree_height)

    return False


def number_of_trees_observed(
    point: Point,
    tree_map: List[List[int]],
    direction_x: int,
    direction_y: int,
    tree_height: int,
):
    new_point = Point(point.x + direction_x, point.y + direction_y)
    if not new_point.is_point_valid(tree_map):
        return 0

    if tree_map[new_point.x][new_point.y] < tree_height:
        return 1 + number_of_trees_observed(new_point, tree_map, direction_x, direction_y, tree_height)

    return 1


def get_scenic_value(list_of_numbers: List[int]):
    total = 1
    for n in list_of_numbers:
        total *= n
    return total


def get_highest_scenic_value_of_tree_map(tree_map: List[List[int]]):
    max_scenic = 0
    for x, row in enumerate(tree_map):
        for y, height in enumerate(row):
            point = Point(x, y)
            solutions = [
                number_of_trees_observed(point, tree_map, 1, 0, height),
                number_of_trees_observed(point, tree_map, -1, 0, height),
                number_of_trees_observed(point, tree_map, 0, 1, height),
                number_of_trees_observed(point, tree_map, 0, -1, height),
            ]
            # calculate scenic value from the 4 directions you see trees
            scenic_value = get_scenic_value(solutions)
            if scenic_value > max_scenic:
                max_scenic = scenic_value

    return max_scenic


def get_total_visible_trees(tree_map: List[List[int]]):
    visible_counter = 0
    for x, row in enumerate(tree_map):
        for y, height in enumerate(row):
            point = Point(x, y)
            solutions = [
                is_visible(point, tree_map, 1, 0, height),
                is_visible(point, tree_map, -1, 0, height),
                is_visible(point, tree_map, 0, 1, height),
                is_visible(point, tree_map, 0, -1, height),
            ]
            if any(solutions):  # can you see the tree from any direction?
                visible_counter += 1

    return visible_counter


def main():
    input = read_input_as_lines('input.txt')
    tree_map = convert_input_to_int(input)
    visible_trees = get_total_visible_trees(tree_map)
    highest_scenic = get_highest_scenic_value_of_tree_map(tree_map)
    print(visible_trees)
    print(highest_scenic)


if __name__ == '__main__':
    main()
