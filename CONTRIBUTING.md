# Contributing

Thanks for considering contributing! This project is a small Clash Royale progression calculator that uses the official Clash Royale API and local progression tables.

## Ground Rules

- **Do not commit secrets**: never commit your Clash Royale API token, screenshots that include it, or any personal data.
- Keep changes **focused**: one bugfix/feature per PR when possible.
- Prefer **small, readable** changes over large refactors.
- Keep UI changes accessible: good contrast, readable fonts, no tiny click targets.

## Prerequisites

- **Python**: originally built for Python 3.9, should work on newer versions too.
- **Dependencies**: `requests` (UI uses Tkinter, which is included with standard Python on Windows/macOS).

Install dependencies:

```bash
pip install requests
```

## Running Locally

### UI

```bash
python clashroyaleUI.py
```

### CLI

```bash
python API.py
```

## Project Layout

- `clashroyaleUI.py` — Tkinter UI (connect → calculate).
- `API.py` — API calls + table loading + (legacy) CLI logic.
- `Account.py`, `Card.py` — simple data models.
- `exp_table.txt` — King Level XP thresholds (level → XP to next → cumulative).
- `card_required_table.txt` — card copies required per level/rarity.
- `upgrade_table.txt` — gold required per upgrade level/rarity.
- `upgrade_table_exp.txt` — XP gained per upgrade level/rarity.

## Updating for New Game Patches

Supercell occasionally changes progression. When that happens, updates usually involve:

1. Updating the `*.txt` tables (XP thresholds, card requirements, gold costs, upgrade XP).
2. Adjusting the level caps and rarity mapping in code if the API changes per-rarity `maxLevel` values.

If you’re proposing a progression update, please include:

- A link to the official patch notes/source.
- The updated table data.
- A brief explanation of what changed and why.

## Code Style & Quality

- Keep functions short and name variables clearly.
- Avoid introducing new dependencies unless necessary.
- Prefer `requests.Session()` reuse for HTTP calls (already used in the UI).
- Keep computation logic deterministic and avoid relying on UI state where possible.

## Git Hygiene

- Do not commit Python cache files:
  - `__pycache__/`
  - `*.pyc`
- If you accidentally committed them, remove from Git history in your branch before opening a PR.

## Reporting Bugs / Requesting Features

When opening an issue, please include:

- What you expected vs what happened
- Steps to reproduce
- Your OS + Python version (`python --version`)
- Any traceback/error message (remove tokens!)

## Pull Request Checklist

Before you open a PR:

- [ ] `python -m py_compile API.py clashroyaleUI.py` succeeds
- [ ] No secrets committed (tokens, IPs, personal data)
- [ ] No `__pycache__/` or `*.pyc` files tracked
- [ ] UI changes are readable and don’t break basic flow (Connect → Calculate)
- [ ] Tables remain consistent (levels align across all `*.txt` files)

## Security

If you believe you’ve found a security issue (e.g., token leakage), please **do not open a public issue**. Instead, contact the maintainer privately with details and reproduction steps.

