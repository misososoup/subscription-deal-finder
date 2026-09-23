---
name: subscription-deal-finder
description: Finds current subscription discounts, bundles, cash-back/sign-up bonuses, and stacking opportunities across streaming (Netflix, Max, Disney+, Hulu, Spotify, etc.), mobile/ISP carriers (T-Mobile, Verizon, AT&T, Xfinity), and everyday membership/productivity/credit-card bundles (Amazon Prime, Walmart+, Costco, Apple One, Google One, Amex/Chase card perks). Use when the user asks to check for subscription deals, streaming bundles, carrier perks, or wants a daily/periodic deals digest.
---

# Subscription Deal Finder

Finds current, real, verifiable discounts and bundles — not just streaming,
but any recurring "daily life" subscription people actually stack: mobile/ISP
perks and switch bonuses, retail/delivery memberships, productivity suites,
and credit-card-linked subscription credits — then logs them clearly enough
that someone can act on them without having to go re-research everything
themselves.

The two things that matter most: **be exhaustive** (a user who finds more on
a two-minute Google search than this skill found in a full run has no reason
to trust it) and **be plain** (every entry should be something a non-expert
can read once and know exactly what to do with).

## Step 1 — Know what to search for

Categories — matches `deal_log.py`'s `--category` choices and the dashboard:

