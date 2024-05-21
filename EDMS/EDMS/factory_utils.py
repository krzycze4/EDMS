import random
from typing import Set


def draw_unique_random_number(used_numbers: Set, min_value: int, max_value: int) -> int:
    number = random.randint(min_value, max_value)  # nosec
    while number in used_numbers:
        number = random.randint(min_value, max_value)
    used_numbers.add(number)
    return number
