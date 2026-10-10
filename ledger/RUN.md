# Current run

Label: `run-2026-10-10-a`
Planned by: orchestrator, 2026-10-10

## Cartographer (one unit per session, in this order)
1. `008000` Reset
2. `0080c9` NMI
3. `0082d8` IRQ

## Translator
None ready. Nothing is `specced` yet.

## Verifier
None ready. Also blocked on O-001 (reference emulator).

## Reviewer
None ready.

## Blocked on open decisions
- O-001 reference emulator: blocks every verifier session.
- O-004 PAL vs NTSC timing: not blocking yet. It's needed before frame-level work.
