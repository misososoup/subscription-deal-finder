# Subscription Deal Finder

A Claude skill that finds current subscription discounts and bundle deals —
streaming (Netflix, Max, Disney+, Hulu, Spotify, ...) and mobile carrier
perks (T-Mobile, Verizon, AT&T) — and remembers what it's already shown you,
so a daily run surfaces only what's *new*.

## Why

Streaming and carrier pricing changes constantly, and the deals worth having
are often bundled in non-obvious places (a phone plan that quietly includes
Netflix, a student discount that bundles Hulu with Spotify, a credit card
portal offer). This project turns "go check five different sites" into one
daily prompt.

## How it works

- **`SKILL.md`** — instructions Claude follows: what providers/categories to
  check each run, how to search for *current* offers (never hard-coded
  prices, since those go stale), and how to format results.
- **`data/providers.json`** — a reference list of providers and known bundle
  patterns to search for. Not a source of truth for pricing — just a
  checklist so nothing gets missed.
- **`scripts/deal_log.py`** — a small CLI that logs every deal found, deduped
  by provider + description. Running it daily means day 2 onward only shows
  deals that are actually new.
- **`deals_log.json`** — the running log `deal_log.py` reads/writes. Starts
  empty; fills in as you use the skill.

## Install as a Claude skill

This is packaged as a standard Claude skill folder (`SKILL.md` with
frontmatter). To use it:

1. Copy this whole folder into wherever your Claude client loads skills from
   (for Claude Code / Cowork, your skills directory — check your client's
   docs for the exact path, since this varies by product and version).
2. Once loaded, just ask Claude things like *"check for subscription
   deals"*, *"any new streaming bundles today"*, or *"run my daily deals
   check"* — Claude will follow `SKILL.md` automatically.

## Usage

Ask Claude to check for deals. It searches live (see `SKILL.md`), then logs
what it found:

```bash
python3 scripts/deal_log.py add \
  --provider "T-Mobile" --category carrier \
  --deal "Netflix Standard w/ Ads included on Experience Beyond" \
  --conditions "Requires Experience Beyond plan, per line" \
  --expires "ongoing" \
  --source "https://www.t-mobile.com/..."
```

See everything new since the last time you ran it:

```bash
python3 scripts/deal_log.py new-since-last-run
```

See the full running list:

```bash
python3 scripts/deal_log.py list
```

## Notes / limitations

- This doesn't scrape or maintain live pricing itself — it relies on Claude's
  web search at the time you run it, cross-checked against official provider
  sites. That's deliberate: hard-coding prices/promo names would go stale
  almost immediately.
- No account access — it can't see what subscriptions you actually hold. Tell
  Claude your carrier/services and it'll prioritize relevant results.
- US-centric by default (see `data/providers.json`); mention if you're
  looking for deals in another region.

## License

MIT — see `LICENSE`.
