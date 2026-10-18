# Utility Bill Entry Form — Spec

## Overview

This feature is a data entry form for the user's energy bill. Together with the building
characteristics (ticket 001), it is the input the suggestion engine will work from.

It gets the bill data from the user and makes sure it is valid. For example, the billing period is
between 6 months and 3 years, and the cost is a euro amount with at most 2 decimals.

## Interface

Several entry boxes dedicated to each one of:

- Energy carrier (drop-down)
- Billing period start date
- Billing period end date
- Consumption (kWh)
- Total cost (€)

## Validation rules

- Energy carrier must be chosen from the drop-down list: Electricity, Gas, Oil, District heating,
  Wood/pellets, Other. These match the building form's heating types.
- Start and end date must both be valid dates.
- The billing period counts both days, so 01.01. to 31.12. is 12 months. It must be at least
  6 months and at most 36 months (3 years).
- The end date must be after the start date and not in the future.
- Consumption must be a whole number from 1 to 300,000 kWh, as printed on the bill.
- Total cost must be more than 0 and at most 50,000 €, with at most 2 decimals. Both a decimal
  comma (`1234,56`) and a decimal dot (`1234.56`) are accepted; thousands separators are not.

## Prerequisites

None. This page does not depend on the building form yet.

## After this step

The data for these entries will get their new value. Linking it with the building data is a later
ticket.

## Error / confirmation behavior

- If the inputs are wrong and don't match the specification, the user should see an error under
  each wrong field to correct their input.
- If the inputs are right, show the confirmation message "Utility bill saved."

## Known limitations

- Energy use is seasonal. A short bill (e.g. 6 months over summer) understates yearly heating, so
  converting it to a year by simple scaling is only an estimate.
- Consumption is stored as printed, not converted to a year. The billing period is kept so the
  suggestion engine can do that conversion later.
