---
name: subscription-deal-finder
description: Finds current subscription discounts, bundles, and promo stacking opportunities across streaming (Netflix, Max, Disney+, Hulu, Spotify, etc.) and mobile carriers (T-Mobile, Verizon, AT&T). Use when the user asks to check for subscription deals, streaming bundles, carrier perks, or wants a daily/periodic deals digest.
---

# Subscription Deal Finder

Finds current, real, verifiable discounts and bundles across streaming services
and mobile carriers, then logs them so repeat runs only surface what's *new*
since last time.

## When to use this skill

Trigger on requests like "check for subscription deals", "any new streaming
bundles today", "what discounts can I stack with my phone plan", "run my daily
deals check", or a scheduled daily digest.

## Step 1 — Know what to search for

Read `data/providers.json` in this skill's folder for the current list of
providers and known bundle patterns to check. It's a starting reference, not a
source of truth — prices and promos change constantly, so never state a price
or offer from that file as current without verifying it live in Step 2.

Categories to cover every run, unless the user narrows the scope:

- **Streaming**: Netflix, Max (HBO Max), Disney+, Hulu, ESPN+, Paramount+,
  Peacock, Apple TV+, Amazon Prime Video, Spotify, YouTube Premium/Music,
  Audible.
- **Mobile carrier perks/bundles**: T-Mobile (e.g. "Netflix on Us", Apple TV+,
  MLB.TV included on certain plans), Verizon (+play, myPlan perks, Disney
  Bundle), AT&T (streaming bundles on unlimited plans).
- **Cross-provider stacking**: student discounts (Spotify + Hulu, Amazon Prime
  Student), family/duo plan splitting, credit card portal offers (e.g. Amex
  Offers, Chase Offers on streaming), annual vs. monthly billing discounts,
  retailer gift-card promos (e.g. discounted gift cards at Costco/Sam's Club).

## Step 2 — Search live, don't rely on training data

Subscription pricing and promos change often and are past this model's
knowledge cutoff for anything recent. For each provider/category:

1. Use web search for queries like `"<provider> promo OR discount OR deal
   2026"`, `"<carrier> streaming perks included"`, `"<provider> student
   discount"`, `"<provider> bundle discount"`.
2. Prefer official sources (the provider's own site, e.g. netflix.com,
   t-mobile.com, verizon.com, att.com, spotify.com, amazon.com) for the
   authoritative current offer. Use reputable deal-aggregator or news sources
   (e.g. major tech/consumer publications) to catch things official pages
   don't advertise loudly, but flag those as unverified until cross-checked.
3. Note the expiration/eligibility conditions exactly as stated — many carrier
   perks require a specific plan tier, autopay, or a new line.
4. Skip anything you can't find a live, dated source for. Never invent a
   price, discount percentage, or promo name.

## Step 3 — Compile the findings

Present results as a table: Provider | Deal | Eligibility/conditions |
Expires | Source link. Group by category (Streaming / Carrier / Stacking).
Call out anything that looks like it stacks with something the user already
mentioned having (e.g. if they've said they're on T-Mobile, highlight
carrier-included streaming perks first).

Always close with a one-line reminder that promo terms change and the user
should confirm final pricing/eligibility on the provider's site before
signing up or switching plans — this skill surfaces leads, not guarantees.

## Step 4 — Log it so tomorrow's run only shows what's new

Run `scripts/deal_log.py` to append today's findings to `deals_log.json` next
to this file. It dedupes against everything logged before and prints a diff
of newly-seen deals vs. ones already known, so a daily run naturally becomes
a digest of *new* offers instead of repeating the same list.

```
python3 scripts/deal_log.py add \
  --provider "T-Mobile" --category carrier \
  --deal "Netflix Standard w/ Ads included on Experience Beyond" \
  --conditions "Requires Experience Beyond plan, per line" \
  --expires "ongoing" \
  --source "https://www.t-mobile.com/..."
```

Then show what's new:

```
python3 scripts/deal_log.py new-since-last-run
```

If the user just wants a one-off check with no logging, skip Step 4 and say
so — logging is what makes daily use valuable, but it's optional.

## Notes

- This skill does not have live carrier/account access — it can't check what
  the user personally already has. If the user tells you their carrier or
  which subscriptions they hold, use that to prioritize relevant results.
- Region matters (offers in `data/providers.json` and search results may be
  US-centric); ask if the user is outside the US and results look off.
