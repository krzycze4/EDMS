import random
from datetime import datetime, timedelta


def create_string_format_valid_date(first_date: str) -> str:
    first_date = datetime.strptime(first_date, "%Y-%m-%d").date()
    second_date = first_date + timedelta(days=random.randint(0, 366))
    return second_date.strftime("%Y-%m-%d")
