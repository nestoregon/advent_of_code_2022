from ctypes import Array
from typing import List, Set, Tuple
from dataclasses import dataclass
from operator import add

import numpy as np
from numpy import array


@dataclass
class Point:
    x: int
    y: int
    type: str


def read_input_as_lines(input_path: str) -> List[str]:
    with open(input_path) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    return lines


def initialize_map_frmo_rock_lines(input: List[str]) -> Set[Tuple[int, int]]:

    rock_points = set()

    for line in input:
        rock_path = line.split(' -> ')
        for i in range(len(rock_path) - 1):
            ax, ay = rock_path[i].split(',')
            bx, by = rock_path[i + 1].split(',')
            ax, ay, bx, by = int(ax), int(ay), int(bx), int(by)
            sorted_y = sorted([ay, by])
            sorted_x = sorted([ax, bx])

            if ax == bx:
                for dy in range(*tuple(sorted_y)):
                    rock_points.add((ax, dy))
            else:
                for dx in range(*tuple(sorted_x)):
                    rock_points.add((dx, ay))

            rock_points.add((max(sorted_x), max(sorted_y)))

    # rock_points = array(rock_points, int)

    return rock_points


def print_map_given_points(
    rock_points: Set,
    sand_points: Set,
    start_point: Set,
):
    all_points = set.union(*[rock_points, sand_points, start_point])
    x_points = sorted([point[0] for point in all_points])
    y_points = sorted([point[1] for point in all_points])
    lowest_x, highest_x = x_points[0], x_points[-1]
    lowest_y, highest_y = y_points[0], y_points[-1]

    for y in range(lowest_y, highest_y + 1):
        line = f'{y} '
        for x in range(lowest_x, highest_x + 1):
            if (x, y) in rock_points:
                line += '#'
            elif (x, y) in sand_points:
                line += 'o'
            elif (x, y) in start_point:
                line += '+'
            else:
                line += '.'

        print(line)


def get_type_of_x_and_y(x, y, points: List[Point]):
    for point in points:
        if point.x == x and point.y == y:
            return point.type
    return '.'


def get_new_falling_point(
    directions: List[List],
    falling_sand_point: List,
    points_to_check: List[List],
) -> List:
    for direction in directions:
        new_direction = list(map(add, falling_sand_point, direction))
        if new_direction not in points_to_check:  # if it's free
            return new_direction
    return falling_sand_point


def main():
    input = read_input_as_lines('input.txt')
    rock_points = initialize_map_frmo_rock_lines(input)
    start_point = (500, 0)
    sand_points = set()

    print_map_given_points(
        rock_points=rock_points,
        sand_points=sand_points,
        start_point={start_point},
    )

    # directions = [[0, 1], [-1, 1], [1, 1]]
    lowest_y = max(sorted([point[1] for point in rock_points.union({start_point})]))


    within_map = True
    sand_points = set()
    part_one = True

    while within_map:
        sand = start_point
        all_points = set.union(*[sand_points, rock_points])

        while True:
            if sand[1] > lowest_y:
                if part_one:
                    part_one = False
                    print(f'Part 1: {len(sand_points)}')
                break
            elif (sand[0], sand[1] + 1) not in all_points:
                sand = (sand[0], sand[1] + 1)
            elif (sand[0] - 1, sand[1] + 1) not in all_points:
                sand = (sand[0] - 1, sand[1] + 1)
            elif (sand[0] + 1, sand[1] + 1) not in all_points:
                sand = (sand[0] + 1, sand[1] + 1)
            else:
                break

        sand_points.add(sand)
        if sand == start_point:
            break

    print_map_given_points(
        rock_points=rock_points,
        sand_points=sand_points,
        start_point={start_point},
    )

    print(f'Part 2: {len(sand_points)}')


if __name__ == '__main__':
    main()
