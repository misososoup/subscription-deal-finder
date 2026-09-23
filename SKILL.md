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

## Step 2 — Search exhaustively, verify on the official domain, every single run

Subscription pricing changes constantly and is past this model's training
cutoff. **Every run does a fresh live web search, every time — nothing here
is ever served from a stored file or cached from an earlier run.** If a user
asks the same question twice in a row, or asks something a prior run already
covered, search again anyway; don't reuse a number from earlier in the
conversation. (`deals_log.json`, in Step 5, is a separate thing — it never
supplies pricing; see that step for what it's actually for.)

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
   requirement, enrollment steps. (What counts as a "condition" is defined
   precisely in Step 4 — read that before writing this field.)
4. Never invent a price, percentage, or promo name. If a number isn't
   explicitly stated by the source, leave the value fields blank rather than
   estimate or derive one.
5. Before finishing, do a quick self-check on scope: if the user asked a
   broad, unscoped question ("check for subscription deals"), which
   providers from Step 1 did you actually search, and which did you skip?
   Thin results on a broad ask undermines trust, so go back and cover more
   rather than stop early. If instead the user asked about one specific
   thing ("how do I watch the US Open", "any deals on Spotify"), searching
   just that thing *is* full coverage — there's no separate scope check
   needed, and nothing to caveat about other categories you didn't touch.

## Step 3 — Write each entry so a customer can act on it, not just read it

For every deal, be explicit about:

- **What it actually is**, in one plain sentence — no unexplained
  abbreviations, rebrand names, or internal program names without saying
  what they mean for the customer. ("ESPN+ is now called ESPN Select" is a
  fact about ESPN's naming, not something a customer needs — what they need
  is "$11.99/mo gets you ESPN+ content; $29.99/mo also gets you live ESPN TV
  channels.")
- **Whether they might already have this for free**, before anything else.
  Check whether an existing provider, plan, or membership the customer
  plausibly already holds already includes what they're asking about (a
  cable/streaming bundle that already carries a channel, a card benefit
  they may already hold, a membership that already bundles the service) and
  put that option first, clearly marked as "if you already have X, this is
  included at no extra cost." Never push a new subscription past a free
  path the customer might already have — the point of this tool is to help
  someone spend less, not more.
- **Effort, as an internal sort order only — never a label shown to the
  customer.** Rank each entry `low` (they likely already have the
  account/card; this is just enrolling in or redeeming an existing benefit),
  `medium` (a new, standalone subscription/membership — no need to switch
  anything they already use), or `high` (requires switching carriers/ISPs,
  opening a new account, or a new phone line) so you can order results
  easiest-first (see Step 4) and so `deal_log.py --effort` (Step 5) has a
  value to store for the dashboard's sort control. Do not print "Effort:
  low/medium/high" or any equivalent phrasing in the answer itself —
  customers don't need the internal label, only the ordering it produces.
  If a deal's effort genuinely depends on what the customer already has
  (e.g. a credit-card credit assumes they hold the card), that dependency
  belongs in the conditions text (Step 4), not as a hidden assumption
  behind a single label.
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

Table: **Provider | Deal | Conditions | Link.** No Effort column — effort
only determines the order rows appear in (easiest/already-have-it first,
then new standalone subscriptions, then anything requiring a switch), it is
never printed as its own field. Group by category, skipping empty ones. If
the user mentioned what they already have (a carrier, a card, a
membership), or if a free/already-included path exists (see Step 3), lead
with that before any paid option.

**Conditions holds only genuine eligibility or requirement facts the source
stated** — region restriction ("US only"), age minimum, a required plan
tier, "new customers only," enrollment steps. It is not a place to restate
the deal's effort level in prose — don't write things like "standalone, no
switching needed"; that's effort information in different words, and effort
isn't shown to the customer at all (see Step 3). If a condition genuinely
has nothing to add beyond the region, just say the region.

When the user asked about a specific thing they want to watch/use/get
(rather than a broad "check for deals"), answer directly and plainly
whether a current way to get it exists, and lead with that answer — don't
preface it with what you did or didn't check (see Step 2.5); that's the
answer they asked for, not a scope report.

Close with one line: promo terms change and rotate (especially cash-back
amounts), so confirm the current details on the linked page before acting.
For a broad, unscoped run only, also add a one-line note on what was
actually covered (e.g. "checked streaming, carrier/ISP switch bonuses, and
productivity bundles; didn't get to credit-card portals this round") —
skip this note for a scoped, specific request (see Step 2.5).

## Step 5 — Log it so tomorrow's run only shows what's new

`deals_log.json` is **not a price cache and is never a source for an
answer.** Every number in every response, including a second run on the
same day, comes from a fresh live search performed in that run (Step 2).
All this log does is remember which *exact* deals you've already shown the
user, so that a repeat daily run can say "nothing new since yesterday"
instead of re-listing the same things — it plays no role in figuring out
what the current price or offer is.

```
python3 scripts/deal_log.py add \
  --provider "T-Mobile" --category carrier --effort high \
  --deal "Netflix Standard with Ads included free (\"Netflix on Us\")" \
  --conditions "Requires a qualifying plan; 1 per account" \
  --expires "ongoing" \
  --link "https://www.t-mobile.com/tv-streaming/netflix-on-us" \
  --monthly-value 8.99
```

`--link` and `--effort` are required (see Step 2 and Step 3 above) even
though neither is shown to the customer directly — `--link` becomes the
clickable CTA, `--effort` only drives sort order and the dashboard's sort
control. `--monthly-value` / `--bonus-value` are optional — only pass them
when the source gave a clean number. Then show what's new:

```
python3 scripts/deal_log.py new-since-last-run
```

If the user just wants a one-off check with no logging, skip this step and
say so.

## Notes

- No live account access — it can't see what the user already has. If they
  tell you their carrier, card, or memberships, prioritize what stacks with
  those, and always check for a free/already-included path before a paid
  one (Step 3).
- Region matters (most sources are US-centric); ask if the user is
  elsewhere and results look off.
- If the user pushes back that results look incomplete or hard to trust,
  that's useful signal, not friction to route around — go broader on Step 2
  rather than defending what's already there.
