from typing import List


def read_input_as_lines(input_path: str) -> List[str]:
    with open(input_path) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    return lines


def main():
    input = read_input_as_lines('easy_input.txt')


if __name__ == '__main__':
    main()
