# 002 — Utility bill entry form

## Scope

A separate page (`/bill`) in the shared app with four fields:

- Energy carrier
- Billing period (start and end date)
- Consumption (kWh)
- Total cost (€)

Validation on Save, with an error under each wrong field and a confirmation message when all
fields are right. Same look as the building form (shared `base.html`).

No persistence and no link to the building form in this ticket.

## Why this scope

The suggestion engine needs bill data, but connecting the steps (passing data between pages via a
session) is its own decision. It is deferred to a later ticket so this one stays small. The data
is entered by hand; uploading a bill file was rejected for now (fragile parsing, personal data).

## Open assumptions — confirm before building

- The 300,000 kWh ceiling is a placeholder, sized for a 3-year bill of a large house.
- The 50,000 € ceiling is a placeholder.
- The end date may not be in the future (a bill is issued after its period).
- Thousands separators in the cost (e.g. `1.234,56`) are not accepted.
