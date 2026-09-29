GERMANY_ZIP_MIN = 1067
GERMANY_ZIP_MAX = 99998

AREA_MAX = 500
BUILDING_AGE_MAX = 300


def _is_integer(value):
    return isinstance(value, int) and not isinstance(value, bool)


def validate_zip_code(zip_code):
    return _is_integer(zip_code) and GERMANY_ZIP_MIN <= zip_code <= GERMANY_ZIP_MAX


def validate_area(area):
    return _is_integer(area) and area < AREA_MAX


def validate_building_age(building_age):
    return _is_integer(building_age) and building_age < BUILDING_AGE_MAX


def validate_building_characteristics(zip_code, area, building_age):
    errors = []
    if not validate_zip_code(zip_code):
        errors.append("zip code must be a valid German postal code (integer)")
    if not validate_area(area):
        errors.append("area must be an integer less than 500")
    if not validate_building_age(building_age):
        errors.append("building age must be an integer less than 300")

    if errors:
        return {"status": "error", "message": "; ".join(errors)}
    return {"status": "confirmed", "message": "Building characteristics saved."}
