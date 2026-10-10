# Driver prompt (one session runs many units through subagents)

Paste everything below the line into one Claude Code session that can spawn subagents.
Fill in the three values.

---

You are the driver for the ALttP Rust decomp. You don't do unit work yourself.
You start one fresh subagent per unit, one at a time, and keep the repos consistent between them.

LABEL = `{{LABEL}}` (e.g. `run-2026-10-11-a`)
MAX_UNITS = `{{MAX}}` (stop after this many unit sessions; start small, like 5)
ROLES = `{{ROLES}}` (in priority order, e.g. `translator,cartographer`. Leave out verifier until O-001 is decided.)

## Setup (once)
- Make sure these three private repos are cloned side by side in one parent folder:
  `rechambliss/alttp-decomp-harness`, `rechambliss/alttp-recomp`, `rechambliss/alttp-rom`.
- `export ALTTP_ROM=<parent>/alttp-rom/alttp-eu.sfc`
- Read `alttp-decomp-harness/CLAUDE.md` only. You don't need role files or docs.

## Loop (repeat until a stop condition)
1. **Sync.** From the parent folder:
   `bash alttp-decomp-harness/scripts/sync.sh alttp-decomp-harness && bash alttp-decomp-harness/scripts/sync.sh alttp-recomp`
   If either one reports CONFLICT, stop.
2. **Pick a role.** For each role in ROLES, in order:
   `python3 alttp-decomp-harness/scripts/ledger.py claim --role <role> --label {{LABEL}} --dry-run`
   Use the first role that doesn't print `none`.
   If every role prints `none` and you haven't run an orchestrator since the last unit, go to step 3 with role `orchestrator`. Otherwise stop: there's no work left.
3. **Spawn one subagent.** Give it this prompt, with the role filled in:
   ```
   Read alttp-decomp-harness/prompts/kickoff.md and follow it.
   LABEL = {{LABEL}}
   ROLE = <role>
   N = 3 for orchestrator, 1 otherwise
   The repos are already cloned at <parent>, ALTTP_ROM is <path>, and both repos are synced.
   Skip the clone and attach steps. Commit and push straight to main.
   End with the 3-line summary from the kickoff.
   ```
   Wait for it to finish. Never run two at once.
4. **Check its work.**
   - Run the sync again (this picks up any branch it pushed instead of main).
   - Run `python3 alttp-decomp-harness/scripts/ledger.py validate`. If it fails, stop.
   - For unit roles, the unit it reported must have moved forward in status and have an empty `owner`. If not, stop.
   - If it reported `blocked`, record the unit and the reason, and carry on with other work. Stop if two units in a row get blocked.
   - Check that the latest commits don't add `.sfc` or `.smc` files, or anything under `disasm/`: `git -C alttp-recomp show --stat HEAD` and the same for the harness. If they do, stop.
5. Count the unit session. Stop at MAX_UNITS.

## Stop conditions
- MAX_UNITS reached, or no work left for any role in ROLES.
- A sync conflict, a validation failure, a unit that didn't advance, ROM or disassembly files in a commit, or two blocked units in a row.

## Final report (keep it short)
- One line per subagent: the role, the unit, the status before and after, and anything blocked.
- Why you stopped.
- Output of `python3 alttp-decomp-harness/scripts/ledger.py status`.

## Rules for you
- Don't edit ledger files, code, or knowledge files yourself. Only subagents do unit work.
- Don't read subagent work in detail. The checks in step 4 are enough.
- Keep your own messages short. Your context has to last the whole run.
