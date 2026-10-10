# Splitting work into token-efficient agent sessions

The goal is that each agent session starts with only what one unit needs, finishes in one sitting, and leaves everything the next agent needs in files.

## Context budget per session

| Item | Target size |
|---|---|
| `CLAUDE.md` | under 80 lines |
| Role file | under 80 lines |
| Task card (ledger TOML) | under 60 lines |
| Assembly for the unit | about 300 instructions max, dumped by tool, never pasted from docs |
| Knowledge lookups | grep results only, never whole files |

If a unit needs more than this, it is too big. Split it.

## Rules that keep sessions small

1. **One unit per session.** Context from unit A degrades work on unit B.
2. **Files over chat.** Anything worth keeping goes into the ledger, the spec, or `knowledge/`.
3. **Grep, don't read.** `knowledge/symbols.toml` and `knowledge/ram-map.md` will grow large. Look up the lines you need.
4. **Callees by signature only.** The translator sees callee names, signatures, and one-line summaries from their specs, never their bodies.
5. **Handoffs are short.** 30 lines max: what was done, what is uncertain, and what the next role should check.
6. **No re-deriving.** If the cartographer recorded the M/X width or a jump table, the translator trusts the spec and does not re-analyze. If the spec looks wrong, block the unit.
7. **Separate verifier.** The verifier gets the spec and the code, not the translator's handoff reasoning. Fresh eyes, small context.

## Batching

The orchestrator can create many task cards in one session, because card creation is cheap and mechanical.
The other roles do one unit per session.

Several translator sessions can run in parallel on independent units, because each unit's ledger file is separate.

## Model tiering (suggested)

| Role | Needs | Suggested tier |
|---|---|---|
| Orchestrator | bookkeeping | smaller, faster model |
| Cartographer | careful reading of 65816 code | strongest model |
| Translator | precise mechanical translation | strong model |
| Verifier | runs tools and reads diffs | mid tier |
| Reviewer | checks conventions | mid tier |

## Signs a session went wrong

- It read whole docs or knowledge files.
- It touched more than one unit.
- It ended without updating the ledger.
- It "fixed" a quirk.
