"""
part 1: brute force following instructions
part 2: use least common multiple in order to keep reminder calcualtion simple
"""
from typing import List
from dataclasses import dataclass


@dataclass
class Monkey:
    items: List
    operation: str
    divisible_by: int
    true: int
    false: int


def read_input_as_lines(input_path: str) -> List[str]:
    with open(input_path) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    return lines


def parse_input(input: List[str]) -> List[Monkey]:
    monkeys = []
    while True:
        input.pop(0)  # number is not used
        monkey = Monkey(
            items=eval(f"[{input.pop(0).split(':')[1]}]"),
            operation=input.pop(0).split('=')[1],
            divisible_by=int(input.pop(0).split()[-1]),
            true=int(input.pop(0).split()[-1]),
            false=int(input.pop(0).split()[-1]),
        )
        monkeys.append(monkey)
        if len(input) == 0:
            break  # end
        input.pop(0)  # new line

    return monkeys


def monkey_game(monkeys: List[Monkey]):

    least_common_multiple = 1
    for monkey in monkeys:
        least_common_multiple *= (monkey.divisible_by)

    counter_items = [0] * len(monkeys)
    part_to_iterations = {
        1: 20,  # 1st part is 20 iters
        2: 10_000  # 2nd part is 10_000 iters
    }

    for part in [1, 2]:
        for _ in range(part_to_iterations[part]):
            for i, monkey in enumerate(monkeys):
                counter_items[i] += len(monkey.items)

                for old in monkey.items:  # old is used in the eval
                    stress_level = eval(monkey.operation)

                    if part == 1:
                        stress_level = stress_level // 3
                    if part == 2:
                        stress_level %= least_common_multiple  # reduce stress

                    if stress_level % monkey.divisible_by == 0:
                        next_monkey = monkey.true
                    else:
                        next_monkey = monkey.false
                    monkeys[next_monkey].items.append(stress_level)
                monkeys[i].items = []  # empty items

        most_popular = sorted(counter_items, reverse=True)
        result = most_popular[0] * most_popular[1]
        print(f'Part {part} solution: {result}')


def main():
    input = read_input_as_lines('input.txt')
    monkeys = parse_input(input)
    monkey_game(monkeys)


if __name__ == '__main__':
    main()
