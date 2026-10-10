# Current run

Label: `run-2026-10-10-b`
Planned by: orchestrator, 2026-10-10

## Cartographer (one unit per session, in this order)
1. `00803b` sub_00803b (followup from 008000: possibly dead bytes $00:803B-$8050)
2. `0080b5` sub_0080b5 (module dispatcher)
3. `00841e` sub_00841e

Still owned by `run-2026-10-10-a` (claimed today, not stale): `0080c9` NMI, `0082d8` IRQ.

## Translator
None ready. `008000` Reset is specced, but its callees are not `translated` yet.

## Verifier
None ready. Also blocked on O-001 (reference emulator).

## Reviewer
None ready.

## Blocked on open decisions
- O-001 reference emulator: blocks every verifier session.
- O-004 PAL vs NTSC timing: not blocking yet. It's needed before frame-level work.
