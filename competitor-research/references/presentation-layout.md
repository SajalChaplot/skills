# Presenting competitor reasoning

Use the user's requested medium. Separate the strategic argument from the broader evidence library so the reader can follow a recommendation without reading every feature cell. Preserve existing styling when refining an artifact.

## Tabbed HTML research presentation

The bundled `../assets/ai-spend-example.html` is a complete, offline example with embedded images, two tabs, product filtering and image inspection. Its facts are historical. Reuse its layout ideas and appropriate CSS/interaction patterns; replace the content, dates, cohort and sources for a new assignment. Do not depend on paths from the original workspace.

### Structure

**Header:** research question, scope, date checked, cohort/reference counts. Keep it brief.

**Tab 1 — Competitive reasoning:**

1. Lead with the recommendation and the job it serves.
2. Explain the small cohort and the role of each reference.
3. Compare evidence, product implications and design implications in adjacent columns.
4. Cover defaults, boundaries and competing explanations. Clearly distinguish observed behavior from hypotheses.
5. Present annotated UX teardowns beside real screenshots.
6. Follow the investigation with the counter-strategy and prioritized insight-to-action table.
7. Place the broader feature comparison, feature checklist and supplementary patterns in expandable sections. Keep evidence accessible without overwhelming the strategic argument.

**Tab 2 — Screenshots:** one section per product. Product name and research relevance, then a “Pattern to borrow” callout and a horizontal image strip. Put wider app views first. Each image has a title, image type, source/date/version context and a short explanation. Do not crop away information to fill a thumbnail.

### Layout behavior

- Comparison tables expand to their full height. Do not trap rows inside a vertically scrolling table. Use compact, readable type (approximately 12–13px for dense reference tables), tighter cell padding and horizontal overflow when needed. Keep long source text legible and preserve all detail.
- Use roughly 14–16px for body text and 20–28px for section headings. Product labels may remain visible during horizontal table scrolling. Avoid widths that force unnecessary horizontal travel.
- Group screenshots by product in separate horizontally scrollable strips, with visible scrollbars, previous/next buttons and a position counter. Support touch, keyboard and narrow viewports.
- Use click-to-enlarge inspection with fit-image/actual-size viewing, source link and previous/next navigation. Restore focus on close. Preserve the full image with contain sizing; do not label a crop as a full-page view.
- A useful annotation names the screen element and explains its consequence. Use numbered notes or markers tied to identifiable elements. Do not invent locations or overlay a redesigned control and call it competitor evidence.
- Put PM and design implications side by side. Keep evidence status and confidence close to the claim rather than burying them in a disclaimer.
- Prefer self-contained image embedding for a standalone HTML deliverable, or a portable relative asset folder in a complete bundle. Keep an image/source manifest.

### Bounded verification

Check the main content and a narrow viewport using permitted rendering tools when available. Verify tabs, product filters, strip arrows/counters, image viewer, source links and focus behavior. Check table expansion and source/image correspondence. A source or DOM check does not establish visual QA; say what could not be verified. Do not bypass a browser or access-policy block to obtain a preview.

## Deck storyboard

Use this when the user wants a presentation deck; use the available presentation-authoring workflow for the requested format. This guide does not itself require creating a deck.

| Slide / beat | Message | Visual arrangement |
|---|---|---|
| Decision and stakes | The job, trigger and consequence of failure | One problem statement and a short job journey; use supplied evidence, not invented market numbers. |
| Cohort | Why these references | A compact role/product/rationale table for the curated cohort. |
| Workflow teardowns | What works and where friction might remain | One product journey at a time: large real screen on the left, 2–3 numbered annotations on the right. Label hypotheses. |
| Defaults and boundaries | What happens without intervention | A concise default → consequence comparison; include source/version context and highlight meaningful differences. |
| Synthesis | The structural opportunity | Observation → interpretation → product implication → design implication. Use two or three strong findings rather than a wall of features. |
| Counter-strategy | Match the baseline; differentiate on the job | Side-by-side “match,” “differentiate” and “defer,” with evidence and tradeoffs. |
| Action and decision gates | What happens next | A short prioritized action table with responsibility, validation and dependency; include the decision being requested if applicable. |
| Appendix | Evidence and detailed comparison | Full feature tables, source links, research limitations and remaining screenshots. |

Adapt the number of slides to the argument. A four-reference cohort does not require equal slide counts. Use a consistent slide grid, stable source/footer placement, generous screenshot area and readable text; move detailed tables to the appendix rather than shrinking them until unreadable. Keep a product implication distinct from a design treatment on every findings slide.
