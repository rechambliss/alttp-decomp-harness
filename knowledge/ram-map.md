# WRAM map

One line per address or range. Grep for the address, don't read the whole file.
Format: `$7E:XXXX  size  NAME  confidence  meaning  (unit that established it)`

<!-- entries below, sorted by address -->
$7E:0003  3  DISPATCH_PTR  likely  24-bit target (lo/hi/bank) built from three byte tables, then jumped through by 0080b5 (JML [$0003]); left holding the current module's entry address  (008000, 0080b5)
$7E:0010  1  MODULE_INDEX  likely  Y index into the dispatch tables at $00:8061/$807D/$8099; 28 entries, valid $00-$1B, no bounds check  (008000, 0080b5)
$7E:0012  1  FRAME_READY  likely  Main loop spins while zero, clears it after each pass (after 0085ec, so a set during frame work is lost: lag frame). Set by NMI: INC when zero, and only then NMI runs 0089e0 and 0083d1  (008000, 0080c9)
$7E:0013  1  INIDISP_MIRROR  likely  Written to $2100 at the end of both NMI paths  (0080c9)
$7E:0017  1  NMI_UPDATE_INDEX  guess  0089e0 jumps through $00:8C6E with X = $17*2, then clears it  (0080c9, seen in callee 0089e0)
$7E:001A  1  FRAME_COUNTER  likely  Incremented once per main loop pass, 8-bit wrap  (008000)
$7E:001C  4  TM_TS_TMW_TSW_MIRROR  likely  $1C-$1F copied to $212C-$212F by NMI  (0080c9)
$7E:0094  2  BGMODE_MOSAIC_MIRROR  likely  $94 -> $2105 BGMODE, $95 -> $2106 MOSAIC; if ($94 & 7) == 7 NMI also loads Mode 7 regs  (0080c9)
$7E:0096  9  WINDOW_CMATH_MIRROR  likely  $96-$98 -> $2123-$2125, $99/$9A -> $2130/$2131, $9C-$9E -> $2132 (three writes)  (0080c9)
$7E:009B  1  HDMAEN_MIRROR  likely  Written to $420C last in both NMI paths ($420C is zeroed at NMI start)  (0080c9)
$7E:00E4  2  BG3HOFS_MIRROR  likely  $E4/$E5 -> $2111 (low, high)  (0080c9)
$7E:00EA  2  BG3VOFS_MIRROR  likely  $EA/$EB -> $2112 (low, high)  (0080c9)
$7E:00F6  1  JOY1_NEW_HI  guess  Read only by dead code at $00:803B (bits 5 and 4 tested); probably a joypad new-press byte  (00803b)
$7E:00FF  1  ALT_IRQ_VTIME  guess  NMI alt path writes it to $4209 (VTIMEL) with $420A=0 before enabling V-IRQ  (0080c9)
$7E:011E  8  BG_SCROLL_MIRROR  likely  $0120/21 -> $210D BG1HOFS, $0124/25 -> $210E BG1VOFS, $011E/1F -> $210F BG2HOFS, $0122/23 -> $2110 BG2VOFS  (0080c9)
$7E:0128  1  IRQ_ENABLE_REQ  guess  When nonzero NMI acks $4211, sets V-IRQ at line $80 and writes $4200=$A1. IRQ does the BG3 scroll split only when nonzero and $4211 bit 7 set; bit 7 of $0128 set makes the split one-shot (IRQ clears $0128 and writes $4200=$81), bit 7 clear repeats every frame  (0080c9, 0082d8)
$7E:012A  1  NMI_ALT_THREAD  likely  When nonzero NMI skips the normal body and takes the stack-swap path at $00:822D; IRQ likewise takes its swap path at $00:831F  (0080c9, 0082d8)
$7E:012C  2  APU_QUEUE_0_1  likely  Pending values for $2140/$2141; NMI sends and clears them. $012C equal to $0133 is neither sent nor cleared (stays pending)  (0080c9)
$7E:012E  2  APU_QUEUE_2_3  likely  Copied to $2142/$2143 every NMI (before the $012A split), then cleared  (0080c9)
$7E:0130  2  APU_LAST_0_1  guess  $0130: last $012C value below $F2; $0131: last value sent to $2141  (0080c9)
$7E:0133  1  APU_LAST_PORT0  guess  Last value sent to $2140; compared against $012C and against readback of $2140  (0080c9)
$7E:0630  2  IRQ_BG3HOFS  guess  IRQ writes $0630/$0631 to $2111 (BG3HOFS low, high) at HBlank for a mid-screen BG3 split, and zeroes BG3VOFS  (0082d8)
$7E:0638  4  M7_CENTER_MIRROR  likely  $0638/39 -> $211F M7X, $063A/3B -> $2120 M7Y, written only when BG mode is 7  (0080c9)
$7E:0800  512  OAM_BUFFER_LOW  likely  Shadow of OAM low table, 128 entries x 4 bytes (X, Y, tile, attr); 00841e sets every Y byte ($0801+4n) to $F0 each frame to hide unused sprites  (00841e)
$7E:0FD7  1  DEBUG_PAUSE_TOGGLE  guess  Incremented by dead code at $00:803B on $F6 bit 5; bit 0 set skipped the frame body. This reader is unreachable in EU; other users not checked  (00803b)
$7E:1F0A  2  ALT_THREAD_SP  likely  Saved stack pointer swapped with S on the NMI alt path and on the IRQ path at $00:831F (both when $012A != 0). Points 1 below a 13-byte frame (DB, D, Y, X, A, P, PC, PB). Only other writer found by byte search: $09:F7FB (unconfirmed)  (0080c9, 0082d8)
$7E:1F0C  1  UPLOAD_E800_REQ  guess  When nonzero 009337 DMAs $7E:E800 to VRAM and clears it  (0080c9, seen in callee 009337)
