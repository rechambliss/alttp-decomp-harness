# Rust conventions

## Layout in alttp-recomp

- `crates/alttp-core/src/bankXX/` holds routines by original bank, one file per unit or small group.
- Each function's doc comment starts with the original address: `/// $00:8000 Reset`.
- Shared state: `Wram`, `Hw`, and `Cpu` (only the register state that crosses routine boundaries).

## Function shape

```rust
/// $02:A1B2 Player_HandleSword
/// Spec: ledger/units/02a1b2.toml
pub fn player_handle_sword(s: &mut State) { ... }
```

- One Rust function per unit entry point.
- Register values that pass between routines go through explicit parameters and return values, documented in the spec.
- Use `u8`/`u16` and wrapping arithmetic (`wrapping_add`, etc.) everywhere the original can overflow. Never rely on debug-mode panics.
- Carry and other flags that a caller reads after return must be returned explicitly.

## Naming

- Use community-style names when known, PascalCase with underscores in symbols (`Player_HandleSword`), and snake_case in Rust.
- Unknown routines are named `sub_BBAAAA` until someone understands them. Renaming later is cheap.
- RAM: constants in `wram::addr`, e.g. `pub const LINK_X: u16 = 0x0022;`.

## Quirks

- Reproduce them. Mark each with `// QUIRK:` and one line explaining what the original does.
- Never fix them in this phase.

## Tests

- Unit tests from the spec live next to the function.
- Differential test fixtures live in `crates/alttp-verify/fixtures/<unit-id>/`. They hold your own captured states, not ROM data.

## Commits

- One unit per commit: `[02a1b2] translate Player_HandleSword`.
- No drive-by changes outside the unit.
