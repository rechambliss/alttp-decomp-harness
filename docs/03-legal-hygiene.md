# Legal hygiene

This is a personal project built from a legally owned cartridge dump. These rules keep the repos free of copyrighted material.

## Never commit

- The ROM, in whole or in part, in any encoding (hex, base64, arrays).
- Extracted graphics, palettes, tilemaps, text, music, or samples.
- Disassembly listings or assembly text copied from the ROM or from other projects.
- Captured WRAM snapshots that embed decompressed ROM data in bulk. Fixtures should be small and targeted.

## Fine to commit

- Addresses, names, and comments describing behavior in your own words.
- Rust code you wrote.
- Tools that read a ROM the user supplies.
- Hashes used to verify the user's ROM.

## How assets reach the game

The build tool or first-run step reads the player's ROM, checks its SHA-1 against the accepted list, and extracts assets to a local cache outside the repo.
Theme packs then override entries in that cache by id.

## Accepted ROM

| Region | SHA-1 | Notes |
|---|---|---|
| EU (PAL) | `7c073a222569b9b8e8ca5fcb5dfec3b5e31da895` | 1 MiB, LoROM, no copier header, checksum `$75B9` valid |

## Where the ROM lives

It lives in the private repo `rechambliss/alttp-rom`, which is never made public and never forked.
Sessions clone it next to the other two repos and point `ALTTP_ROM` at it.

## Agents

If a task would require committing any of the above, stop and set the unit to `blocked`.
