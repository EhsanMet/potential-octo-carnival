import html

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


VALID_BILL = {
    "energy_carrier": "Gas",
    "start_date": "2025-01-01",
    "end_date": "2025-12-31",
    "consumption_kwh": "12000",
    "total_cost": "1234,56",
}


def test_valid_bill_shows_confirmation():
    response = app.test_client().post("/bill", data=VALID_BILL)
    assert b"Utility bill saved." in response.data


def test_short_billing_period_shows_error():
    response = app.test_client().post("/bill", data={**VALID_BILL, "end_date": "2025-03-31"})
    assert b"Billing period must be 6 months to 3 years" in response.data


def test_cost_with_three_decimals_shows_error():
    response = app.test_client().post("/bill", data={**VALID_BILL, "total_cost": "12,345"})
    assert b"Total cost must be more than 0" in response.data


def test_nav_links_both_pages():
    response = app.test_client().get("/bill")
    assert b'href="/"' in response.data
    assert b'href="/bill"' in response.data


def test_valid_submit_shows_location():
    response = app.test_client().post("/", data=VALID_FORM)
    assert "📍 10115 Berlin, Berlin" in response.get_data(as_text=True)
    assert b"52.532, 13.3922" in response.data


def test_unknown_postal_code_shows_error_and_does_not_save(monkeypatch):
    import app as app_module

    monkeypatch.setattr(app_module, "lookup_postal_code", lambda zip_code: {"status": "not_found"})
    response = app.test_client().post("/", data=VALID_FORM)
    assert b"Building characteristics saved." not in response.data
    assert "This postal code doesn't exist." in html.unescape(response.get_data(as_text=True))


# When Zippopotam is unavailable, the local check is the backup: the form still saves.
def test_lookup_unavailable_saves_with_backup_note(monkeypatch):
    import app as app_module

    monkeypatch.setattr(app_module, "lookup_postal_code", lambda zip_code: {"status": "unavailable"})
    response = app.test_client().post("/", data=VALID_FORM)
    assert b"Building characteristics saved." in response.data
    assert "couldn't verify this postal code right now" in response.get_data(as_text=True)


def test_locally_invalid_zip_does_not_call_lookup(monkeypatch):
    import app as app_module

    calls = []
    monkeypatch.setattr(app_module, "lookup_postal_code", lambda zip_code: calls.append(zip_code))
    response = app.test_client().post("/", data={**VALID_FORM, "zip_code": "999999"})
    assert calls == []
    assert b"Zip code must be a valid German postal code." in response.data


def test_unknown_zip_error_shows_together_with_other_errors(monkeypatch):
    import app as app_module

    monkeypatch.setattr(app_module, "lookup_postal_code", lambda zip_code: {"status": "not_found"})
    response = app.test_client().post("/", data={**VALID_FORM, "area": "abc"})
    page = html.unescape(response.get_data(as_text=True))
    assert "This postal code doesn't exist." in page
    assert "Area must be a whole number" in page
