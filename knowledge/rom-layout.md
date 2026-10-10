# ROM layout (EU)

Facts read from the cartridge header of the accepted EU dump. Only verified facts go here.

| Field | Value |
|---|---|
| Size | 1 MiB (8 Mbit), no copier header |
| Map mode | `$20` LoROM, SlowROM |
| Cartridge type | `$02` ROM + RAM + battery |
| SRAM | `$03` = 8 KiB |
| Region | `$02` Europe (PAL, 50 Hz) |
| Version | 0 |
| Checksum | `$75B9`, complement `$8A46`, verified |

## Vectors

| Vector | Header addr | Target |
|---|---|---|
| Emulation RESET | `$00:FFFC` | `$00:8000` |
| Native NMI | `$00:FFEA` | `$00:80C9` |
| Native IRQ | `$00:FFEE` | `$00:82D8` |
| Native BRK | `$00:FFE6` | `$00:FFFF` (unused) |

## LoROM address mapping

A SNES address `$BB:AAAA` with `AAAA >= $8000` maps to file offset `(BB & $7F) * $8000 + (AAAA - $8000)`.
This is implemented and tested in `alttp-recomp/crates/alttp-rom`.
