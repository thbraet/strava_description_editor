import pytest
from datetime import datetime, timedelta

from app.blueprints.streak.routes import longest_streak

@pytest.mark.parametrize(
    "dates, expected",
    [
        # Happy path tests
        ([datetime(2023, 1, 1), datetime(2023, 1, 2), datetime(2023, 1, 3)], 3),
        ([datetime(2023, 1, 1), datetime(2023, 1, 3), datetime(2023, 1, 4)], 2),
        ([datetime(2023, 1, 1), datetime(2023, 1, 2), datetime(2023, 1, 4)], 2),

        # Edge cases
        ([], 0),
        ([datetime(2023, 1, 1)], 1),
        ([datetime(2023, 1, 1), datetime(2023, 1, 3)], 1),
        ([datetime(2023, 1, 1), datetime(2023, 1, 2), datetime(2023, 1, 5)], 2),

        # Error cases
        ([datetime(2023, 1, 1), datetime(2022, 12, 31)], 2),
        ([datetime(2023, 1, 1), datetime(2023, 1, 1)], 1),
    ],
    ids=[
        "consecutive_dates", "non_consecutive_dates", "mixed_consecutive_non_consecutive",
        "empty_list", "single_date", "two_non_consecutive_dates", "two_consecutive_one_non_consecutive",
        "dates_in_reverse_order", "duplicate_dates"
    ]
)
def test_longest_streak(dates, expected):
    # Act
    result = longest_streak(dates)

    # Assert
    assert result == expected
