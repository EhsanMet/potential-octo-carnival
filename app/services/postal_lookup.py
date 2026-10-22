import json
import urllib.error
import urllib.request

API_URL = "https://api.zippopotam.us/de/{}"

# Rough bounding box of Germany. Zippopotam often returns swapped or broken coordinates for
# German codes (e.g. 01067: longitude "51.05", latitude "14612"), so anything outside is dropped.
LATITUDE_RANGE = (47.0, 55.1)
LONGITUDE_RANGE = (5.8, 15.1)


def _parse_coordinate(text, low, high):
    try:
        value = float(text)
    except (TypeError, ValueError):
        return None
    return value if low <= value <= high else None


def lookup_postal_code(zip_code, timeout=3):
    # The form turns "01067" into 1067; the API needs the 5-digit code.
    post_code = f"{zip_code:05d}"
    try:
        with urllib.request.urlopen(API_URL.format(post_code), timeout=timeout) as response:
            data = json.load(response)
        place = data["places"][0]
    except urllib.error.HTTPError as error:
        return {"status": "not_found"} if error.code == 404 else {"status": "unavailable"}
    except (OSError, ValueError, KeyError, IndexError, TypeError):
        return {"status": "unavailable"}

    return {
        "status": "found",
        "post_code": post_code,
        "place": place.get("place name"),
        "state": place.get("state"),
        "latitude": _parse_coordinate(place.get("latitude"), *LATITUDE_RANGE),
        "longitude": _parse_coordinate(place.get("longitude"), *LONGITUDE_RANGE),
    }
