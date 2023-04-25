#!/usr/bin/env python3
"""Memento mori.

Display a message about life and mortality,
based on the user's date of birth.
"""

from datetime import date, datetime

from dateutil.relativedelta import relativedelta

LIFE_EXPECTANCY = 80


def get_date_of_birth() -> datetime.date:
    """Return the user's date of birth."""
    while True:
        user_input = input("\nWhen were you born? (YYYY-MM-DD) ")
        try:
            date_of_birth = datetime.strptime(user_input, "%Y-%m-%d").date()
            if date_of_birth > date.today():
                print(
                    "Are you a time traveller? "
                    "Please enter a date in the past."
                )
                continue
        except ValueError:
            print("Please enter a real date in the format YYYY-MM-DD.")
        else:
            return date_of_birth


def get_age(date_of_birth) -> int:
    """Calculate and return the user's age in years."""
    today = date.today()
    age_timedelta = today - date_of_birth
    age = round(
        # 3,600 seconds per hour, 24 hours per day,
        # 365 days per year (accounting for leap years).
        age_timedelta.total_seconds() / (365.2425 * 24 * 3600)
    )
    return age


def get_remaining_lifespan(date_of_birth, life_expectancy) -> dict:
    """Calculate the user's approximate remaining lifespan.

    Return the number of days, weeks, and years.
    """
    today = date.today()
    date_of_death = date_of_birth + relativedelta(years=life_expectancy)
    remaining_timedelta = date_of_death - today
    remaining = {
        "days": remaining_timedelta.days,
        "weeks": round(remaining_timedelta.days / 7),
        "years": round(
            remaining_timedelta.total_seconds() / (365.2425 * 24 * 3600)
        ),
    }
    return remaining


def get_days_until_birthday(date_of_birth) -> int:
    """Return the number of days until the user's next birthday."""
    # First, find out the user's next birthday.
    today = date.today()
    # Take care of birthdays on Feb 29th (leap years):
    if not (date_of_birth.month == 2 and date_of_birth.day == 29):
        birthday_this_year = date(
            today.year,
            date_of_birth.month,
            date_of_birth.day,
        )
        birthday_next_year = date(
            today.year + 1,
            date_of_birth.month,
            date_of_birth.day,
        )
    else:
        birthday_this_year = date(today.year, 2, 28)
        birthday_next_year = date(today.year + 1, 2, 28)

    if birthday_this_year < today:
        # This year's birthday has already passed.
        next_birthday = birthday_next_year
    else:
        # This year's birthday is still to come or is today.
        next_birthday = birthday_this_year

    # Calculate days until next birthday.
    birthday_timedelta = next_birthday - today
    return birthday_timedelta.days


def main():
    """Call functions and display information."""
    print("=== MEMENTO MORI ===")

    date_of_birth = get_date_of_birth()
    age = get_age(date_of_birth)
    remaining = get_remaining_lifespan(date_of_birth, LIFE_EXPECTANCY)
    days_until_birthday = get_days_until_birthday(date_of_birth)

    print(f"\nToday you are {age} years old.")
    if days_until_birthday:
        if days_until_birthday > 1:
            print(f"In {days_until_birthday} days", end=" ")
        else:
            print("Tomorrow", end=" ")
        print(f"you will turn {age + 1}.")
    print("\nRemember that every day could be your last.")
    print(f"Will you even live to see the year {date.today().year + 1}?")
    if age < LIFE_EXPECTANCY:
        print(f"\nImagine that you will die at the age of {LIFE_EXPECTANCY}.")
        print("Which would leave you a remaining lifespan of …")
        print(
            f"\n{remaining['years']} years. "
            f"That is {remaining['weeks']:,} weeks, "
            f"or {remaining['days']:,} days.")
        print("How will you spend them?")
    print("\n💀 Memento mori - remember that you will die.")
    print("✨ But even more important: remember to LIVE!")


if __name__ == "__main__":
    main()
