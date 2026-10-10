# Goals and scope

## Goal

A Rust reimplementation of ALttP (EU) that behaves identically to the original, runs natively on desktop, Android, and iOS, and loads its graphics, text, and audio from data files so alternate theme packs can replace them.

## In scope

- Game logic for every routine reachable from the reset, NMI, and IRQ vectors.
- A renderer that turns PPU state into a framebuffer.
- An asset layer that extracts from the player's own ROM at build or first-run time.
- A theme pack format that overrides extracted assets without code changes.
- A differential test harness that proves equivalence against the original.

## Out of scope (for now)

- Gameplay changes, enhancements, or bug fixes. Those come after the faithful build, behind flags.
- Other regions or revisions. EU only until the core is done.
- Online features.

## Definition of done for the project

- Every routine in the ledger is `done`.
- A full playthrough input recording replays with WRAM identical to the original at every frame.
- Desktop, Android, and iOS builds run that recording.

## Downstream

A Halloween theme pack is planned as a separate fork/pack. It changes assets and text only, never code. Keep the asset layer clean enough that a pack can replace any graphic, palette, string, or song by id.
