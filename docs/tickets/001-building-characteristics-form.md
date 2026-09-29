# 001 — Building characteristics input form

## Scope

Minimal field set only, front-end only:

- Square footage
- Year built
- Heating system type
- Location / postal code

Inline (per-field, real-time) validation on each field.

Captured/validated data is held in memory and handed to the next step. No backend, no API,
no persistence in this ticket.

## Why this scope

Kept small and actionable on purpose, to avoid scope creep on a first slice. Extended fields
(insulation, windows, roof type, occupancy) and persistence were deliberately deferred rather
than bundled in here.

## Open assumptions — confirm before building

- Square footage unit (sq ft vs. m²) not decided.
- Year-built valid range is a placeholder.
- Heating-system-type enum list is a placeholder, not yet matched to what the suggestion logic
  can act on.
- Postal code format/locale assumed as a single country, not confirmed.
- No data contract yet exists between this form and the suggestion engine, or with a separate
  bill-entry ticket.
