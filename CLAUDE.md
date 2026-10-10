# Agent entry point

You are one agent in a multi-session effort to decompile ALttP (EU) into Rust.
Keep your context small. Read only what is listed here for your role.

## Read order

1. This file.
2. Your role file in `agents/` (named in your task card or kickoff prompt).
3. Your task card in `ledger/units/<unit-id>.toml` and anything it links.
4. Grep `knowledge/` for the specific symbols or addresses you need. Do not read those files whole.

Do not read `docs/` unless your role file or task card points you at a specific section.

## Hard rules

- Never commit ROM bytes, extracted assets, or disassembly listings. Addresses, names, and your own notes are fine.
- Work one unit at a time. Do not start a second unit in the same session.
- Faithful first: reproduce original behavior exactly, including bugs and quirks. Note quirks, do not fix them.
- Write results to files. Chat output is lost between sessions.
- Update the unit's ledger file before you finish: status, notes, handoff.
- If blocked, set `status = "blocked"`, write why in `blocked_reason`, and stop. Do not guess past a blocker.
- Do not change code outside the unit you own. If a callee or shared type needs changing, record it in `followups`.

## Status flow

`unmapped -> mapped -> specced -> translated -> verified -> reviewed -> done`

Any state can go to `blocked`. Verification failure sends a unit back to `translated` with notes.

## Repos

- `../alttp-decomp-harness` (this repo): process, ledger, knowledge.
- `../alttp-recomp`: Rust code and tests.

## Finish checklist

- [ ] Ledger file updated (status, owner cleared, handoff filled).
- [ ] New symbols added to `knowledge/symbols.toml`.
- [ ] New RAM facts added to `knowledge/ram-map.md`.
- [ ] `python3 scripts/ledger.py validate` passes.
- [ ] The harness commit references the unit id. Commit in recomp only if you changed code there, and never make an empty commit.
