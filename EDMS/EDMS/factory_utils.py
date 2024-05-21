import random
from datetime import datetime, timedelta
from typing import Set


def draw_unique_random_number(used_numbers: Set, min_value: int, max_value: int) -> int:
    number = random.randint(min_value, max_value)
    while number in used_numbers:
        number = random.randint(min_value, max_value)
    used_numbers.add(number)
    return number


def create_date(first_date: datetime) -> datetime:
    second_date = first_date + timedelta(days=random.randint(0, 366))
    return second_date
