from typing import List


def read_input_as_lines(input_path: str) -> List[str]:
    with open(input_path) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    return lines


def finding_first_signal(input: str, number_of_unique_numbers: int) -> int:
    signal = []
    for index, letter in enumerate(input):
        signal.append(letter)
        if len(signal) > number_of_unique_numbers:
            signal.pop(0)
        if len(set(signal)) == number_of_unique_numbers:
            return index + 1
    return 0


input = read_input_as_lines('input.txt')[0]
start_number = finding_first_signal(input, 4)
message_number = finding_first_signal(input, 14)
print('start number', start_number)
print('message number', message_number)
