from flask import Flask, render_template, request

from validators import HEATING_TYPES, WINDOW_TYPES, validate_building_characteristics

app = Flask(__name__)

FIELDS = ["zip_code", "area", "building_age", "heating_type", "windows_type"]


def _to_int(text):
    try:
        return int(text)
    except ValueError:
        return None


@app.route("/", methods=["GET", "POST"])
def building_form():
    values = {field: request.form.get(field, "") for field in FIELDS}
    result = None
    if request.method == "POST":
        result = validate_building_characteristics(
            zip_code=_to_int(values["zip_code"]),
            area=_to_int(values["area"]),
            building_age=_to_int(values["building_age"]),
            heating_type=values["heating_type"],
            windows_type=values["windows_type"],
        )
    return render_template(
        "form.html",
        values=values,
        result=result,
        heating_types=HEATING_TYPES,
        window_types=WINDOW_TYPES,
    )


if __name__ == "__main__":
    app.run(debug=True)
