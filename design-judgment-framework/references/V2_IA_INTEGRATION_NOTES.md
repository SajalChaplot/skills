# Forward compatibility: IA exploration and V2 contextual preference engine

V1.1 intentionally adds information architecture **as a separately inspectable stage** instead of hiding structural decisions in screen scoring. It does not implement V2's persona/domain parameter resolution.

## V2 should build on these artifacts

1. Use V2 context resolver to identify user jobs, competing beneficiaries, object complexity and whether IA exploration is warranted.
2. Retrieve domain evidence and IA precedents with source links, confidence and applicability conditions.
3. Dynamically recommend **IA-appropriate** dimensions with descriptors/rubrics and evidence provenance. Avoid repeating every globally available slider or conflating information density with simplicity.
4. Let the designer override organization and task weights; show suggested versus effective values and what changed.
5. Support per-persona IA task walkthrough ratings and multi-job navigation, not only one weighted scalar.
6. Test sensitivity and alternative structures; hard constraints and unverified critical technology dependencies are independent gates.
7. Feed the provisional or validated primary IA into downstream screen concepts and wireframes. Keep revision triggers in the decision record.
8. Associate successful IA validation evidence with the precise persona/job, domain, workflow stage and design version; do not silently turn inferred competitor patterns into rules.

## Compatibility

- The original eight V1 axes remain unchanged in `scripts/evaluate.py` and `profiles/preferences.json`.
- `scripts/evaluate_ia.py` reads **case-defined** IA axes and weights from a separate file. There is no automatic mapping in V1.1.
- Avoid a breaking API change by introducing a future `resolved_ia_profile` object with mappings and provenance; preserve V1 tasks and overrides when migrating.
- The new `information_architecture` stage is optional only with an explicit skip reason and stays before UI `options`.
