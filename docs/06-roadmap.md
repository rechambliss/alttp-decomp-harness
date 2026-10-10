# Roadmap

## Phase 0: Tooling (before any unit work)
- Settle O-001 (reference emulator) and O-002 (disassembler).
- ROM loader with hash check and LoROM mapping. Done in `alttp-recomp/crates/alttp-rom`.
- A local disassembly dump command: `dump <address-range>` prints M/X-aware 65816 for one unit.
- Routine-level differential runner: load state, run to return, diff WRAM and hardware writes.
- Capture tooling: save gameplay states and extract the WRAM present at routine entry.

Exit criteria: one trivial routine goes through the whole pipeline end to end.

## Phase 1: Skeleton
- Map the reset, NMI, and IRQ units and the main loop's module dispatcher (a jump table).
- This produces the first wave of callee units, and the ledger fills out from here.

## Phase 2: Bottom-up translation
- Leaves first. The ledger's `next` command feeds roles.
- Frame-level diffing switches on once the main loop and NMI are translated.

## Phase 3: Platform
- Renderer, audio, and input on desktop.
- An asset extraction step that writes to a local cache.
- A theme pack loader.

## Phase 4: Mobile
- Android and iOS shells, touch controls, controller support, save handling.

## Phase 5: Cleanup
- Idiomatic refactors, one field or routine at a time, with the diff harness still green.
