# Energy Audit Platform

_For the Coding with AI course_

## Problem

"My bill is expensive and the options are too complex to compare."

## MVP concept

A web app that takes the user's utility bill and their building's characteristics, and
suggests improvements based on them.

## Status

Ticket 001 (building characteristics form, `/`) and ticket 002 (utility bill entry, `/bill`) are
implemented as one small Flask app, sharing the same look (floating labels, round Save button) and
a nav link between the pages. The app code lives in `app/`; `docs/tickets/` holds only the ticket
and spec documents.

Not built yet: the improvement-suggestion engine, and saving data between steps.

## Running it

```
pip install -r requirements.txt
cd app
python -m pytest
python app.py
```

Then open http://127.0.0.1:5000.

## Tickets

- [001 — Building characteristics input form](docs/tickets/001-building-characteristics-form/ticket.md)
- [002 — Utility bill entry form](docs/tickets/002-utility-bill-entry/ticket.md)
