from typing import List, Set


def read_input_as_lines(input_path: str) -> List[str]:
    with open(input_path) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    return lines


def get_set_from_integers(lower_range: str, upper_range: str) -> Set[int]:
    return set(range(int(lower_range), int(upper_range) + 1))


def is_fully_contained(list_of_sets: List[Set[int]]) -> int:
    intersection = set.intersection(*list_of_sets)
    if intersection in list_of_sets:
        return 1
    return 0


def get_number_of_sets_contained(list_of_sets: List[Set[int]]) -> int:
    intersection = set.intersection(*list_of_sets)
    if len(intersection) > 0:
        return 1
    return 0


def extract_sets_from_rows(row: str):
    group_one, group_two = row.split(',')
    group_one = group_one.split('-')
    group_two = group_two.split('-')
    set_one = get_set_from_integers(group_one[0], group_one[1])
    set_two = get_set_from_integers(group_two[0], group_two[1])
    return set_one, set_two


cleaning_racks = read_input_as_lines('input.txt')
total_full_contained = 0
total_individal_sets = 0
for rack in cleaning_racks:
    first_set, second_set = extract_sets_from_rows(rack)
    total_full_contained += is_fully_contained([first_set, second_set])
    total_individal_sets += get_number_of_sets_contained([first_set, second_set])

print(total_full_contained)
print(total_individal_sets)
