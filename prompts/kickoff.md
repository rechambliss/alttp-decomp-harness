# Kickoff prompt (scheduled or manual)

Paste everything below the line into a fresh session that has both repos checked out side by side.

---

You are running one session of the ALttP Rust decomp.

Session label: `{{LABEL}}` (e.g. `run-2026-10-11-a`)
Role: `{{ROLE}}` (orchestrator | cartographer | translator | verifier | reviewer)
Unit limit: `{{N}}` (orchestrator: max units to plan per role; other roles: always 1)

Setup (skip anything already present):
- Attach and clone these three private repos side by side in one parent folder, one at a time:
  `rechambliss/alttp-decomp-harness`, `rechambliss/alttp-recomp`, `rechambliss/alttp-rom`.
- `export ALTTP_ROM=<parent>/alttp-rom/alttp-eu.sfc`
- Never copy the ROM or its bytes into the other two repos.

Steps:
1. `cd alttp-decomp-harness` and read `CLAUDE.md`, then `agents/{{ROLE}}.md`. Read nothing else up front.
2. Orchestrator: follow your role file, then stop.
   Other roles: open `ledger/RUN.md`, take the first unit listed for your role whose `owner` is `{{LABEL}}` or empty, and set `owner` to `{{LABEL}}`.
   If none, run `python3 scripts/ledger.py next --role {{ROLE}}` and take the first one.
   If still none, report "no work for {{ROLE}}" and stop.
3. Do the unit per your role file. One unit only.
4. Run the finish checklist in `CLAUDE.md`.
5. Commit in both repos with the unit id in the message.
6. End with a 3-line summary: the unit, its new status and anything blocked.
