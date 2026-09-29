import pytest

# Test-only file, per request: the functions below don't exist yet.
# Assumed interface (implement in validators.py, same folder):
#   validate_zip_code(zip_code) -> bool
#   validate_area(area) -> bool
#   validate_building_age(age) -> bool
#   validate_building_characteristics(zip_code, area, building_age) -> dict
#       with {"status": "confirmed" | "error", "message": str}
from validators import (
    validate_zip_code,
    validate_area,
    validate_building_age,
    validate_building_characteristics,
)


# Zip code must be within Germany (01067-99998) and an integer.
@pytest.mark.parametrize("zip_code", [1067, 10115, 20095, 80331, 99998])
def test_valid_zip_code(zip_code):
    assert validate_zip_code(zip_code) is True


@pytest.mark.parametrize("zip_code", [0, 999999, -10115, "10115", 10115.5])
def test_invalid_zip_code(zip_code):
    assert validate_zip_code(zip_code) is False


# Area must be an integer and less than 500.
@pytest.mark.parametrize("area", [1, 120, 499])
def test_valid_area(area):
    assert validate_area(area) is True


@pytest.mark.parametrize("area", [500, 600, "120", 120.5])
def test_invalid_area(area):
    assert validate_area(area) is False


# Building age must be an integer and less than 300.
@pytest.mark.parametrize("building_age", [0, 50, 299])
def test_valid_building_age(building_age):
    assert validate_building_age(building_age) is True


@pytest.mark.parametrize("building_age", [300, 350, "50", 50.5])
def test_invalid_building_age(building_age):
    assert validate_building_age(building_age) is False


# Right inputs show a confirmation message; wrong inputs show an error.
def test_valid_inputs_show_confirmation():
    result = validate_building_characteristics(zip_code=10115, area=120, building_age=50)
    assert result["status"] == "confirmed"


@pytest.mark.parametrize(
    "zip_code, area, building_age",
    [
        (999999, 120, 50),  # invalid zip code
        (10115, 600, 50),  # invalid area
        (10115, 120, 350),  # invalid building age
    ],
)
def test_invalid_inputs_show_error(zip_code, area, building_age):
    result = validate_building_characteristics(
        zip_code=zip_code, area=area, building_age=building_age
    )
    assert result["status"] == "error"
