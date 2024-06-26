import secrets
from datetime import date, timedelta


def create_string_format_valid_date(first_date: date) -> date:
    """
    Generates a random valid date within a year from the given start date.

    Args:
        first_date (date): The initial date from which the new date is calculated.

    Returns:
        date: A new date within a range 0-365 days from the given start date.
    """
    return first_date + timedelta(days=secrets.randbelow(366))
