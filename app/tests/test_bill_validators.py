from datetime import date
from decimal import Decimal

import pytest

from validators.bill import (
    ENERGY_CARRIERS,
    parse_cost,
    parse_date,
    validate_billing_period,
    validate_consumption,
    validate_cost,
    validate_energy_carrier,
    validate_utility_bill,
)

TODAY = date(2026, 1, 1)

VALID = dict(
    energy_carrier="Gas",
    start_date=date(2025, 1, 1),
    end_date=date(2025, 12, 31),
    consumption_kwh=12000,
    total_cost=Decimal("1234.56"),
    today=TODAY,
)


# Energy carrier must be chosen from the drop-down list.
@pytest.mark.parametrize("energy_carrier", ENERGY_CARRIERS)
def test_valid_energy_carrier(energy_carrier):
    assert validate_energy_carrier(energy_carrier) is True


@pytest.mark.parametrize("energy_carrier", ["", None, "Coal", "gas"])
def test_invalid_energy_carrier(energy_carrier):
    assert validate_energy_carrier(energy_carrier) is False


# Billing period counts both days, must be 6-36 months, end after start and not in the future.
@pytest.mark.parametrize(
    "start_date, end_date",
    [
        (date(2025, 1, 1), date(2025, 6, 30)),  # exactly 6 months
        (date(2025, 1, 1), date(2025, 12, 31)),  # 12 months
        (date(2022, 1, 1), date(2024, 12, 31)),  # exactly 36 months
        (date(2024, 8, 31), date(2025, 2, 27)),  # month-end start, 6 months
        (date(2025, 1, 1), TODAY),  # ends today
    ],
)
def test_valid_billing_period(start_date, end_date):
    assert validate_billing_period(start_date, end_date, today=TODAY) is True


@pytest.mark.parametrize(
    "start_date, end_date",
    [
        (date(2025, 1, 1), date(2025, 5, 31)),  # 5 months
        (date(2025, 1, 1), date(2025, 6, 29)),  # one day short of 6 months
        (date(2022, 1, 1), date(2025, 1, 1)),  # one day over 36 months
        (date(2021, 12, 1), date(2024, 12, 31)),  # 37 months
        (date(2025, 12, 31), date(2025, 1, 1)),  # end before start
        (date(2025, 6, 1), date(2025, 6, 1)),  # same day
        (date(2025, 6, 1), date(2026, 1, 2)),  # ends in the future
        (None, date(2025, 12, 31)),
        (date(2025, 1, 1), None),
        ("2025-01-01", "2025-12-31"),
    ],
)
def test_invalid_billing_period(start_date, end_date):
    assert validate_billing_period(start_date, end_date, today=TODAY) is False


# Consumption must be a whole number from 1 to 300,000 kWh.
@pytest.mark.parametrize("consumption_kwh", [1, 12000, 300000])
def test_valid_consumption(consumption_kwh):
    assert validate_consumption(consumption_kwh) is True


@pytest.mark.parametrize("consumption_kwh", [0, -1, 300001, "12000", 12000.5, True, None])
def test_invalid_consumption(consumption_kwh):
    assert validate_consumption(consumption_kwh) is False


# Total cost must be more than 0 and at most 50,000 €, with at most 2 decimals.
@pytest.mark.parametrize("total_cost", [Decimal("0.01"), Decimal("1234.56"), Decimal("50000"), Decimal("80.5")])
def test_valid_cost(total_cost):
    assert validate_cost(total_cost) is True


@pytest.mark.parametrize(
    "total_cost",
    [Decimal("0"), Decimal("-10"), Decimal("50000.01"), Decimal("12.345"), Decimal("NaN"), 1234.56, 1234, None],
)
def test_invalid_cost(total_cost):
    assert validate_cost(total_cost) is False


# The cost box accepts a decimal comma or dot, but no thousands separators.
@pytest.mark.parametrize(
    "text, expected",
    [("1234,56", Decimal("1234.56")), ("1234.56", Decimal("1234.56")), (" 99 ", Decimal("99"))],
)
def test_parse_cost(text, expected):
    assert parse_cost(text) == expected


@pytest.mark.parametrize("text", ["1.234,56", "abc", "", "NaN", "Infinity", None])
def test_parse_cost_rejects(text):
    assert parse_cost(text) is None


# Dates come from the date picker as YYYY-MM-DD.
def test_parse_date():
    assert parse_date("2025-01-31") == date(2025, 1, 31)


@pytest.mark.parametrize("text", ["31.01.2025", "2025-02-30", "", None])
def test_parse_date_rejects(text):
    assert parse_date(text) is None


# Right inputs show a confirmation message; wrong inputs show an error for that field.
def test_valid_inputs_show_confirmation():
    result = validate_utility_bill(**VALID)
    assert result["status"] == "confirmed"
    assert result["message"] == "Utility bill saved."
    assert result["errors"] == {}


@pytest.mark.parametrize(
    "field, bad_value, error_key",
    [
        ("energy_carrier", "Coal", "energy_carrier"),
        ("end_date", date(2025, 3, 31), "billing_period"),
        ("consumption_kwh", 300001, "consumption_kwh"),
        ("total_cost", Decimal("12.345"), "total_cost"),
    ],
)
def test_invalid_input_shows_error_for_that_field(field, bad_value, error_key):
    result = validate_utility_bill(**{**VALID, field: bad_value})
    assert result["status"] == "error"
    assert list(result["errors"]) == [error_key]


def test_all_invalid_inputs_show_four_errors():
    result = validate_utility_bill(None, None, None, None, None, today=TODAY)
    assert result["status"] == "error"
    assert len(result["errors"]) == 4
