GERMANY_ZIP_MIN = 1067
GERMANY_ZIP_MAX = 99998

AREA_MAX = 500
BUILDING_AGE_MAX = 300

HEATING_TYPES = ["Gas", "Oil", "District heating", "Heat pump", "Electric", "Wood/pellets", "Other"]
WINDOW_TYPES = ["1 layer", "2 layers", "3 layers"]


def _is_integer(value):
    return isinstance(value, int) and not isinstance(value, bool)


def validate_zip_code(zip_code):
    return _is_integer(zip_code) and GERMANY_ZIP_MIN <= zip_code <= GERMANY_ZIP_MAX


def validate_area(area):
    return _is_integer(area) and 0 < area < AREA_MAX


def validate_building_age(building_age):
    return _is_integer(building_age) and 0 <= building_age < BUILDING_AGE_MAX


def validate_heating_type(heating_type):
    return heating_type in HEATING_TYPES


def validate_windows_type(windows_type):
    return windows_type in WINDOW_TYPES


def validate_building_characteristics(zip_code, area, building_age, heating_type, windows_type):
    errors = {}
    if not validate_zip_code(zip_code):
        errors["zip_code"] = "Zip code must be a valid German postal code."
    if not validate_area(area):
        errors["area"] = "Area must be a whole number from 1 to 499 m²."
    if not validate_building_age(building_age):
        errors["building_age"] = "Building age must be a whole number from 0 to 299."
    if not validate_heating_type(heating_type):
        errors["heating_type"] = "Please choose a heating type."
    if not validate_windows_type(windows_type):
        errors["windows_type"] = "Please choose a windows type."

    if errors:
        return {"status": "error", "message": " ".join(errors.values()), "errors": errors}
    return {"status": "confirmed", "message": "Building characteristics saved.", "errors": {}}
