import calendar
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation

from validators.common import is_integer

ENERGY_CARRIERS = ["Electricity", "Gas", "Oil", "District heating", "Wood/pellets", "Other"]

CONSUMPTION_MAX = 300_000
COST_MAX = Decimal("50000")
PERIOD_MIN_MONTHS = 6
PERIOD_MAX_MONTHS = 36


def parse_date(text):
    try:
        return date.fromisoformat(text)
    except (TypeError, ValueError):
        return None


def parse_cost(text):
    # Accept a German decimal comma ("1234,56") as well as a dot.
    try:
        cost = Decimal(text.strip().replace(",", "."))
    except (AttributeError, InvalidOperation):
        return None
    return cost if cost.is_finite() else None


def _add_months(day, months):
    month_index = day.month - 1 + months
    year = day.year + month_index // 12
    month = month_index % 12 + 1
    return date(year, month, min(day.day, calendar.monthrange(year, month)[1]))


def validate_energy_carrier(energy_carrier):
    return energy_carrier in ENERGY_CARRIERS


def validate_billing_period(start_date, end_date, today=None):
    if not isinstance(start_date, date) or not isinstance(end_date, date):
        return False
    today = today or date.today()
    if end_date <= start_date or end_date > today:
        return False
    # Both days count, so 01.01.-31.12. is 12 months: compare against the day after the end.
    period_end = end_date + timedelta(days=1)
    return (
        _add_months(start_date, PERIOD_MIN_MONTHS)
        <= period_end
        <= _add_months(start_date, PERIOD_MAX_MONTHS)
    )


def validate_consumption(consumption_kwh):
    return is_integer(consumption_kwh) and 0 < consumption_kwh <= CONSUMPTION_MAX


def validate_cost(total_cost):
    return (
        isinstance(total_cost, Decimal)
        and total_cost.is_finite()
        and 0 < total_cost <= COST_MAX
        and total_cost.as_tuple().exponent >= -2
    )


def validate_utility_bill(energy_carrier, start_date, end_date, consumption_kwh, total_cost, today=None):
    errors = {}
    if not validate_energy_carrier(energy_carrier):
        errors["energy_carrier"] = "Please choose an energy carrier."
    if not validate_billing_period(start_date, end_date, today):
        errors["billing_period"] = (
            "Billing period must be 6 months to 3 years, end after it starts and not in the future."
        )
    if not validate_consumption(consumption_kwh):
        errors["consumption_kwh"] = "Consumption must be a whole number from 1 to 300,000 kWh."
    if not validate_cost(total_cost):
        errors["total_cost"] = "Total cost must be more than 0 and at most 50,000 €, with up to 2 decimals."

    if errors:
        return {"status": "error", "message": " ".join(errors.values()), "errors": errors}
    return {"status": "confirmed", "message": "Utility bill saved.", "errors": {}}
