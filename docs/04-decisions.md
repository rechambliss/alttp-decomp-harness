# Decisions

Each decision gets an id. Open ones need Riley's call before work that depends on them starts.

## Decided

**D-001 Faithful first.** Reproduce the original exactly, quirks included. Improvements come later, behind flags.

**D-002 Original WRAM layout.** Translated code operates on a 128 KiB byte array that matches SNES WRAM. See methodology.

**D-003 Two repos.** The harness repo holds process, ledger, and knowledge. The recomp repo holds code. The Halloween version is a theme pack on the same engine, not a code fork.

**D-004 SNES-accurate assets.** Theme packs use the original tile sizes, frame counts, and 16-color palettes, so a pack can be tested in the ROM before the port runs.

**D-005 Targets.** Desktop first, for development and verification. Android and iOS follow.

**D-006 Ledger is one file per unit.** This avoids merge conflicts when agents run in parallel.

**D-007 In-house disassembler (closes O-002).** `alttp-recomp/tools/alttp-disasm` is a flow-following, M/X-aware 65816 disassembler. It prints the `[map]` block for a unit's ledger file. Its output is local only.

## Open

**O-001 Reference emulator for differential tests.**
It needs to support loading WRAM and CPU state, running to a return, snapshotting, and logging hardware writes.
Options: embed an existing SNES core through bindings, or write a minimal 65816 interpreter for routine-level tests only.
A minimal interpreter is enough for routine-level work, since most routines touch only WRAM. Frame-level work needs a full core.

**O-003 Community references.**
Whether agents may consult public ALttP disassemblies and RAM maps for names and hints.
If yes, record each source and its license here, and still verify every fact against the emulator.

**O-004 PAL vs NTSC timing.**
The EU ROM runs at 50 Hz, and some game timing may differ from the US version.
Decide whether the port runs at 50 Hz to match the dump, or targets 60 Hz, which would need a US ROM as a second reference.

**O-005 Audio.**
Options: emulate the SPC700 and DSP and feed it the original sound driver and data, or reimplement the driver.
Emulation is much less work and fully faithful. Reimplementation is cleaner for theme packs that replace music.

**O-006 Renderer.**
Options: a PPU-accurate software renderer, or a tile renderer that only supports what the game uses. Pick a graphics backend for mobile as well.

**O-007 Scheduling.**
How often scheduled sessions run, which roles they run, and how many units each session takes.
