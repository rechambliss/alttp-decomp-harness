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
   Other roles: run `python3 scripts/ledger.py claim --role {{ROLE}} --label {{LABEL}}`.
   It prints the one unit to work on and sets its owner. Work on that unit and no other.
   If it prints `none`, report "no work for {{ROLE}}" and stop.
   If the unit is `mapped` rather than `unmapped`, your job is the spec step, not the map step.
3. Do the unit per your role file. One unit only.
4. Run the finish checklist in `CLAUDE.md`.
5. Commit in `alttp-decomp-harness` with the unit id in the message. Commit in `alttp-recomp` only if you changed files there. Never make an empty commit. Push what you committed.
6. End with a 3-line summary: the unit, its new status and anything blocked.
