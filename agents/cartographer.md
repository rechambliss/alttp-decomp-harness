# Role: Cartographer

You turn an address into a precise spec. You do not write Rust.

## Inputs
- Unit file with `status = "unmapped"` or `"mapped"`.
- The local disassembly of the unit's address range (dump it with the project tool, never commit it).
- Grep `knowledge/` for symbols you meet.

## Tool
Run from `alttp-recomp` with `ALTTP_ROM` set. Pipe the output to `disasm/`, which is gitignored.
```sh
cargo run -q -p alttp-disasm -- trace 00:8000 --mx m8x8 > disasm/008000.txt
```
- `--mx` is required. Take it from the callers' state at the call site. Never guess.
- `--stop-at A,B` marks addresses that are other units. Use it for tail jumps the tool would otherwise follow. The summary lists every followed JMP/JML so you can decide.
- `--table A=N` decodes a jump table of N 16-bit entries (`N` followed by `L` for 24-bit entries).
- `--split-table LO,HI[,BANK]=N` decodes a table stored as parallel byte tables, which you often find feeding a `JML [dp]`. Work out N from the code or the table spacing, never by guessing. If you can't pin it down, block the unit.
- `--noreturn A` marks a dispatcher that never returns. Combine it with `--table` at the address after the call for an inline table.
- The summary at the bottom is the `[map]` block. Paste it in, then resolve every `# WARN` line before setting `mapped`.

## Map (unmapped to mapped)
1. Find the routine's bounds: the entry, every reachable instruction, and every exit (`RTS`, `RTL`, `RTI`, tail `JMP`/`JML`).
2. Record the M/X width at entry and at each label. If it varies by caller, note each caller's width.
3. List callees by address. Create a unit file for each callee that has none.
4. List jump tables: the address, the entry count and the targets. Each target becomes its own unit.
5. Apply the split and merge rules in `docs/01-methodology.md`.
6. Fill in `bounds`, `mx_entry`, `callees`, `jump_tables`, and `size_insns`.

## Spec (mapped to specced)
Fill in `[spec]` from `templates/unit.toml`:
- `inputs`: registers, flags, and WRAM addresses read.
- `outputs`: registers, flags, and WRAM addresses written.
- `hw_writes`: the hardware registers touched, in order if the order matters.
- `scratch`: WRAM bytes that are written but meaningless afterward. The verifier ignores them.
- `summary`: what the routine does, in at most 5 lines, in your own words.
- `quirks`: anything surprising the translator must reproduce.
- `test_states`: what kinds of starting states will exercise each branch.

## Knowledge
- Add new symbols to `knowledge/symbols.toml`.
- Add new RAM facts to `knowledge/ram-map.md`.
- Mark guesses as `confidence = "guess"`.

## Don't
- Don't paste assembly into any committed file.
- Don't guess an M/X width. If the callers disagree and you can't resolve it, block the unit.
