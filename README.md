# Subscription Deal Finder

A Claude skill that finds current subscription discounts and bundles —
not just streaming (Netflix, Max, Disney+, Hulu, ESPN, Spotify, ...), but the
everyday bundles people actually stack: mobile carrier perks (T-Mobile,
Verizon, AT&T), retail/delivery memberships (Amazon Prime, Walmart+, Costco,
Uber One, DashPass), productivity bundles (Apple One, Google One, Microsoft
365), and credit-card-linked subscription credits (Amex Platinum, Chase
Sapphire). It remembers what it's already shown you, so a daily run surfaces
only what's *new* — and a companion static site lets you (or anyone) browse
the current list without needing an AI account at all.

## Why

Subscription and bundle pricing changes constantly, and the best deals are
often hidden in non-obvious places (a phone plan that quietly includes
Netflix, a retail membership that includes a streaming service, a credit
card credit toward a subscription you already pay for). This project turns
"go check a dozen different sites" into one daily prompt — and a page you can
just glance at.

## How it works

- **`SKILL.md`** — instructions Claude follows: what providers/categories to
  check each run, how to search for *current* offers (never hard-coded
  prices, since those go stale), and how to format results. Categories:
  `streaming`, `carrier`, `membership`, `productivity`, `creditcard`,
  `stacking`.
- **`data/providers.json`** — a reference checklist of providers and known
  bundle patterns to search for, organized by category. Not a source of
  truth for pricing — just a checklist so nothing gets missed.
- **`scripts/deal_log.py`** — a small CLI that logs every deal found, deduped
  by provider + description. Running it daily means day 2 onward only shows
  deals that are actually new.
- **`deals_log.json`** — the running log `deal_log.py` reads/writes. Starts
  empty; fills in as you use the skill.
- **`index.html`** — a static, searchable/filterable dashboard that reads
  `deals_log.json` directly. No server, no AI calls, no cost to view —
  works as a GitHub Pages site (see below) so you or anyone else can browse
  current deals like a normal webpage.

## Browse it as a website (no AI account needed)

Enable GitHub Pages for this repo once: **Settings → Pages → Source: Deploy
from a branch → Branch: `main`, folder: `/ (root)` → Save**. GitHub will
publish `index.html` at `https://<your-username>.github.io/<repo-name>/`.
It reads `deals_log.json` client-side, so every time you push an updated log,
the page updates too — no rebuild step, no backend, free to host, free for
anyone to visit.

## Install as a Claude skill

This is packaged as a standard Claude skill folder (`SKILL.md` with
frontmatter). To use it:

1. Copy this whole folder into wherever your Claude client loads skills from
   (for Claude Code / Cowork, your skills directory — check your client's
   docs for the exact path, since this varies by product and version).
2. Once loaded, just ask Claude things like *"check for subscription
   deals"*, *"any new streaming bundles today"*, or *"run my daily deals
   check"* — Claude will follow `SKILL.md` automatically.

## Use it elsewhere — ChatGPT, other AI, or with friends

`SKILL.md` is just a plain prompt, so it isn't locked to one AI product or
one person:

- **Other AI assistants**: paste `SKILL.md`'s content into a ChatGPT Custom
  GPT's instructions (or the equivalent "custom instructions"/"Gem" feature
  on another platform). It runs the same searches under that platform's
  account.
- **Friends**: anyone can copy `SKILL.md` into their own Claude skill or
  their own Custom GPT and run it on their own account. Nothing here calls
  a shared backend, so each person's usage is billed to their own AI
  account, not yours.
- **Friends who don't have an AI account at all**: point them at the GitHub
  Pages link above. It's a static page, so viewing it costs nothing and
  needs no AI account on their end — they just see whatever `deals_log.json`
  currently holds.

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
