#!/usr/bin/env python3
"""
deal_log.py — dedup/diff tracker for the subscription-deal-finder skill.

Each time Claude finds deals, it logs them here. Deals are deduped by
provider+description, so a deal already known just gets its "last_seen"
date bumped. `new-since-last-run` then shows only what's new since the
previous logging session — which is what turns this into a useful daily
digest instead of the same list every day.

Categories (kept in sync with SKILL.md and the web dashboard's filter chips):
  streaming    — video/audio streaming services
  carrier      — mobile/ISP bundled perks
  membership   — retail/delivery membership programs (Prime, Walmart+, Costco, Uber One, DashPass...)
  productivity — cloud/productivity bundles (Apple One, Google One, Microsoft 365...)
  creditcard   — subscription credits/perks tied to a credit card
  stacking     — combinations across the above categories

Usage:
  deal_log.py add --provider NAME --category CATEGORY \
      --deal TEXT [--conditions TEXT] [--expires TEXT] [--source URL]
  deal_log.py new-since-last-run [--category CATEGORY]
  deal_log.py list [--category CATEGORY]
"""
import argparse
import hashlib
import json
from datetime import date
from pathlib import Path

LOG_PATH = Path(__file__).resolve().parent.parent / "deals_log.json"

CATEGORIES = ["streaming", "carrier", "membership", "productivity", "creditcard", "stacking"]


def _load():
    if LOG_PATH.exists():
        with LOG_PATH.open() as f:
            return json.load(f)
    return {"deals": {}, "run_dates": []}


def _save(data):
    with LOG_PATH.open("w") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")


def _key(provider, deal):
    raw = f"{provider.strip().lower()}::{deal.strip().lower()}"
    return hashlib.sha1(raw.encode()).hexdigest()[:12]


def cmd_add(args):
    data = _load()
    today = date.today().isoformat()
    key = _key(args.provider, args.deal)

    entry = data["deals"].get(key)
    is_new = entry is None
    if is_new:
        entry = {
            "provider": args.provider,
            "category": args.category,
            "deal": args.deal,
            "conditions": args.conditions or "",
            "expires": args.expires or "",
            "source": args.source or "",
            "first_seen": today,
            "last_seen": today,
        }
    else:
        entry["last_seen"] = today
        entry["category"] = args.category
        entry["conditions"] = args.conditions or entry.get("conditions", "")
        entry["expires"] = args.expires or entry.get("expires", "")
        entry["source"] = args.source or entry.get("source", "")

    data["deals"][key] = entry
    if not data["run_dates"] or data["run_dates"][-1] != today:
        data["run_dates"].append(today)
    _save(data)

    status = "NEW" if is_new else "seen again"
    print(f"[{status}] {args.provider}: {args.deal}")


def cmd_new_since_last_run(args):
    data = _load()
    run_dates = data.get("run_dates", [])
    if not run_dates:
        print("No runs logged yet. Use 'add' first.")
        return
    last_run = run_dates[-1]
    deals = [
        d
        for d in data["deals"].values()
        if d["first_seen"] == last_run
        and (not args.category or d["category"] == args.category)
    ]
    if not deals:
        print(f"No new deals logged on the last run ({last_run}).")
        return
    print(f"New since last run ({last_run}):\n")
    for d in sorted(deals, key=lambda x: (x["category"], x["provider"])):
        print(f"- [{d['category']}] {d['provider']}: {d['deal']}")
        if d["conditions"]:
            print(f"    conditions: {d['conditions']}")
        if d["expires"]:
            print(f"    expires: {d['expires']}")
        if d["source"]:
            print(f"    source: {d['source']}")


def cmd_list(args):
    data = _load()
    deals = list(data["deals"].values())
    if args.category:
        deals = [d for d in deals if d["category"] == args.category]
    if not deals:
        print("No deals logged yet.")
        return
    for d in sorted(deals, key=lambda x: (x["category"], x["provider"])):
        print(
            f"- [{d['category']}] {d['provider']}: {d['deal']} "
            f"(first seen {d['first_seen']}, last seen {d['last_seen']})"
        )


def main():
    parser = argparse.ArgumentParser(description="Track subscription deals across runs.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Log a deal found in this run")
    p_add.add_argument("--provider", required=True)
    p_add.add_argument("--category", required=True, choices=CATEGORIES)
    p_add.add_argument("--deal", required=True)
    p_add.add_argument("--conditions")
    p_add.add_argument("--expires")
    p_add.add_argument("--source")
    p_add.set_defaults(func=cmd_add)

    p_new = sub.add_parser("new-since-last-run", help="Show deals first seen on the most recent run")
    p_new.add_argument("--category", choices=CATEGORIES)
    p_new.set_defaults(func=cmd_new_since_last_run)

    p_list = sub.add_parser("list", help="List all logged deals")
    p_list.add_argument("--category", choices=CATEGORIES)
    p_list.set_defaults(func=cmd_list)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
