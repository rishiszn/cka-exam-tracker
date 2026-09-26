# CKA Exam Tracker

A Streamlit reproduction of the "Ultimate CKA" Excel progress tracker —
same 5 categories, same 40 topics, same weights, same status workflow
(Yet to Start / WIP / Done), rebuilt as an interactive local app with
persistent SQLite storage.

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the URL Streamlit prints (usually `http://localhost:8501`).

## Project structure

```
cka-tracker/
├── app.py          # UI + layout + calculations, generated from data.py
├── data.py         # Categories, topics, weights, colors (the single source of truth)
├── database.py      # SQLite persistence (topic_id, name, status, last_updated)
├── styles.py        # All CSS for the spreadsheet look
├── requirements.txt
├── README.md
└── cka_tracker.db   # created automatically on first run
```

## What's in it

- All 40 topics across the 5 official categories, weighted 25 / 15 / 20 / 10 / 30%.
- A status dropdown per topic (Yet to Start / WIP / Done), color-coded exactly
  like the sheet (cyan → orange → bold green), that updates instantly — no save button.
- SQLite-backed persistence: close the app, reopen it, your progress is still there.
- Overall progress, per-category progress, and the exam-weighted progress
  (`Σ category_progress × category_weight`), all recalculated live.
- The bottom "Done with Concepts, Demos, and Practice?" / "Ready to get your
  CKA Cert?" readout, driven by the same live numbers (thresholds in `data.py`:
  0–49% Not Yet, 50–79% Almost, 80–99% Nearly Ready, 100% Ready).
- Search box, status filter, and CKA/CKA & CKAD exam filter — instant, no page reload.
- CSV export and re-import of your progress.
- Reset Progress button with a required Yes/Cancel confirmation step.

## A note on the one place this departs from a literal pixel copy

Excel's status cells are dropdowns *inside* spreadsheet cells. Streamlit can't
put a live, interactive widget inside an HTML `<table>` cell, so each
category is rendered as two aligned pieces: the left side is a real HTML
table (row-numbered, with the category name spanning its rows exactly like
the merged cell in Excel, colored to match) showing the *current* status in
the same color coding as the sheet; a slim "Edit" column right next to it
holds the actual interactive dropdown you use to change that status. Change
it there and the colored status shown in the table — plus every progress
number on the page — updates immediately.

## Customizing

- Add/edit topics or categories: `data.py` (`CATEGORIES` list) — the UI,
  progress math, and CSV export all regenerate from this automatically.
- Change readiness thresholds: `data.py` → `READINESS_THRESHOLDS`.
- Change colors: `data.py` (category `color`, `STATUS_COLOR`) or `styles.py`.
