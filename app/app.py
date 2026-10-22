from flask import Flask, render_template, request

from services.postal_lookup import lookup_postal_code
from validators.bill import ENERGY_CARRIERS, parse_cost, parse_date, validate_utility_bill
from validators.building import HEATING_TYPES, WINDOW_TYPES, validate_building_characteristics

app = Flask(__name__)

FIELDS = ["zip_code", "area", "building_age", "heating_type", "windows_type"]
BILL_FIELDS = ["energy_carrier", "start_date", "end_date", "consumption_kwh", "total_cost"]


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
        zip_code = _to_int(values["zip_code"])
        result = validate_building_characteristics(
            zip_code=zip_code,
            area=_to_int(values["area"]),
            building_age=_to_int(values["building_age"]),
            heating_type=values["heating_type"],
            windows_type=values["windows_type"],
        )
        # The lookup only adds information; it never blocks saving.
        if result["status"] == "confirmed":
            result["location"] = lookup_postal_code(zip_code)
    return render_template(
        "building_form.html",
        values=values,
        result=result,
        heating_types=HEATING_TYPES,
        window_types=WINDOW_TYPES,
    )


@app.route("/bill", methods=["GET", "POST"])
def bill_form():
    values = {field: request.form.get(field, "") for field in BILL_FIELDS}
    result = None
    if request.method == "POST":
        result = validate_utility_bill(
            energy_carrier=values["energy_carrier"],
            start_date=parse_date(values["start_date"]),
            end_date=parse_date(values["end_date"]),
            consumption_kwh=_to_int(values["consumption_kwh"]),
            total_cost=parse_cost(values["total_cost"]),
        )
    return render_template(
        "bill_form.html",
        values=values,
        result=result,
        energy_carriers=ENERGY_CARRIERS,
    )


if __name__ == "__main__":
    app.run(debug=True)
