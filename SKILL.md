---
name: subscription-deal-finder
description: Finds current subscription discounts, bundles, and promo stacking opportunities across streaming (Netflix, Max, Disney+, Hulu, Spotify, etc.), mobile carriers (T-Mobile, Verizon, AT&T), and everyday membership/productivity/credit-card bundles (Amazon Prime, Walmart+, Costco, Apple One, Google One, Amex/Chase card perks). Use when the user asks to check for subscription deals, streaming bundles, carrier perks, or wants a daily/periodic deals digest.
---

# Subscription Deal Finder

Finds current, real, verifiable discounts and bundles — not just streaming, but
any recurring "daily life" subscription people actually stack: mobile carrier
perks, retail/delivery memberships, productivity suites, and credit-card-linked
subscription credits — then logs them so repeat runs only surface what's *new*
since last time.

## When to use this skill

Trigger on requests like "check for subscription deals", "any new streaming
bundles today", "what discounts can I stack with my phone plan", "run my daily
deals check", or a scheduled daily digest.

## Step 1 — Know what to search for

Read `data/providers.json` in this skill's folder for the current checklist of
providers and known bundle patterns, organized by `streaming_video`,
`streaming_audio`, `mobile_carriers`, `membership_bundles`,
`productivity_bundles`, `credit_card_bundles`, and `stacking_categories`.
It's a starting reference, not a source of truth — prices and promos change
constantly, so never state a price or offer from that file as current without
verifying it live in Step 2.

Categories to cover every run, unless the user narrows the scope. Use the
category taxonomy below consistently — it matches `deal_log.py`'s
`--category` choices and the web dashboard's filter chips:

- **`streaming`** — video: Netflix, Max (HBO Max), Disney+, Hulu, ESPN
  (the standalone app, separate from ESPN+), ESPN+, Paramount+, Peacock,
  Apple TV+, Amazon Prime Video, Starz, AMC+, MGM+, Crunchyroll. Audio:
  Spotify, Apple Music, YouTube Music/Premium, Amazon Music Unlimited,
  Audible, Tidal, Pandora.
- **`carrier`** — mobile/ISP bundled perks: T-Mobile (e.g. "Netflix on Us",
  Apple TV+, MLB.TV, T-Mobile Tuesdays), Verizon (+play, myPlan perks,
  Disney Bundle), AT&T, Google Fi, Xfinity Mobile/Comcast (often bundles
  Peacock), Spectrum Mobile/Charter.
- **`membership`** — retail/delivery membership programs that bundle
  several perks into one subscription: Amazon Prime (shipping + video +
  music + more, not just Prime Video), Walmart+ (has included Paramount+),
  Costco/Sam's Club (executive tiers, discounted gift cards), Uber One,
  DoorDash DashPass, Instacart+.
- **`productivity`** — cloud/productivity bundles: Apple One (Music + TV+ +
  Arcade + iCloud+, higher tiers add News+/Fitness+), Google One (storage +
  VPN/AI on paid tiers), Microsoft 365 Family.
- **`creditcard`** — subscription credits/perks tied to a credit card: Amex
  Platinum (Walmart+, Uber Cash, Disney Bundle credit, CLEAR Plus), Chase
  Sapphire Reserve/Preferred (DashPass, Lyft/Peloton credits on some
  products), Capital One Venture X. Card-specific benefits vary by exact
  product and change often — verify against the card issuer's current
  benefits page, not a generic card-name search. Personalized offer portals
  (Amex Offers, Chase Offers) can't be searched generically — tell the user
  to check their own account instead of guessing what's in it.
- **`stacking`** — combinations across the above: student discounts
  (Spotify + Hulu, Amazon Prime Student, Apple Music Student usually
  bundling Apple TV+), family/duo plan splitting, annual vs. monthly
  billing discounts, a membership that already includes a streaming
  service (so a separate subscription would be redundant), a carrier's
  weekly perk program stacking with its included streaming perk.

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
Expires | Source link. Group by category (Streaming / Carrier / Membership /
Productivity / Credit Card / Stacking) — skip empty categories rather than
padding the table. Call out anything that looks like it stacks with something
the user already mentioned having (e.g. if they've said they're on T-Mobile,
highlight carrier-included streaming perks first; if they mentioned an Amex
Platinum, check its current benefit list before generic card searches).

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
