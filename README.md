# alttp-decomp-harness

Process, planning, and source of truth for decompiling *The Legend of Zelda: A Link to the Past* (EU, SNES) into Rust.

The code lives in a separate repo: `alttp-recomp`.
This repo holds the method, the agent instructions, and the ledger that tracks every unit of work.

## What lives here

| Path | Purpose |
|---|---|
| `CLAUDE.md` | Entry point for every agent session. Read first, always. |
| `docs/` | Goals, methodology, conventions, legal hygiene, decisions, token budget. |
| `agents/` | One short role file per agent type. An agent reads only its own. |
| `templates/` | Task card, unit spec, handoff note. |
| `ledger/units/` | One TOML file per unit of work. The single source of truth for status. |
| `knowledge/` | Shared facts: ROM layout, RAM map, symbol table. Grep it, never read it whole. |
| `prompts/` | Kickoff prompts for scheduled and manual sessions. |
| `scripts/ledger.py` | Status report, next-unit picker, ledger validator. |

## Quick start

```sh
python3 scripts/ledger.py status      # where the project stands
python3 scripts/ledger.py next        # next units ready for each role
python3 scripts/ledger.py validate    # check ledger integrity
```

To run many units back to back, paste `prompts/driver.md` into one Claude Code session. It starts a fresh subagent per unit, one at a time.

To run a single session by hand, paste `prompts/kickoff.md` into a fresh agent session with both repos checked out side by side:

```
work/
  alttp-decomp-harness/
  alttp-recomp/
```

## Ground rules

- No ROM bytes, no extracted assets, no copied disassembly text in either repo. See `docs/03-legal-hygiene.md`.
- Faithful first. Translated code reproduces the original exactly, bugs included, before anyone cleans it up.
- Nothing is done until it is verified against the original running in an emulator.
