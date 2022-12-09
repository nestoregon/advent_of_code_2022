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


def get_tail_visit_of_rope(input: List[str], length: int) -> int:

    start = (0, 0)
    visited_by_tail = [start]
    rope = visited_by_tail * length
    hx, hy = rope[0]
    tx, ty = rope[-1]

    for instruction in input:
        direction, value = instruction.split()
        dx, dy = LETTER_TO_DIRECTION[direction]
        for _ in range(int(value)):
            hx, hy = rope[0]
            hx += dx  # update head only
            hy += dy
            rope[0] = hx, hy

            for i in range(length - 1):
                hx, hy = rope[i]
                tx, ty = rope[i + 1]

                # update tail
                diff_x = hx - tx
                diff_y = hy - ty
                if abs(diff_x) <= 1 and abs(diff_y) <= 1:
                    continue  # tail is touching

                if abs(diff_x) == 2 or abs(diff_y) == 2:
                    if diff_x != 0:
                        tx += diff_x // abs(diff_x)
                    if diff_y != 0:
                        ty += diff_y // abs(diff_y)

                rope[i+1] = tx, ty

            visited_by_tail.append(rope[-1])

    return len(set(visited_by_tail))


def main():
    movement_instructions = read_input_as_lines('input.txt')
    rope_of_two = get_tail_visit_of_rope(movement_instructions, 2)
    rope_of_ten = get_tail_visit_of_rope(movement_instructions, 10)
    print(rope_of_two)
    print(rope_of_ten)


if __name__ == '__main__':
    main()
