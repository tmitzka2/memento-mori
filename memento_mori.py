"""Memento mori.

Display a message about life and mortality,
based on the user's date of birth.
"""

from datetime import date, datetime, timedelta

from dateutil.relativedelta import relativedelta
import streamlit as st


def get_date_of_birth() -> datetime.date:
    """Let the user enter a date of birth."""
    date_of_birth = st.date_input(
        label="When were you born?",
        value=date.today() - relativedelta(years=20),
        min_value=date.today() - relativedelta(years=100),
        max_value=date.today() - timedelta(days=1),
    )
    return date_of_birth


def get_age(date_of_birth: datetime.date) -> int:
    """Calculate and return the user's age in years."""
    today = date.today()
    age_timedelta = today - date_of_birth
    age = round(
        # 3,600 seconds per hour, 24 hours per day,
        # 365 days per year (accounting for leap years).
        age_timedelta.total_seconds() / (365.2425 * 24 * 3600)
    )
    return age


def get_remaining_lifespan(
        date_of_birth: datetime.date,
        life_expectancy: int,
) -> dict:
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


def get_days_until_birthday(date_of_birth: datetime.date) -> int:
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


def show_message(
    age: int,
    days_until_birthday: int,
    life_expectancy: int,
    remaining: dict,
):
    """Display a message about the user's mortality."""
    st.markdown(f"\nToday you are **{age}** years old.")
    if days_until_birthday:
        if days_until_birthday > 1:
            st.markdown(
                f"In :red[{days_until_birthday} days] "
                f"you will turn **{age + 1}**."
            )
        else:
            st.markdown(f":red[Tomorrow] you will turn **{age + 1}**.")
    st.write("")
    st.markdown("\nRemember that every day could be your last.")
    st.markdown(
        f"Will you even live to see the year {date.today().year + 1}?\n\n"
    )
    if age < life_expectancy:
        st.write("")
        st.markdown(
            f"\nImagine that you will die at the age of **{life_expectancy}**."
        )
        st.write("Which would leave you a remaining lifespan of …")
        st.markdown(
            f"\n:red[{remaining['years']} years.] "
            f"That is {remaining['weeks']:,} weeks, "
            f"or {remaining['days']:,} days.")
        st.write("How will you spend them?")
    st.write("")
    st.markdown("\n💀 Memento mori - remember that you will die.")
    st.markdown("🌱 But even more important: :green[**remember to LIVE!**]")


def main(life_expectancy=80):
    """Call functions and display information."""
    st.title("Memento Mori")

    date_of_birth = get_date_of_birth()
    age = get_age(date_of_birth)
    remaining = get_remaining_lifespan(date_of_birth, life_expectancy)
    days_until_birthday = get_days_until_birthday(date_of_birth)

    button_clicked = st.button("Remind me!")
    st.divider()

    if button_clicked:
        show_message(age, days_until_birthday, life_expectancy, remaining)


if __name__ == "__main__":
    main()
