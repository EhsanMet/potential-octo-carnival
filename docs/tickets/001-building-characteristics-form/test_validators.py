import pytest

from validators import (
    HEATING_TYPES,
    WINDOW_TYPES,
    validate_area,
    validate_building_age,
    validate_building_characteristics,
    validate_heating_type,
    validate_windows_type,
    validate_zip_code,
)

VALID = dict(zip_code=10115, area=120, building_age=50, heating_type="Gas", windows_type="2 layers")


# Zip code must be within Germany (01067-99998) and an integer.
@pytest.mark.parametrize("zip_code", [1067, 10115, 20095, 80331, 99998])
def test_valid_zip_code(zip_code):
    assert validate_zip_code(zip_code) is True


@pytest.mark.parametrize("zip_code", [0, 999999, -10115, "10115", 10115.5])
def test_invalid_zip_code(zip_code):
    assert validate_zip_code(zip_code) is False


# Area must be an integer, more than 0 and less than 500.
@pytest.mark.parametrize("area", [1, 120, 499])
def test_valid_area(area):
    assert validate_area(area) is True


@pytest.mark.parametrize("area", [0, -5, 500, 600, "120", 120.5])
def test_invalid_area(area):
    assert validate_area(area) is False


# Building age must be an integer, at least 0 and less than 300.
@pytest.mark.parametrize("building_age", [0, 50, 299])
def test_valid_building_age(building_age):
    assert validate_building_age(building_age) is True


@pytest.mark.parametrize("building_age", [-1, 300, 350, "50", 50.5])
def test_invalid_building_age(building_age):
    assert validate_building_age(building_age) is False


# Heating type and windows type must be chosen from the drop-down lists.
@pytest.mark.parametrize("heating_type", HEATING_TYPES)
def test_valid_heating_type(heating_type):
    assert validate_heating_type(heating_type) is True


@pytest.mark.parametrize("heating_type", ["", None, "Coal", "gas"])
def test_invalid_heating_type(heating_type):
    assert validate_heating_type(heating_type) is False


@pytest.mark.parametrize("windows_type", WINDOW_TYPES)
def test_valid_windows_type(windows_type):
    assert validate_windows_type(windows_type) is True


@pytest.mark.parametrize("windows_type", ["", None, "4 layers", 2])
def test_invalid_windows_type(windows_type):
    assert validate_windows_type(windows_type) is False


# Right inputs show a confirmation message; wrong inputs show an error for that field.
def test_valid_inputs_show_confirmation():
    result = validate_building_characteristics(**VALID)
    assert result["status"] == "confirmed"
    assert result["errors"] == {}


@pytest.mark.parametrize(
    "field, bad_value",
    [
        ("zip_code", 999999),
        ("area", 600),
        ("building_age", 350),
        ("heating_type", "Coal"),
        ("windows_type", "4 layers"),
    ],
)
def test_invalid_input_shows_error_for_that_field(field, bad_value):
    result = validate_building_characteristics(**{**VALID, field: bad_value})
    assert result["status"] == "error"
    assert list(result["errors"]) == [field]
