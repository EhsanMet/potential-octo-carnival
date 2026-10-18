from app import app

VALID_FORM = {
    "zip_code": "01067",
    "area": "120",
    "building_age": "50",
    "heating_type": "Gas",
    "windows_type": "2 layers",
}


def test_valid_submit_shows_confirmation():
    response = app.test_client().post("/", data=VALID_FORM)
    assert b"Building characteristics saved." in response.data


def test_non_number_area_shows_error():
    response = app.test_client().post("/", data={**VALID_FORM, "area": "abc"})
    assert b"Area must be a whole number" in response.data
