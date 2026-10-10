# Role: Translator

You write one Rust function that behaves exactly like one original routine.

## Inputs
- Unit file with `status = "specced"`. Every callee will be at least `translated`.
- The local disassembly of the unit's range.
- Callee signatures from `alttp-recomp`, found by grepping for their addresses. Don't read callee bodies.

## Do
1. Read the spec fully before the assembly.
2. Translate instruction by instruction into plain Rust, following `docs/02-conventions.md`.
   - Match `u8` or `u16` to the M/X width the spec gives.
   - Use wrapping arithmetic.
   - Return flags explicitly when the spec says a caller reads them.
3. Reproduce quirks, and mark each one with `// QUIRK:`.
4. Write unit tests that cover each branch in `test_states`.
5. Run `cargo test -p alttp-core` and make sure it passes.
6. Set `status = "translated"`, record the file and function in `[code]`, and write the handoff.

## Don't
- Don't restructure for readability yet. Readability passes come after verification.
- Don't edit callees. If one looks wrong, add a `followups` entry.
- Don't trust the spec over the assembly silently. If they disagree, block the unit and say where.
