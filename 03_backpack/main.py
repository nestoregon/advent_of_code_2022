from typing import List


def read_input_as_lines(input_path: str) -> List[str]:
    with open(input_path) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    return lines


def get_value_given_letter(letter: str) -> int:
    if letter.islower():
        minus = 96
    else:
        minus = 38
    letter_value = ord(letter) - minus
    return letter_value


def split_backpacks_into_two_and_find_intersection(backpacks: List[str]):
    total_value = 0
    for backpack in backpacks:
        length_of_backpack = len(backpack) // 2
        compartment_one = backpack[:length_of_backpack]
        compartment_two = backpack[length_of_backpack:]
        letter = get_intersection_given_group_of_strings([compartment_one, compartment_two])
        letter_value = get_value_given_letter(letter)
        total_value += letter_value
    return total_value


def get_intersection_given_group_of_strings(backpacks: List[str]):
    backpack_set = [set(backpack) for backpack in backpacks]
    intersection = set.intersection(*backpack_set)
    letter = next(iter(intersection))
    return letter


def split_backpacks_into_three_and_find_intersection(backpacks: List[str]):
    total_value = 0
    while len(backpacks) > 0:
        backpack_set = backpacks[:3]
        backpacks = backpacks[3:]  # update
        letter = get_intersection_given_group_of_strings(backpack_set)
        letter_value = get_value_given_letter(letter)
        total_value += letter_value
    return total_value


backpacks = read_input_as_lines('input.txt')
total_value_compartments = split_backpacks_into_two_and_find_intersection(backpacks)
total_value_sets = split_backpacks_into_three_and_find_intersection(backpacks)
print(total_value_compartments)
print(total_value_sets)
