from typing import List
from copy import deepcopy


def read_input_as_lines(input_path: str) -> List[int]:
    with open(input_path) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    lines = [eval(line) for line in lines if line != '']
    return lines


def compare_two_lists(list_one, list_two) -> int:
    """Return 0 if it's a tie, 1 if list_one is lower, -1 if list one is higher"""

    if type(list_one) == list and type(list_two) == int:
        list_two = [list_two]
    elif type(list_two) == list and type(list_one) == int:
        list_one = [list_one]

    # if it's a list
    if type(list_one) == type(list_two) == list:
        while True:
            if len(list_one) == 0 and len(list_two) > 0:
                return 1
            elif len(list_two) == 0 and len(list_one) > 0:
                return -1
            elif len(list_two) == len(list_one) == 0:
                return 0

            item_one = list_one.pop(0)
            item_two = list_two.pop(0)
            result = compare_two_lists(item_one, item_two)
            if result != 0:
                return result

    # if it's an integer
    else:
        if list_one < list_two:
            return 1
        elif list_one > list_two:
            return -1
        else:
            return 0


def get_score_for_indexes_that_are_in_correct_order(original_input: List[int]) -> int:
    input = deepcopy(original_input)

    iteration = 0
    score = 0

    # iterate through pairs. Is there a better way?
    for i in range(len(input) // 2):
        iteration += 1
        if compare_two_lists(input[i * 2], input[i * 2 + 1]) == 1:
            score += iteration
    return score


def sort_list_of_brackets(original_input: List, items_to_add: List) -> List:
    input = deepcopy(original_input)
    input += items_to_add  # Add items
    ordered_list = [input.pop(0)]

    for line in input:
        position = 0
        for item in ordered_list:
            if compare_two_lists(deepcopy(item), deepcopy(line)) == 1:
                position += 1
                continue

        ordered_list.insert(position, line)

    return ordered_list


def print_lists(input: List[int]):
    for line in input:
        print(line)


def main():
    input = read_input_as_lines('input.txt')
    score = get_score_for_indexes_that_are_in_correct_order(input)

    item_one = [[2]]
    item_two = [[6]]
    ordered_list = sort_list_of_brackets(input, items_to_add=[item_one, item_two])
    index_one = ordered_list.index(item_one) + 1
    index_two = ordered_list.index(item_two) + 1

    print(f'Part one: {score}')
    print(f'Part two: {index_one*index_two}')


if __name__ == '__main__':
    main()
