#!/usr/bin/env python3
"""Ledger tool: status, next, validate. Stdlib only (Python 3.11+)."""
import argparse
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UNITS = ROOT / "ledger" / "units"

STATUSES = ["unmapped", "mapped", "specced", "translated", "verified", "reviewed", "done", "blocked"]
RANK = {s: i for i, s in enumerate(STATUSES[:-1])}  # blocked has no rank
TRANSLATED_OR_LATER = {"translated", "verified", "reviewed", "done"}

ROLE_STATUSES = {
    "cartographer": {"unmapped", "mapped"},
    "translator": {"specced"},
    "verifier": {"translated"},
    "reviewer": {"verified"},
}

REQUIRED_TOP = ["id", "name", "address", "status", "owner", "blocked_reason", "notes", "followups"]
REQUIRED_TABLES = ["map", "spec", "code", "verify", "review", "handoff"]
ADDR_RE = re.compile(r"^\$([0-9A-F]{2}):([0-9A-F]{4})$")


def load():
    units = {}
    for p in sorted(UNITS.glob("*.toml")):
        with p.open("rb") as f:
            units[p.stem] = (p, tomllib.load(f))
    return units


def addr_to_id(addr):
    m = ADDR_RE.match(addr)
    return (m.group(1) + m.group(2)).lower() if m else None


def callees_ready(u, units):
    for c in u.get("map", {}).get("callees", []):
        if c not in units:
            return False
        if units[c][1]["status"] not in TRANSLATED_OR_LATER:
            return False
    return True


def cmd_status(units):
    counts = {s: 0 for s in STATUSES}
    for _, u in units.values():
        counts[u["status"]] = counts.get(u["status"], 0) + 1
    total = len(units)
    print(f"units: {total}")
    for s in STATUSES:
        print(f"  {s:<11} {counts.get(s, 0)}")
    done = counts.get("done", 0)
    if total:
        print(f"done: {done}/{total} ({100 * done / total:.1f}%)")
    blocked = [(i, u) for i, (_, u) in units.items() if u["status"] == "blocked"]
    if blocked:
        print("blocked:")
        for i, u in blocked:
            print(f"  {i} {u['name']}: {u['blocked_reason']}")


def cmd_next(units, role, limit):
    roles = [role] if role else list(ROLE_STATUSES)
    for r in roles:
        picks = []
        for i, (_, u) in units.items():
            if u["status"] not in ROLE_STATUSES[r] or u["owner"]:
                continue
            if u.get("map", {}).get("merged_into"):
                continue
            if r == "translator" and not callees_ready(u, units):
                continue
            picks.append((i, u))
        # cartographer: mapped before unmapped (finish what's started)
        picks.sort(key=lambda x: (-RANK.get(x[1]["status"], 0), x[0]))
        print(f"{r}:")
        if not picks:
            print("  (none)")
        for i, u in picks[:limit]:
            print(f"  {i} {u['name']} [{u['status']}]")


def cmd_validate(units):
    errors = []
    for i, (p, u) in units.items():
        for k in REQUIRED_TOP:
            if k not in u:
                errors.append(f"{i}: missing top-level key '{k}'")
        for t in REQUIRED_TABLES:
            if not isinstance(u.get(t), dict):
                errors.append(f"{i}: missing table [{t}]")
        if u.get("id") != i:
            errors.append(f"{i}: id '{u.get('id')}' does not match filename")
        if addr_to_id(u.get("address", "")) != i:
            errors.append(f"{i}: address '{u.get('address')}' does not match id (format $BB:AAAA, uppercase hex)")
        if u.get("status") not in STATUSES:
            errors.append(f"{i}: invalid status '{u.get('status')}'")
        if u.get("status") == "blocked" and not u.get("blocked_reason"):
            errors.append(f"{i}: blocked without blocked_reason")
        if not isinstance(u.get("followups", []), list):
            errors.append(f"{i}: followups must be a top-level list (put it above the first [table])")
        m = u.get("map", {})
        for c in m.get("callees", []):
            if c not in units:
                errors.append(f"{i}: callee {c} has no unit file")
        mi = m.get("merged_into", "")
        if mi and mi not in units:
            errors.append(f"{i}: merged_into {mi} has no unit file")
        st = u.get("status")
        if st in TRANSLATED_OR_LATER and not u.get("code", {}).get("function"):
            errors.append(f"{i}: status {st} but [code].function is empty")
        if st in {"verified", "reviewed", "done"} and u.get("verify", {}).get("result") != "pass":
            errors.append(f"{i}: status {st} but [verify].result is not 'pass'")
    if errors:
        print("\n".join(errors))
        print(f"FAIL: {len(errors)} error(s)")
        return 1
    print(f"OK: {len(units)} unit(s)")
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    n = sub.add_parser("next")
    n.add_argument("--role", choices=list(ROLE_STATUSES))
    n.add_argument("--limit", type=int, default=5)
    sub.add_parser("validate")
    a = ap.parse_args()
    units = load()
    if a.cmd == "status":
        cmd_status(units)
    elif a.cmd == "next":
        cmd_next(units, a.role, a.limit)
    else:
        sys.exit(cmd_validate(units))


if __name__ == "__main__":
    main()