- **`streaming`** — video: Netflix, Max (the service formerly called HBO
  Max — always say "Max" on first mention per provider, then it's fine to
  reuse), Disney+, Hulu, ESPN's standalone app (Select tier = ESPN+ content
  only; Unlimited tier = all ESPN cable channels + NFL Network — always
  check both and explain the difference, don't just report one), Paramount+,
  Peacock, Apple TV+, Amazon Prime Video, Starz, AMC+, MGM+, Crunchyroll.
  Audio: Spotify, Apple Music, YouTube Music/Premium, Amazon Music
  Unlimited, Audible, Tidal, Pandora. Also check cross-provider bundle pages
  (e.g. Disney+/Hulu/ESPN together is a different, cheaper offer than any
  one of them alone — don't stop at single-provider pages).
- **`carrier`** — mobile *and* ISP bundled perks AND switch/sign-up cash
  bonuses (these are a distinct, commonly-missed deal type — always search
  for both): T-Mobile, Verizon, AT&T, Google Fi, Xfinity/Comcast (mobile
  *and* home internet — they bundle streaming apps into internet plans too,
  e.g. "StreamSaver"), Spectrum/Charter. Search explicitly for "$ gift card
  switch", "cash back new customer", "sign-up bonus", "activation fee
  waived" in addition to "included streaming perk" — these are two separate
  offer types most carriers run simultaneously.
- **`membership`** — retail/delivery membership programs that bundle several
  perks into one subscription: Amazon Prime (shipping + video + music, not
  just Prime Video), Walmart+ (has included Paramount+ or Peacock),
  Costco/Sam's Club, Uber One, DoorDash DashPass, Instacart+.
- **`productivity`** — Apple One, Google One, Microsoft 365 Family.
- **`creditcard`** — Amex Platinum, Chase Sapphire Reserve/Preferred,
  Capital One Venture X. Verify against the issuer's current benefits page,
  not a generic card-name search — these change often. Personalized offer
  portals (Amex Offers, Chase Offers) can't be searched generically — tell
  the user to check their own account.
- **`stacking`** — combos across the above: student discounts, family/duo
  plan splitting, annual-vs-monthly discounts, a membership that already
  includes a streaming service.

`data/providers.json` has this same checklist with official domains — read
it, but never treat it as a source of truth for pricing; everything below
gets verified live.

## Step 2 — Search exhaustively, verify on the official domain

1. For every provider, run more than one query angle before concluding
   there's nothing — a single search missing a real offer is how deals get
   missed (e.g. searching only "ESPN standalone app" misses the separate
   Disney+/Hulu/ESPN bundle page, which is a materially different, cheaper
   offer). At minimum try: `"<provider> promo OR discount OR deal 2026"`,
   `"<provider> bundle"`, `"<provider> cash back OR gift card switch"`,
   `"<provider> student discount"`.
2. **The link you log must be the provider's own official domain
   (netflix.com, t-mobile.com, apple.com, ...) — never a blog, review site,
   news article, or forum thread.** This is the URL the user will click to
   actually act on the deal, not just a citation. If you can only confirm
   specifics via secondary reporting (common for credit-card benefit
   pages that block fetching), still find and use the provider's own page
   for the link — the secondary source is for fact-checking, not for the
   link field. If you genuinely cannot find an official page at all, don't
   log the deal.
3. Note conditions exactly as stated — plan tier, autopay, new-line
   requirement, enrollment steps.
4. Never invent a price, percentage, or promo name. If a number isn't
   explicitly stated by the source, leave the value fields blank rather than
   estimate or derive one.
5. Before finishing, do a quick self-check: which providers from Step 1 did
   you actually search, and which did you skip? If you're reporting fewer
   than a handful of results for a broad request like "check for subscription
   deals," that's a signal to go back and cover more of the checklist rather
   than stop early — a thin result set undermines trust in the whole tool.

## Step 3 — Write each entry so a customer can act on it, not just read it

For every deal, be explicit about:

- **What it actually is**, in one plain sentence — no unexplained
  abbreviations, rebrand names, or internal program names without saying
  what they mean for the customer. ("ESPN+ is now called ESPN Select" is a
  fact about ESPN's naming, not something a customer needs — what they need
  is "$11.99/mo gets you ESPN+ content; $29.99/mo also gets you live ESPN TV
  channels.")
- **Effort** — `low` (you likely already have the account/card; this is just
  enrolling in or redeeming an existing benefit), `medium` (a new,
  standalone subscription/membership — no need to switch anything you
  already use), or `high` (requires switching carriers/ISPs, opening a new
  account, or a new phone line). When a deal's effort genuinely depends on
  what the user already has (e.g. a credit-card credit assumes they hold the
  card), say so explicitly in the conditions rather than picking one label
  and hiding the assumption.
- **Value, only when the source states a clean number** — `monthly-value`
  for recurring savings/worth, `bonus-value` for one-time cash/gift-card
  amounts. Skip both rather than back into a number by doing math on a
  rounded percentage.
- **When there are multiple tiers of the same thing** (e.g. ESPN Select vs.
  Unlimited, or a bundle's ad vs. ad-free pricing), put the comparison in
  one entry so the customer can choose, rather than several entries that
  don't explain how to pick between them.

Tone: state facts plainly. No urgency language, no "don't miss out," no
picking a "best" deal for the user — you're providing information, not
selling anything. This is a deliberate design choice; keep it that way.

## Step 4 — Present results

Table: Provider | Deal | Effort | Conditions | Link. Group by category,
skipping empty ones. If the user mentioned what they already have (a
carrier, a card, a membership), lead with anything that stacks on top of it.

Close with one line: promo terms change and rotate (especially cash-back
amounts), so confirm the current details on the linked page before acting —
and, for a broad run, a one-line note on what was actually covered (e.g.
"checked streaming, carrier/ISP switch bonuses, and productivity bundles;
didn't get to credit-card portals this round") so the user knows the scope,
not just the results.

## Step 5 — Log it so tomorrow's run only shows what's new

```
python3 scripts/deal_log.py add \
  --provider "T-Mobile" --category carrier --effort high \
  --deal "Netflix Standard with Ads included free (\"Netflix on Us\")" \
  --conditions "Requires a qualifying plan; 1 per account" \
  --expires "ongoing" \
  --link "https://www.t-mobile.com/tv-streaming/netflix-on-us" \
  --monthly-value 8.99
```

`--link` and `--effort` are required (see Step 2 and Step 3 above).
`--monthly-value` / `--bonus-value` are optional — only pass them when the
source gave a clean number. Then show what's new:

```
python3 scripts/deal_log.py new-since-last-run
```

If the user just wants a one-off check with no logging, skip this step and
say so.

## Notes

- No live account access — it can't see what the user already has. If they
  tell you their carrier, card, or memberships, prioritize what stacks with
  those.
- Region matters (most sources are US-centric); ask if the user is
  elsewhere and results look off.
- If the user pushes back that results look incomplete or hard to trust,
  that's useful signal, not friction to route around — go broader on Step 2
  rather than defending what's already there.
