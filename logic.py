from datetime import datetime


def validate_trip_dates(start_date, end_date):
    """
    Checks whether the trip dates are valid.
    Returns (True, "Valid dates") if valid.
    Returns (False, error message) if invalid.
    """

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD."

    if end < start:
        return False, "End date cannot be before start date."

    return True, "Valid dates"


def calculate_trip_days(start_date, end_date):
    """
    Calculates the number of days in a trip.
    Both start and end dates are included.
    """

    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()

    if end < start:
        raise ValueError("End date cannot be before start date.")

    return (end - start).days + 1


def validate_cost(cost):
    """
    Checks whether a cost is valid.
    """

    if not isinstance(cost, (int, float)):
        return False, "Cost must be a number."

    if cost < 0:
        return False, "Cost cannot be negative."

    return True, "Valid cost"


def calculate_total_budget(transport, stay, activities, meals):
    """
    Calculates the total estimated trip cost.
    """

    costs = [transport, stay, activities, meals]

    for cost in costs:
        valid, message = validate_cost(cost)

        if not valid:
            raise ValueError(message)

    return transport + stay + activities + meals


def calculate_average_daily_cost(total_cost, trip_days):
    """
    Calculates the average cost per day.
    """

    if trip_days <= 0:
        raise ValueError("Trip days must be greater than zero.")

    if total_cost < 0:
        raise ValueError("Total cost cannot be negative.")

    return total_cost / trip_days