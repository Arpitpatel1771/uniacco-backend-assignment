from datetime import date, timedelta, datetime
from pprint import pprint


def calculate_repayment_schedule(
    amount, start_date, emi_date, interest_rate, tenure_months=12
):
    # Convert annual interest rate to daily and monthly interest rates
    monthly_interest_rate = (interest_rate / 100) / 12
    daily_interest_rate = (interest_rate / 100) / 365

    # Calculate EMI using the formula: E = P * r * (1 + r)^n / [(1 + r)^n - 1]
    emi = (
        amount
        * monthly_interest_rate
        * (1 + monthly_interest_rate) ** tenure_months
        / ((1 + monthly_interest_rate) ** tenure_months - 1)
    )

    schedule = []
    remaining_balance = amount
    current_date = start_date

    # Handle the first EMI with partial interest
    first_emi_date = current_date
    if (
        current_date.day > emi_date
    ):  # If start_date is after EMI day, move to next month
        first_emi_date = date(current_date.year, current_date.month, emi_date)
        while (
            first_emi_date <= current_date.date()
        ):  # Adjust to the next month if necessary
            if first_emi_date.month == 12:
                first_emi_date = date(first_emi_date.year + 1, 1, emi_date)
            else:
                first_emi_date = date(
                    first_emi_date.year, first_emi_date.month + 1, emi_date
                )
    elif current_date.day < emi_date:  # If start_date is before EMI day
        first_emi_date = date(current_date.year, current_date.month, emi_date)

    # Calculate days between start_date and first EMI date
    days_diff = (first_emi_date - current_date.date()).days
    partial_interest = remaining_balance * daily_interest_rate * days_diff

    # Add the first partial EMI
    schedule.append(
        {
            "emi_date": first_emi_date,
            "principal": 0.0,
            "interest": round(partial_interest, 2),
            "emi": round(partial_interest, 2),
            "remaining_balance": round(remaining_balance, 2),
        }
    )

    current_date = first_emi_date

    # Calculate subsequent EMIs
    for i in range(tenure_months):
        # Calculate interest for the month
        interest = remaining_balance * monthly_interest_rate

        # Calculate principal part of EMI
        principal = emi - interest

        # Reduce remaining balance
        remaining_balance -= principal

        # Ensure dates align with the EMI date
        if current_date.month == 12:
            next_due_date = date(current_date.year + 1, 1, emi_date)
        else:
            next_due_date = date(current_date.year, current_date.month + 1, emi_date)

        # Add EMI details to schedule
        schedule.append(
            {
                "emi_date": next_due_date,
                "principal": round(principal, 2),
                "interest": round(interest, 2),
                "emi": round(emi, 2),
                "remaining_balance": round(
                    max(remaining_balance, 0), 2
                ),  # Avoid negative balance
            }
        )

        # Move to the next month
        current_date = next_due_date

    return schedule
