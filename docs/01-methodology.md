# Methodology

## Ground truth

The original ROM running in a reference emulator is the only ground truth.
Not documentation, not community notes, not an agent's reading of the assembly.
If the Rust and the emulator disagree, the Rust is wrong until proven otherwise.

## Core design choice: keep the original memory layout

Translated code reads and writes a `Wram` struct that is a 128 KiB byte array, addressed exactly like SNES WRAM ($7E:0000 to $7F:FFFF).
Typed accessors and named constants sit on top, but the bytes stay where the original put them.

Why:
- Diffing against the emulator is a byte compare. No mapping layer to get wrong.
- Save states, glitches, and timing quirks keep working.
- Refactoring into idiomatic structs happens later, one field at a time, with the diff harness catching mistakes.

Hardware registers (PPU, DMA, APU ports) are written to a `Hw` struct that records writes in order, so register traffic can be diffed too.

## Unit of work

A unit is one routine: one entry address through every path to its returns (`RTS`, `RTL`, `RTI`), or to a tail jump into another routine.

Split a routine into several units when:
- It is longer than about 300 instructions.
- It contains a jump table. The dispatcher is one unit, and each target is its own unit.

Merge into one unit when:
- A routine is under about 20 instructions and has exactly one caller. Fold it into the caller's unit and note it.

## Pipeline per unit

1. **Map** (cartographer): find the routine's bounds, entry M/X register widths, callers, callees, jump tables. Add symbols. Status becomes `mapped`.
2. **Spec** (cartographer): write the unit spec. This covers inputs (registers, WRAM, flags), outputs, side effects, hardware writes and quirks. Status becomes `specced`.
3. **Translate** (translator): write the Rust function from the spec and the asm. Unit tests come from the spec. Status becomes `translated`.
4. **Verify** (verifier): run the differential test. Status becomes `verified`, or goes back to `translated` with a failure report.
5. **Review** (reviewer): check conventions, naming, and that quirks are documented and not fixed. Status becomes `reviewed`, then `done` once merged.

Each step is a separate session. The verifier never sees the translator's reasoning, only the code and the spec. That keeps the work from grading itself.

## Differential testing, two levels

**Routine level (available from day one).**
1. Load a WRAM snapshot and CPU register state into the emulator.
2. Set PC to the routine's entry and run until it returns.
3. Snapshot WRAM and the hardware write log.
4. Load the same starting state into Rust and call the function.
5. Compare. Any byte difference is a failure, unless the spec lists it as scratch.

Starting states come from real gameplay: record save states at many points, and sample the WRAM present when the routine is entered.
Each unit needs at least 3 distinct starting states, more if it has many branches.

**Frame level (once the main loop is translated).**
- Replay recorded input in both, and compare WRAM at the end of every frame.
- This catches ordering and interaction bugs that routine tests miss.

## Bottom-up order

Translate leaves first, meaning routines that call nothing untranslated.
`scripts/ledger.py next` only offers a unit for translation when all its callees are at least `translated`.
Until then, a call to an untranslated routine is a hard error in tests, never a silent stub.

## Variable register width

65816 code changes accumulator and index width with `REP` and `SEP`.
The cartographer records the M/X state at the entry and at each label in the spec.
The translator uses `u8` or `u16` to match, and never guesses.
A width mismatch is the most likely bug class, so the verifier should prioritize states that hit both widths.

## When something is unclear

Write the question in the unit's `notes`, set `blocked`, and stop.
A blocked unit costs one session. A wrong guess that passes review costs many.
