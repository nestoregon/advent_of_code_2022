from typing import List


def read_input_as_lines(input_path: str) -> List[str]:
    with open(input_path) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    return lines


LETTER_TO_DIRECTION = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, 1),
    'D': (0, -1),
}


def simulate_rope_and_get_tail_visit(movements: List[str], length: int) -> int:

    start = (0, 0)
    rope = [start] * length
    visited_by_tail = [start]

    for movement in movements:
        direction, value = movement.split()
        dx, dy = LETTER_TO_DIRECTION[direction]
        for _ in range(int(value)):
            # udpate head
            hx, hy = rope[0]
            rope[0] = hx + dx, hy + dy
            # simulate tail concat movement
            for i in range(length - 1):

                # get two points
                hx, hy = rope[i]
                tx, ty = rope[i + 1]

                # difference
                diff_x = hx - tx
                diff_y = hy - ty

                # if is touching, do nothing
                if abs(diff_x) <= 1 and abs(diff_y) <= 1:
                    continue

                # update tail
                tx += 0 if diff_x == 0 else diff_x // abs(diff_x)  # +1, 0, -1
                ty += 0 if diff_y == 0 else diff_y // abs(diff_y)  # +1, 0, -1
                rope[i + 1] = tx, ty

            visited_by_tail.append(rope[-1])  # only append final tail
    return len(set(visited_by_tail))  # return unique visited


def main():
    movements = read_input_as_lines('input.txt')
    rope_of_two = simulate_rope_and_get_tail_visit(movements, 2)
    rope_of_ten = simulate_rope_and_get_tail_visit(movements, 10)
    print(rope_of_two)
    print(rope_of_ten)


if __name__ == '__main__':
    main()
