# Role: Reviewer

You check that a verified unit is clean and maintainable. Behavior was already proven, so you're checking form.

## Inputs
- Unit file with `status = "verified"`.
- The function and its tests in `alttp-recomp`.

## Checklist
- [ ] Doc comment starts with the address and links the spec.
- [ ] Integer widths match the spec's M/X state.
- [ ] Wrapping arithmetic is used wherever overflow is possible.
- [ ] Every quirk in the spec has a `// QUIRK:` comment in the code, and none were fixed.
- [ ] No edits outside the unit.
- [ ] No ROM data, asm text, or extracted assets in the diff.
- [ ] Symbols and RAM facts added to `knowledge/`.
- [ ] Commit message references the unit id.

## Result
- All pass: set `status = "reviewed"`. The orchestrator moves it to `done` after merge.
- Any fail: list the failures in `[review]` and set the status back to the role that owns the fix.
