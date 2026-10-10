# WRAM map

One line per address or range. Grep for the address, don't read the whole file.
Format: `$7E:XXXX  size  NAME  confidence  meaning  (unit that established it)`

<!-- entries below, sorted by address -->
$7E:0003  3  DISPATCH_PTR  likely  24-bit target built from three byte tables, then jumped through by 0080b5  (008000, seen in callee 0080b5)
$7E:0010  1  MODULE_INDEX  likely  Y index into the dispatch tables at $00:8061/$807D/$8099  (008000)
$7E:0012  1  FRAME_READY  guess  Main loop spins while zero, clears it after each pass (after 0085ec, so a set during frame work is lost: lag frame); setter not mapped yet, probably NMI  (008000)
$7E:001A  1  FRAME_COUNTER  likely  Incremented once per main loop pass, 8-bit wrap  (008000)
