from typing import List
from dataclasses import dataclass


# for convenience, but you can also use a list
@dataclass
class Instruction:
    quantity: int
    origin: int
    destination: int


def read_input_as_lines(input_path: str) -> List[str]:
    with open(input_path) as file:
        lines = file.readlines()
    lines = [line.replace('\n', '') for line in lines]
    return lines


def transform_stacks_raw_to_stacks(stacks_raw: List[str]) -> List[List[str]]:
    keys = stacks_raw.pop()
    stacks_raw = stacks_raw[::-1]
    stacks = {}
    stacks = []
    for index, key in enumerate(keys):
        if key == ' ':
            continue
        stack = []
        for stack_row in stacks_raw:
            try:
                stack_letter = stack_row[index]
            except Exception:
                continue
            if stack_letter == ' ':
                continue
            stack.append(stack_letter)
        stacks.append(stack)
    return stacks


def transform_instructions_raw_to_instructions(instructions_raw: List[str]) -> List[Instruction]:
    instructions = []
    for instruction in instructions_raw:
        instruction = instruction.split(' ')
        instruction = Instruction(
            int(instruction[1]),
            int(instruction[3]) - 1,
            int(instruction[5]) - 1,
        )
        instructions.append(instruction)
    return instructions


def get_instructions_and_stacks_raw(input: List[str]):
    stacks_raw = []
    instructions_raw = []
    for index, line in enumerate(input):
        if line == '':
            stacks_raw = input[:index]
            instructions_raw = input[index + 1:]
            break
    return stacks_raw, instructions_raw


def move_multiple_crates_at_a_time(
    stacks_input: List[List[str]],
    instructions: List[Instruction],
) -> List[List[str]]:
    stacks = [stack.copy() for stack in stacks_input]
    for i in instructions:
        stacks[i.destination] += stacks[i.origin][-i.quantity:]  # append
        stacks[i.origin] = stacks[i.origin][:-i.quantity]  # update
    return stacks


def move_one_crate_at_a_time(
    stacks_input: List[List[str]],
    instructions_input: List[Instruction],
) -> List[List[str]]:
    stacks = [stack.copy() for stack in stacks_input]
    for i in instructions_input:
        quantity = i.quantity
        while quantity > 0:
            stacks[i.destination] += stacks[i.origin].pop()
            quantity -= 1

    return stacks


def get_stacks_and_instructions_from_input(input: List[str]):
    stacks_raw, instructions_raw = get_instructions_and_stacks_raw(input)
    stacks = transform_stacks_raw_to_stacks(stacks_raw)
    instructions = transform_instructions_raw_to_instructions(instructions_raw)
    return stacks, instructions


def get_top_letters_from_each_stack(stacks: List[List[str]]) -> str:
    letters = [stack[-1] for stack in stacks]
    letters = ''.join(letters)
    return letters


def print_information_about_process(stack: List[List[str]]):
    top_letters = get_top_letters_from_each_stack(stack)
    print(f'Top letters: {top_letters}')


input = read_input_as_lines('input.txt')
stacks, instructions = get_stacks_and_instructions_from_input(input)
stacks_moved_1 = move_one_crate_at_a_time(stacks, instructions)
stacks_moved_2 = move_multiple_crates_at_a_time(stacks, instructions)
print_information_about_process(stacks_moved_1)
print_information_about_process(stacks_moved_2)
