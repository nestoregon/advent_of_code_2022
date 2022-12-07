from typing import List


def read_input_lines(input_path: str) -> List[str]:
    with open(input_path) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    return lines


def get_elf_total_calories(input: List[str]):
    elf_total_calories = []
    calories_so_far = 0

    for calories in input:
        if calories == '':
            elf_total_calories.append(calories_so_far)
            calories_so_far = 0
        else:
            calories_so_far += int(calories)
    elf_total_calories.append(calories_so_far)

    return elf_total_calories


input = read_input_lines('input.txt')
elf_total_calories = get_elf_total_calories(input)
elf_total_calories = sorted(elf_total_calories)[::-1]

elf_with_max_calories = elf_total_calories[0]
top_three_elves_calories = sum(elf_total_calories[:3])

print(f'The elf with most calories has {elf_with_max_calories}')
print(f'The top 3 elves with most calories have {top_three_elves_calories}')
