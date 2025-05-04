# File: date_utils.py
from datetime import datetime


class DateHelper:
    """A utility class for date-related operations."""

    @staticmethod
    def get_year():
        """Returns the current year."""
        return datetime.now().year

    @staticmethod
    def get_month():
        """Returns the current month (1-12)."""
        return datetime.now().month

    @staticmethod
    def get_day():
        """Returns the current day of the month."""
        return datetime.now().day
