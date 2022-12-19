from typing import List, Set, Tuple
from dataclasses import dataclass


@dataclass
class Sensor:
    point: Set
    beacon: Set
    point: Set


def read_input_as_lines(input_path: str) -> List[str]:
    with open(input_path) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    return lines


def get_sensor_and_beacon_from_line(line: str) -> Tuple:
    sensor, beacon = line.split(':')

    sensor_x, sensor_y = sensor.split(' ', 2)[-1].split(', ')
    sensor_x = int(sensor_x.split('=')[1])
    sensor_y = int(sensor_y.split('=')[1])
    sensor = (sensor_x, sensor_y)

    beacon_x, beacon_y = beacon.split(' ', 2)[-1].split(', ')
    beacon_x = int(beacon_x.split('=')[1])
    beacon_y = int(beacon_y.split('=')[1])
    beacon = (beacon_x, beacon_y)

    return (sensor_x, sensor_y), (beacon_x, beacon_y)


def get_points_covered_by_beacons(input: List[str]):

    sensors = set()
    beacons = set()
    points = set()
    repeated_points = set()

    for index, line in enumerate(input):
        print(f'Processing line: {index}')
        sensor, beacon = get_sensor_and_beacon_from_line(line)
        sensors.add(sensor)
        beacons.add(beacon)
        distance = abs(beacon[0] - sensor[0]) + abs(beacon[1] - sensor[1])
        print(distance)
        continue

        # find a quicker algorithm to find all points
        # x_diff = range(-distance, distance + 1)
        # y_diff = x_diff
        # beacon_points = set()
        # for i in range(distance + 1):
        #     x, y = i, distance - i
        #     to_add = {
        #         (sensor[0] + x, sensor[1] + y),
        #         (sensor[0] + x, sensor[1] - y),
        #         (sensor[0] - x, sensor[1] + y),
        #         (sensor[0] - x, sensor[1] - y),
        #     }
        #     beacon_points = set.union(*[to_add, beacon_points])
        # repeated_points = repeated_points.union(beacon_points.intersection(points))
        # points = points.union(beacon_points)

        for x in range(-distance, distance + 1):
            for y in range(-distance, distance + 1):
                if abs(x) + abs(y) <= distance:
                    points.add((x + sensor[0], y + sensor[1]))

    breakpoint()
    return points, sensors, beacons, repeated_points


def print_map(
    points: Set,
    sensors: Set,
    beacons: Set,
    repeated_points: Set,
):
    points = (points - sensors) - beacons
    all_points = set.union(*[points, sensors, beacons]) - repeated_points
    lines = points - repeated_points
    x_points = sorted(list(set([point[0] for point in all_points])))
    y_points = sorted(list(set([point[1] for point in all_points])))

    for y in range(y_points[0], y_points[-1] + 1):
        line = f'{str(y).zfill(len(str(y_points[-1])))} '
        for x in range(x_points[0], x_points[-1] + 1):
            if (x, y) in points:
                line += '#'
            elif (x, y) in beacons:
                line += 'B'
            elif (x, y) in sensors:
                line += 'S'
            else:
                line += '.'
        print(line)


def get_beacons_covered_places_in_y_coordinate(
    points: Set,
    sensors: Set,
    beacons: Set,
    repeated_points: Set,
    y_coordinate: int,
) -> int:
    points = (points - sensors) - beacons
    all_points = set.union(*[points, sensors, beacons]) - repeated_points
    x_points = sorted(list(set([point[0] for point in all_points])))

    covered = 0
    covering = True

    for x in range(x_points[0], x_points[-1] + 1):

        if (x, y_coordinate) in points:
            covered += 1
            # if (x + 1, y_coordinate - 1) in all_points and (x - 1, y_coordinate + 1) in all_points:
            #     covering = not covering
            # if (x - 1, y_coordinate - 1) in all_points and (x + 1, y_coordinate + 1) in all_points:
            #     covering = not covering
        # elif covering:
        #     covered += 1

    print(f'Line {y_coordinate}: {covered}')
    return covered


def main():
    input = read_input_as_lines('input.txt')
    points, sensors, beacons, repeated_points = get_points_covered_by_beacons(input)
    print_map(points, sensors, beacons, repeated_points)
    get_beacons_covered_places_in_y_coordinate(points, sensors, beacons, repeated_points, 10)


if __name__ == '__main__':
    main()
