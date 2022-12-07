"""
Rock paper scissors among elves! 🧝

Rock = 1
Paper = 2
Scissors = 3

The difficulty of this game is:
    - given a pair, what is the outcome?
    - given opponent score + outcome, what is your play?

I decided to do it calculating differences, but you can also hardcode the combinations.

Guess outcome example:
    - Your play is scissors: 3
    - Their play is paper: 2

    If the difference is negative you sum 3.

    Final outcome == 1 -> WIN!
    Final outcome == 2 -> LOSE!
    Final outcome == 0 -> TIE!

    differece = 1, so... 😏 You win!

Guess your play example:
    - Their play is paper: 2
    - Outcome is losing

    losing difference == 2

    2 + 2 = 4.
    However, your play can only be 1,2,3.
    Therefore, we substract 3. 4-3 = 1.

    You should play ROCK to lose!
"""
from typing import List

ABC_TO_ROCK_PAPER_SCISSORS = {
    'A': 1,  # rock
    'B': 2,  # paper
    'C': 3,  # scissors
}
XYZ_TO_ROCK_PAPER_SCISSORS = {
    'X': 1,  # rock
    'Y': 2,  # paper
    'Z': 3,  # scissors
}
XYZ_TO_OUTCOME = {
    'X': 0,  # lose
    'Y': 3,  # tie
    'Z': 6,  # win
}

# 6 points for winning, 3 for tying, 0 for losing.
OUTCOME_TO_DIFFERENCE = {
    6: 1,  # winning difference = 1
    3: 0,  # tying difference = 0
    0: 2,  # losing difference = 2
}
# reverse dict above
DIFFERENCE_TO_OUTCOME = {val: key
                         for (key, val) in OUTCOME_TO_DIFFERENCE.items()}


def read_input_as_lines(input_path: str) -> List[str]:
    with open(input_path) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    return lines


def make_sure_difference_is_positive(difference: int) -> int:
    """Difference has to be within 0,1,2. Eg: If -2 return 1."""
    return (difference + 3) % 3


def make_sure_play_is_less_than_4(play: int) -> int:
    """Play has to be within 1,2,3"""
    if play > 3:
        return play - 3
    return play


def get_outcome_given_plays(opponent_number: int, your_number: int) -> int:
    difference = your_number - opponent_number
    difference = make_sure_difference_is_positive(difference)
    return DIFFERENCE_TO_OUTCOME[difference]


def get_sum_of_outcomes_given_plays(plays: List[str]) -> int:
    total_result = 0
    for play in plays:
        opponent_play = ABC_TO_ROCK_PAPER_SCISSORS[play[0]]
        your_play = XYZ_TO_ROCK_PAPER_SCISSORS[play[2]]
        outcome = get_outcome_given_plays(opponent_play, your_play)
        total_result += your_play + outcome
    return total_result


def get_sum_of_your_plays_given_opponent_play_and_outcome(plays: List[str]):
    total_result = 0
    for play in plays:
        opponent_play = ABC_TO_ROCK_PAPER_SCISSORS[play[0]]
        outcome = XYZ_TO_OUTCOME[play[2]]
        your_play = what_should_i_throw_to_get_the_outcome(opponent_play, outcome)
        total_result += your_play + outcome
    return total_result


def what_should_i_throw_to_get_the_outcome(opponent_number: int, outcome: int) -> int:
    differece = OUTCOME_TO_DIFFERENCE[outcome]
    your_play = opponent_number + differece
    your_play = make_sure_play_is_less_than_4(your_play)
    return your_play


plays = read_input_as_lines('input.txt')
result_of_plays = get_sum_of_outcomes_given_plays(plays)
result_of_your_play = get_sum_of_your_plays_given_opponent_play_and_outcome(plays)
print(f'The total result is {result_of_plays}')
print(f'The total result of your plays is {result_of_your_play}')
