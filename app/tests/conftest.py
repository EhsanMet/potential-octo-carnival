import pytest

import app as app_module

BERLIN = {
    "status": "found",
    "post_code": "10115",
    "place": "Berlin",
    "state": "Berlin",
    "latitude": 52.532,
    "longitude": 13.3922,
}


# Keep the test suite offline: the building form would otherwise call the real postal-code API.
@pytest.fixture(autouse=True)
def stub_postal_lookup(monkeypatch):
    monkeypatch.setattr(app_module, "lookup_postal_code", lambda zip_code: BERLIN)
