from typing import List


def read_input_as_lines(input_path: str) -> List[str]:
    with open(input_path) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    return lines


def update_clock(time, x):
    if (time + 20) % 40 == 0:
        return x * time
    return 0


def draw(line, time, x):
    draw_time = time % 40

    if draw_time in range(x, x + 3):
        line += '#'
    else:
        line += '.'
    if draw_time == 0:
        print(line)
        line = ''  # reset line
    return line


def main():
    input = read_input_as_lines('input.txt')
    total_sum = 0

    x = 1
    cycle = 1
    FRAME = '#'  # Starts with 1
    total_sum += update_clock(cycle, x)

    for line in input:
        cycle += 1
        FRAME = draw(FRAME, cycle, x)
        total_sum += update_clock(cycle, x)

        if line == 'noop':
            continue

        _, value = line.split()
        x += int(value)
        cycle += 1
        FRAME = draw(FRAME, cycle, x)
        total_sum += update_clock(cycle, x)

    print(f'Problem 1: {total_sum}')


if __name__ == '__main__':
    main()
