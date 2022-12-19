"""
Let's find those Beacons!!!

Sensors can be understood as circles with a center.
Circles can have intersections!


Given a line, (-), you can calculate interections (i)

......................................................
............................#.........................
...........................###........................
--------------------------i###i-----------------------
.........................###S###......................
..........................#####.......................
...........................###........................
............................#.........................
......................................................

These intersection points (i) will be useful to solve the problems.
"""
from typing import List, Set, Tuple
from dataclasses import dataclass


@dataclass
class Intersection:
    x: int
    side: str


SIDE_TO_PARENTHESIS = {
    'left': 1,
    'right': -1,
}


def read_input_as_lines(input_path: str) -> List[str]:
    with open(input_path) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    return lines


def get_all_intersections_with_line(sensors, y_coordinate):
    intersections = []
    for cx, cy, distance in sensors:
        dx = distance - abs(y_coordinate - cy)
        if 0 < dx <= distance:
            intersections.append(Intersection(cx - dx, 'left'))
            intersections.append(Intersection(cx + dx, 'right'))

    intersections_sorted = sort_all_intersections_according_to_x_value(intersections)
    return intersections_sorted


def sort_all_intersections_according_to_x_value(intersections) -> List[Intersection]:
    return sorted(intersections, key=lambda x: x.x)


def is_point_seen_by_sensors(x, y, sensors):
    for sx, sy, distance in sensors:
        if abs(x - sx) + abs(y - sy) <= distance:
            return True
    return False


def get_total_coverage_by_line(sensors, beacons, y_coordinate):
    """
    The goal is to find the coverage of a line.
    To do that we need to find the intersections of the line.

    Where
        i = intersection
        # = covered
        . = empty

    line = i#####i###i###########i....................i#########i..........

    - We get all the intersections (i). There can be two intersections (right and left) for a given sensor
    - We sort them according to X (left to right)
        - We go from left to right. If we encounter a left edge, then we're being seen by a sensor.
        - If we encounter a righ one, means that we're out of the range
            - It could be that we encounter 2 right edges, in which case we're seen by 2 sensors.
        - , we're in an interval where there If there are no sensors "seeing" us
    """

    intersections_sorted = get_all_intersections_with_line(sensors, y_coordinate)

    if len(intersections_sorted) == 0:
        return 0

    sensors_within_range = 1
    previous = intersections_sorted.pop(0)
    covered = 0

    for intersection in intersections_sorted:
        difference = intersection.x - previous.x
        if sensors_within_range > 0:
            covered += difference  # sum all difference
        else:
            covered += 1  # sum the edge
        sensors_within_range += SIDE_TO_PARENTHESIS[intersection.side]
        previous = intersection  # udpate

    beacons_in_y = set([x[0] for x in beacons if x[0] == y_coordinate])
    covered -= len(beacons_in_y)  # take out beacons in the same line

    return covered


def get_missing_beacon(sensors: Set, iters: int) -> Tuple:
    """
    Same as 'get_total_coverage_by_line', but this time across multiple Y values.
    - Per line (y_coordinate) we get the intersections with the edges of beacons
    - Between 2 of these intersections is our missing beacon
    - The difference between edges needs to be 2.  #B#, where B is our missing beacon!
    - Once we found a difference of 2, we check if the point is not seen.
    - If that's the case, we check up and down. If they are seen, then we got it!

    ....................
    ...##############...
    ...###.###..#####...  in this example, the empty . is the missing beacon!
    ....###########.....
    """

    for y_coordinate in range(iters):
        intersections_sorted = get_all_intersections_with_line(sensors, y_coordinate)

        if len(intersections_sorted) == 0:
            continue

        opened = 1
        previous = intersections_sorted.pop(0)

        for intersection in intersections_sorted:
            difference = intersection.x - previous.x

            if difference == 2 and intersection.x - y_coordinate < iters:  # is what we're looking for?
                x = intersection.x - 1  # we're at an edge, so let's get the point to the left
                if not is_point_seen_by_sensors(x, y_coordinate, sensors):  # not seen!
                    upper_point_seen = is_point_seen_by_sensors(x, y_coordinate + 1, sensors)
                    lower_point_seen = is_point_seen_by_sensors(x, y_coordinate - 1, sensors)

                    if upper_point_seen and lower_point_seen:
                        return (x, y_coordinate)  # we found the sneaky beacon

            opened += SIDE_TO_PARENTHESIS[intersection.side]  # update parenthesis count
            previous = intersection  # udpate

    return (0, 0)  # no solution sadly


def format_input(lines):
    beacons = set()
    sensors = set()
    for line in lines:
        line = line.split()
        sx, sy = int(line[2][2:-1]), int(line[3][2:-1])
        bx, by = int(line[8][2:-1]), int(line[9][2:])
        distance = abs(sx - bx) + abs(sy - by)
        sensors.add((sx, sy, distance))
        beacons.add((bx, by))

    return sensors, beacons


def main():

    y_coordinate = int(2e6)
    iters = int(4e6)

    lines = read_input_as_lines('input.txt')
    sensors, beacons = format_input(lines)

    coverage = get_total_coverage_by_line(sensors, beacons, y_coordinate=y_coordinate)
    missing_beacon = get_missing_beacon(sensors, iters=iters)
    score = missing_beacon[0] * iters + missing_beacon[1]

    print(f'Problem 1: the sensor covers {coverage} tiles at y = {y_coordinate}')
    print(f'Problem 2: the missing sensor is located at {missing_beacon} (x, y). Score = {score}')


if __name__ == '__main__':
    main()
