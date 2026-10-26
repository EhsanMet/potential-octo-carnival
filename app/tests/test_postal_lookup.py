import io
import json
import urllib.error
import urllib.request

import pytest

from services.postal_lookup import lookup_postal_code

# Real responses from api.zippopotam.us, recorded on 2026-10-22.
BERLIN_10115 = {
    "country": "Germany",
    "country abbreviation": "DE",
    "post code": "10115",
    "places": [
        {"place name": "Berlin", "longitude": "13.3922", "latitude": "52.532", "state": "Berlin", "state abbreviation": "BE"}
    ],
}
DRESDEN_01067 = {
    "country": "Germany",
    "country abbreviation": "DE",
    "post code": "01067",
    "places": [
        {"place name": "Dresden", "longitude": "51.05", "latitude": "14612", "state": "Sachsen", "state abbreviation": "SN"},
        {"place name": "Dresden Friedrichstadt", "longitude": "51.0587", "latitude": "14612", "state": "Sachsen", "state abbreviation": "SN"},
    ],
}


def fake_urlopen(monkeypatch, body=None, error=None, answers=None):
    # `answers` maps a URL to its own body or exception; other URLs get `body` / `error`.
    requested = []

    def urlopen(url, timeout):
        requested.append(url)
        answer = (answers or {}).get(url, error or body)
        if isinstance(answer, BaseException):
            raise answer
        return io.BytesIO(answer if isinstance(answer, bytes) else json.dumps(answer).encode())

    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    return requested


def http_error(code):
    return urllib.error.HTTPError("https://api.zippopotam.us/de/x", code, "error", {}, io.BytesIO(b"{}"))


# A known postal code returns the first place, with coordinates as numbers.
def test_found_returns_place_and_coordinates(monkeypatch):
    fake_urlopen(monkeypatch, BERLIN_10115)
    assert lookup_postal_code(10115) == {
        "status": "found",
        "post_code": "10115",
        "place": "Berlin",
        "state": "Berlin",
        "latitude": 52.532,
        "longitude": 13.3922,
    }


# Zippopotam returns swapped/broken coordinates for some German codes; they are dropped.
def test_broken_coordinates_are_dropped(monkeypatch):
    fake_urlopen(monkeypatch, DRESDEN_01067)
    result = lookup_postal_code(1067)
    assert result["status"] == "found"
    assert result["place"] == "Dresden"
    assert result["latitude"] is None
    assert result["longitude"] is None


# The form turns "01067" into 1067; the request must use the 5-digit code.
def test_leading_zero_is_restored(monkeypatch):
    requested = fake_urlopen(monkeypatch, DRESDEN_01067)
    lookup_postal_code(1067)
    assert requested == ["https://api.zippopotam.us/de/01067"]


# An unknown postal code comes back as 404 with an empty body. It only counts as "not found"
# if the known code 10115 is still found afterwards.
def test_unknown_postal_code_is_not_found(monkeypatch):
    requested = fake_urlopen(
        monkeypatch,
        answers={
            "https://api.zippopotam.us/de/12340": http_error(404),
            "https://api.zippopotam.us/de/10115": BERLIN_10115,
        },
    )
    assert lookup_postal_code(12340) == {"status": "not_found"}
    assert requested == ["https://api.zippopotam.us/de/12340", "https://api.zippopotam.us/de/10115"]


# If the known code fails too, the 404 means the service (or our request) is broken, not the code.
@pytest.mark.parametrize("known_code_answer", [http_error(404), TimeoutError("timed out"), {}])
def test_404_with_broken_service_is_unavailable(monkeypatch, known_code_answer):
    fake_urlopen(
        monkeypatch,
        answers={
            "https://api.zippopotam.us/de/12340": http_error(404),
            "https://api.zippopotam.us/de/10115": known_code_answer,
        },
    )
    assert lookup_postal_code(12340) == {"status": "unavailable"}


# Any other failure means the lookup is unavailable, not that the code is wrong.
@pytest.mark.parametrize(
    "error",
    [http_error(500), urllib.error.URLError("no network"), TimeoutError("timed out")],
)
def test_failures_are_unavailable(monkeypatch, error):
    fake_urlopen(monkeypatch, error=error)
    assert lookup_postal_code(10115) == {"status": "unavailable"}


@pytest.mark.parametrize("body", [b"not json", {}, {"places": []}])
def test_unexpected_answers_are_unavailable(monkeypatch, body):
    fake_urlopen(monkeypatch, body)
    assert lookup_postal_code(10115) == {"status": "unavailable"}
