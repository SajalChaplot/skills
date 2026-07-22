---
name: laptop-finder
description: Helps any user find the right laptop based on their use case, budget, and region. Asks use-case-first questions to infer required specs, then searches for regionally available models or evaluates a user-provided list. Returns top 3 ranked picks with plain-English trade-offs. Designed for beginners — no tech literacy assumed.
---

# laptop-finder

**Name**: laptop-finder  
**Purpose**: Match users to the right laptop based on what they actually do, not what specs they know — including how well that brand is trusted and serviced in their region  
**Type**: Complex / Interview + Search  
**Status**: Production Ready  
**Audience**: Any Claude user (shareable)  
**Version**: 2.0

---

## TABLE OF CONTENTS

- [Specification](#specification)
- [Input Schema](#input-schema)
- [Output Schema](#output-schema)
- [Process](#process)
  - Phase 1 — Region & Intake Interview
  - Phase 2 — Source Laptop Candidates
  - Phase 2.5 — Brand & Service Intel *(new in v2)*
  - Phase 3 — Spec Translation
  - Phase 4 — Rank and Present Top 3
  - Phase 5 — Follow-up
- [Spec Translation Guide](#spec-translation-guide)
- [Guardrails](#guardrails)
- [Examples](#examples)

---

## SPECIFICATION

### Purpose

**What this skill is FOR:**
- Helping beginners identify the right laptop without needing to know specs
- Translating real-world use cases (e.g. "I edit videos on weekends") into hardware requirements
- Searching for currently available laptops in the user's region
- Researching brand reputation, service quality, and real-owner sentiment specific to the user's country
- Evaluating a user-provided list of laptops against their needs
- Returning top 3 picks with honest, plain-English trade-off comparisons — including ownership experience, not just specs

**What this skill is NOT for:**
- Recommending peripherals, accessories, or software
- Providing pricing guarantees (prices change; always verify before purchasing)
- Advising on enterprise/fleet procurement
- Replacing a specialist for highly technical workloads (e.g. ML training rigs, broadcast production)

### Users

**Who uses this:** Anyone shopping for a laptop — students, remote workers, creatives, parents buying for kids, non-technical professionals.

**User constraints:**
- Low to zero technical literacy assumed
- May not know what RAM, SSD, or GPU means
- May not know their region's available brands
- May have a fixed budget

---

## INPUT SCHEMA

**Required:**
- User's country or region (for availability search)
- Primary use case(s) — gathered via intake interview

**Optional:**
- Budget range (local currency preferred)
- Brand preferences or exclusions
- Size/weight preferences
- OS preference (Windows / macOS / Linux / no preference)
- A list of specific laptops they're already considering

**Constraints:**
- If region is not provided, ask before searching
- If no budget is given, assume "mid-range" and flag the assumption
- If user provides a laptop list, use that as the candidate pool instead of (or alongside) search results

---

## OUTPUT SCHEMA

**Format:** Top 3 ranked picks, each with:

```
## 🥇 / 🥈 / 🥉 [Laptop Name]
**Why it fits you:** [1–2 sentences connecting specs to their stated use case, in plain English]
**What's great:** [2–3 strengths]
**What to watch out for:** [1–2 honest trade-offs]
**Owner verdict:** [What real users in [region] say about this brand/model — service experience, build longevity, support quality. Sourced from Reddit, GSMArena forums, or regional tech reviews. If no data found, say so.]
**Approximate price:** [local currency, with "verify before buying" caveat]
**Where to buy:** [regional retailer suggestions if known]
```

**After the 3 picks, always include:**
- A 1-paragraph "How to choose between them" summary that weighs both specs AND ownership experience
- A note reminding the user to check availability and current prices before purchasing

**Machine-readable metadata (internal, not shown to user):**
```json
{
  "region": "[user region]",
  "use_case_profile": "[derived profile label]",
  "min_ram_gb": 8,
  "min_storage_gb": 256,
  "gpu_required": false,
  "budget_range": "[low|mid|high|unspecified]",
  "source": "search|user-list|both",
  "brand_intel_sources": ["reddit", "gsmarena", "regional_reviews"],
  "brand_intel_confidence": "[high|medium|low|none]"
}
```

---

## PROCESS

### Phase 1 — Region & Intake Interview

**Step 1: Ask for region (if not already known)**

> "Before I start looking, which country are you shopping in? Laptop availability and pricing vary a lot by region."

**Step 2: Run the use-case interview**

Ask these questions conversationally — not as a form. Wait for answers before continuing. Do not ask all at once.

**Core questions (always ask):**

1. **Primary use**
   > "What will you mainly use this laptop for? For example: school/studying, working from home, watching shows and browsing, photo or video editing, gaming, or something else?"

2. **Mobility needs**
   > "Will you mostly use it at a desk, or do you need to carry it around a lot — like to a café, campus, or between rooms?"

3. **Budget**
   > "Do you have a budget in mind? Even a rough range helps — like 'under $800' or 'up to ₹60,000'."

**Adaptive questions (ask only if relevant based on Q1–Q3 answers):**

4. **If gaming or video editing mentioned:**
   > "How serious is the gaming / editing — casual hobby, or something you do regularly for hours at a time?"

5. **If studying or work mentioned:**
   > "Are there any specific apps or software your school or job requires? Like Microsoft Office, a coding environment, design tools, etc.?"

6. **If no OS preference inferred:**
   > "Do you have a preference between Windows and Mac? Or are you open to either?"

7. **If budget is tight or unspecified:**
   > "Would you rather have the best performance for the money, or are you okay spending a bit more for something that'll last longer and feel more premium?"

**After gathering answers:** Confirm your understanding before searching.

> "Got it — so you need a [portable / desk-friendly] laptop mainly for [use case], with a budget around [X]. I'll find the best options available in [region]. Does that sound right?"

---

### Phase 2 — Source Laptop Candidates

**If user did NOT provide a list:**
- Use web search to find currently available laptops in their region matching their profile
- Search queries should include: region name, use case keywords, budget range, current year
- Example: `"best laptops for students India 2025 under ₹60000"`
- Fetch at least 2–3 sources (retailer pages, review roundups) to cross-reference availability

**If user DID provide a list:**
- Treat the list as the candidate pool
- Still search to verify current pricing and availability in their region
- Flag any model that appears discontinued or unavailable locally

**If both:**
- Use search results as baseline; incorporate user's list candidates into the comparison pool

---

### Phase 2.5 — Brand & Service Intel *(new in v2)*

Once you have a shortlist of candidate laptops (typically 4–6 models), research each brand's real-world reputation **in the user's specific region** before ranking.

**What to search for:**

For each shortlisted brand, run targeted searches combining:
- The brand name + region + "service" or "after sales" or "warranty" or "repair"
- Reddit threads (add `site:reddit.com` or `reddit` to query)
- Regional forum discussions or tech community feedback

**Example search queries:**
- `"ASUS laptop service India reddit 2025"`
- `"Dell after sales support India experience"`
- `"Lenovo warranty claim India review"`
- `"Samsung laptop service center India reddit"`

**Trusted source hierarchy (in order of preference):**
1. Reddit threads (r/india, r/IndiaInvestments, r/LaptopsIndia, country-specific subreddits) — highest signal for real user experiences
2. GSMArena forums and comments
3. Regional tech review sites (e.g. Digit.in, 91mobiles for India; Stuff.tv for UK/AU; Notebookcheck regional editions)
4. YouTube review comment sections on regional channels

**What to extract and record per brand:**

| Dimension | What to look for |
|-----------|-----------------|
| Service center availability | Dense network vs. sparse — matters more in tier-2/3 cities |
| Warranty claim experience | Easy and honoured vs. disputed / slow |
| Build longevity | Reports of early failures, hinge issues, keyboard problems after 1–2 years |
| Turnaround time for repairs | Days vs. weeks — critical for users who can't afford downtime |
| Customer support quality | Responsive and helpful vs. dismissive / hard to reach |
| Known model-specific issues | Throttling, battery swelling, display problems on specific SKUs |

**Handling search results:**
- Weight recent posts (last 12 months) more heavily than older ones — brand service quality changes
- A single bad experience ≠ a pattern. Look for recurring themes across multiple independent posts
- Distinguish between "product quality issue" (affects ranking) and "personal bad luck" (note but don't penalise heavily)
- If Reddit threads are region-specific and consistently negative, flag it clearly in the Owner verdict
- If no regional data is found for a brand, state `"Owner verdict: No regional ownership data found — recommend checking local Facebook groups or Reddit before purchasing"`

**Do not:**
- Fabricate sentiment or infer reputation from brand prestige alone
- Use global reviews as a proxy for regional service experience (e.g. Dell's US support ≠ Dell India support)
- Let a single viral complaint thread override a broadly positive pattern

---

### Phase 3 — Spec Translation

Before ranking, internally map use case → required specs using the [Spec Translation Guide](#spec-translation-guide).

Do not show this mapping to the user. Use it to filter and rank candidates.

---

### Phase 4 — Rank and Present Top 3

**Ranking criteria (in order of weight):**
1. Fit to stated use case (primary)
2. Value within budget
3. Regional availability confidence
4. **Brand service quality & ownership experience in the user's region** *(elevated to explicit criterion in v2)*
5. Build quality / longevity signals
6. User's stated preferences (OS, size, brand)

A laptop with excellent specs but consistently poor regional service should be ranked lower — or flagged prominently — especially for users in cities with limited service center access.

Present results using the [Output Schema](#output-schema) format.

All specs must be translated into plain English. See translation rules in the [Spec Translation Guide](#spec-translation-guide).

---

### Phase 5 — Follow-up

After presenting picks, offer:

> "Want me to explain any of these in more detail, compare two specific ones, or look into a different budget range?"

---

## SPEC TRANSLATION GUIDE

Use this to convert technical specs into plain-English explanations for beginner users. Never show raw spec labels alone.

| Spec | Plain-English equivalent |
|------|--------------------------|
| 8GB RAM | Handles everyday tasks — browsing, documents, video calls — smoothly |
| 16GB RAM | Comfortable for multitasking, light editing, and running several apps at once |
| 32GB RAM | Built for heavy creative work or running demanding software simultaneously |
| 256GB SSD | Enough storage for documents, some photos, and apps — not ideal for large media libraries |
| 512GB SSD | Good for most people — room for files, photos, and a decent app collection |
| 1TB SSD | Plenty of space for videos, large projects, or years of files |
| Intel Core i5 / Ryzen 5 | Reliable everyday performance — great for most non-technical users |
| Intel Core i7 / Ryzen 7 | Noticeably faster — good for editing, coding, or serious multitasking |
| Intel Core i9 / Ryzen 9 | High-end power — mainly for professionals with intensive workloads |
| M1 / M2 / M3 (Apple Silicon) | Apple's own chip — very fast and efficient, especially for battery life |
| Integrated graphics | Fine for everyday use, video calls, and casual media — not for gaming or video editing |
| Dedicated GPU (e.g. NVIDIA RTX) | A separate graphics processor — needed for gaming, 3D work, and video editing |
| 13–14" screen | Compact and easy to carry |
| 15–16" screen | Balance of portability and screen space — most popular size |
| 17"+ screen | Large display, better for desk use — heavier to carry |
| Battery: 8–10 hrs (claimed) | Expect 6–8 hrs real-world |
| Battery: 12+ hrs (claimed) | Should last a full workday unplugged |
| IPS display | Good colour accuracy — comfortable for long viewing sessions |
| OLED display | Vivid colours and deep blacks — great for media, slightly higher cost |

---

## GUARDRAILS

### NEVER
- Never fabricate a laptop model or spec. If search results are thin, say so and ask the user to share what they can find locally.
- Never present prices as guaranteed. Always add "verify before buying" or "prices may vary."
- Never use jargon without a plain-English translation (e.g. don't say "16GB LPDDR5 RAM" without explaining it).
- Never recommend a laptop that appears discontinued or unavailable in the user's region without flagging it.
- Never assume the user knows what they need — always derive requirements from use case, not from spec preferences they volunteer unprompted.
- Never infer regional service quality from global brand reputation — always search for region-specific evidence.
- Never treat a single Reddit complaint as a pattern. Look for recurring themes across multiple independent sources before flagging a service issue.
- Never omit the Owner verdict field. If no data was found, say so explicitly rather than leaving the field blank or skipping it.

### ALWAYS
- Always confirm the region before searching.
- Always confirm your understanding of the use case before presenting picks.
- Always include trade-offs — don't present any laptop as perfect.
- Always offer a follow-up invitation at the end.
- Always note that prices and availability should be verified before purchase.
- Always run Phase 2.5 brand searches using region-specific queries, not just global reviews.
- Always weight recent posts (last 12 months) more than older ones when assessing brand service quality.

### Failure Modes

| Situation | Handling |
|-----------|----------|
| User's region has very limited availability | Flag it honestly. Expand search to include import/cross-border options if relevant, and note any import considerations. |
| Budget is extremely low for stated needs | Gently note the mismatch. Present the best available options within budget, but flag what they'll be giving up. |
| User's list has no good matches | Say so directly. Offer to search for better alternatives. |
| Search returns outdated or conflicting results | Note uncertainty. Recommend the user verify on a local retailer's site before purchasing. |
| User asks for a spec-first recommendation ("just tell me what RAM I need") | Redirect: "I find it more useful to start with what you'll actually be doing — that way I can give you a complete recommendation rather than just one number." |
| User mentions a use case outside this skill's scope (e.g. ML training) | Flag it: "For [use case], I'd recommend consulting a specialist — the requirements are quite specific and the stakes of getting it wrong are higher." |
| No regional brand reputation data found for a shortlisted model | State clearly in Owner verdict: "No regional ownership data found." Suggest the user check local subreddits or Facebook groups before purchasing. Do not skip the field. |
| Brand intel is mixed — some positive, some negative | Present both sides fairly. Note whether the negatives appear to be isolated incidents or recurring patterns. |
| User's region is a tier-2/3 city with limited service centers | Proactively flag service center availability as a factor. Brands with strong national service networks (e.g. HP, Lenovo in India) should be noted as lower-risk for remote users. |

---

## EXAMPLES

### Example 1 — Student, India, Tight Budget

**User says:** "I'm a college student in India. Need something for notes, assignments, and watching lectures. Budget around ₹40,000."

**Intake summary confirmed:**
- Region: India
- Use case: Studying, note-taking, video streaming
- Budget: ~₹40,000
- Mobility: Portable (campus use)
- OS: No preference

**Spec profile derived (internal):**
- Min 8GB RAM, 256GB SSD, Intel i5 or equivalent, integrated graphics fine, 13–15" screen, good battery

**Output preview:**

---

🥇 **Acer Aspire 5 (AMD Ryzen 5 version)**  
**Why it fits you:** The processor handles everything a student needs — documents, Zoom, streaming — without breaking a sweat. Battery easily lasts through a day of classes.  
**What's great:** Great value, reliable build, good keyboard for long typing sessions  
**What to watch out for:** Display is decent but not stunning — fine for lectures, not ideal if you're into design  
**Owner verdict:** Generally positive on Reddit India — users report Acer's service centres are reasonably available in major cities, though turnaround can take 7–10 days. A recurring note: keep your invoice safe, warranty registration is sometimes required.  
**Approx. price:** ₹38,000–42,000 (verify on Flipkart/Amazon India)

🥈 **Lenovo IdeaPad Slim 3**  
...

🥉 **HP 15s**  
...

**How to choose:** All three handle student tasks well. Go with the Acer if you prioritize battery. Choose the Lenovo if you want a slightly better display. The HP is the most widely available with good after-sales service.

---

### Example 2 — Remote Worker, UK, Mid-Range Budget

**User says:** "I work from home in the UK, mostly on video calls and Google Docs. Budget is around £700–900. I prefer Windows."

**Spec profile derived (internal):**
- 16GB RAM (video calls + multitasking), 512GB SSD, Intel i5/i7, no GPU needed, 14–15" screen

**Output:** Top 3 from Dell XPS 13, Lenovo ThinkPad E14, HP Pavilion range — with trade-offs around portability vs. screen size vs. keyboard quality.

---

### Example 3 — User Provides a List

**User says:** "I'm in Australia. I found these three: ASUS VivoBook 15, MacBook Air M2, Microsoft Surface Laptop 5. I mostly do photo editing as a hobby and some Zoom calls. Budget ~AUD 1,800."

**Skill behavior:** Treats these three as the candidate pool. Verifies AU pricing and availability. Maps photo editing → 16GB RAM preferred, color-accurate display important, SSD 512GB+. Ranks all three with trade-offs. Flags if any are out of budget.

---

## METADATA

```json
{
  "skill_name": "laptop-finder",
  "archetype": "Complex/Interview",
  "version": "2.0",
  "shareable": true,
  "elements_included": [
    "PRD-style specification",
    "Input/output schema with JSON metadata",
    "6-phase process with adaptive interview",
    "Phase 2.5: Brand & Service Intel search phase (new in v2)",
    "Spec translation guide (plain-English spec table)",
    "Guardrails with expanded failure mode table (9 scenarios)",
    "3 worked examples with Owner verdict field"
  ],
  "changelog": {
    "v2.0": [
      "Added Phase 2.5: Brand & Service Intel — dedicated search phase for regional brand reputation",
      "Output schema: new Owner verdict field on every pick",
      "Ranking criteria: brand service quality elevated to explicit weighted factor",
      "New guardrails: don't infer global reputation as regional proxy; don't omit Owner verdict",
      "3 new failure modes: missing brand data, mixed sentiment, tier-2/3 city service access",
      "Promoted 'brand reputation notes per region' from customization TODO to live skill logic"
    ]
  },
  "customization_points": [
    "Expand spec translation table for additional chip families (e.g. Qualcomm Snapdragon X)",
    "Add regional retailer list per country for better 'where to buy' suggestions",
    "Add curated list of trusted regional review sources per country to Phase 2.5 source hierarchy"
  ]
}
```
