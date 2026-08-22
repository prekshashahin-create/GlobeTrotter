import unittest

from logic import (
    validate_trip_dates,
    calculate_trip_days,
    validate_cost,
    calculate_total_budget,
    calculate_average_daily_cost,
    validate_stop_dates,
    calculate_stop_days,
    validate_activity_date,
    check_budget_status
)


class TestTripDates(unittest.TestCase):

    def test_valid_trip_dates(self):
        result = validate_trip_dates("2026-09-01", "2026-09-05")
        self.assertEqual(result, (True, "Valid dates"))

    def test_end_date_before_start_date(self):
        result = validate_trip_dates("2026-09-10", "2026-09-05")
        self.assertFalse(result[0])

    def test_invalid_date_format(self):
        result = validate_trip_dates("01-09-2026", "05-09-2026")
        self.assertFalse(result[0])

    def test_one_day_trip(self):
        result = calculate_trip_days("2026-09-01", "2026-09-01")
        self.assertEqual(result, 1)


class TestCosts(unittest.TestCase):

    def test_valid_cost(self):
        result = validate_cost(5000)
        self.assertEqual(result, (True, "Valid cost"))

    def test_negative_cost(self):
        result = validate_cost(-500)
        self.assertFalse(result[0])

    def test_total_budget(self):
        total = calculate_total_budget(
            5000,
            8000,
            3000,
            4000
        )
        self.assertEqual(total, 20000)

    def test_average_daily_cost(self):
        average = calculate_average_daily_cost(20000, 5)
        self.assertEqual(average, 4000)


class TestStops(unittest.TestCase):

    def test_valid_stop(self):
        result = validate_stop_dates(
            "2026-09-01",
            "2026-09-10",
            "2026-09-02",
            "2026-09-05"
        )

        self.assertEqual(result, (True, "Valid stop dates"))

    def test_stop_before_trip(self):
        result = validate_stop_dates(
            "2026-09-05",
            "2026-09-10",
            "2026-09-01",
            "2026-09-04"
        )

        self.assertFalse(result[0])

    def test_stop_after_trip(self):
        result = validate_stop_dates(
            "2026-09-01",
            "2026-09-10",
            "2026-09-12",
            "2026-09-15"
        )

        self.assertFalse(result[0])

    def test_stop_days(self):
        days = calculate_stop_days(
            "2026-09-02",
            "2026-09-05"
        )

        self.assertEqual(days, 4)


class TestActivities(unittest.TestCase):

    def test_valid_activity_date(self):
        result = validate_activity_date(
            "2026-09-01",
            "2026-09-10",
            "2026-09-05"
        )

        self.assertEqual(result, (True, "Valid activity date"))

    def test_activity_outside_trip(self):
        result = validate_activity_date(
            "2026-09-01",
            "2026-09-10",
            "2026-09-15"
        )

        self.assertFalse(result[0])


class TestBudget(unittest.TestCase):

    def test_within_budget(self):
        result = check_budget_status(18000, 20000)
        self.assertEqual(result, (True, "Trip is within budget"))

    def test_over_budget(self):
        result = check_budget_status(25000, 20000)
        self.assertEqual(result, (False, "Trip is over budget."))


if __name__ == "__main__":
    unittest.main()