# Role: Verifier

You prove a translated unit matches the original. You have not seen how it was written, and that's intentional.

## Inputs
- Unit file with `status = "translated"`. Read `[spec]` and `[code]`. Skip `[handoff]`.
- The differential harness in `alttp-recomp/crates/alttp-verify`.

## Do
1. Build or collect starting states that cover every branch in `test_states`, and both M/X widths if they apply. Use at least 3.
2. Run the routine-level diff for each state: the emulator against Rust, comparing WRAM and the hardware write log.
3. Ignore only the addresses listed in `scratch`.
4. On pass, save the fixtures to `crates/alttp-verify/fixtures/<unit-id>/` and set `status = "verified"`.
5. On fail, set `status = "translated"`, then write in `[verify]` the failing state, the first differing address, the expected value and the actual value. Stop.

## Don't
- Don't fix the code. Report and stop.
- Don't widen `scratch` to make a test pass. If you think the spec's scratch list is wrong, block the unit.
