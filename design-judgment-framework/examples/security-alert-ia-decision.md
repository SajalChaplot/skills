# IA exploration case — security alert investigation

**Status:** Illustrative, reconstructed decision exercise. **No direct user evidence or outcome claim.**

## Design question

Which primary organizing structure best supports a security analyst who needs to prioritize critical alerts, investigate evidence, and coordinate remediation?

## Inputs

**Provisional primary job:** security triage and investigation. Affected secondary users include incident responders and service/platform owners. Critical constraints include security authorization for remediation, continued access to important alerts, privacy and accessibility.

**User-supplied task priorities:** Efficiency 90, Information density 80, Discoverability 55, User control 95, Guidance 70, Flexibility 70, Consistency 85, Simplicity 80. These are stated relative priorities, not empirical findings.

## Structurally different candidates

| IA alternative | Primary entry | Advantage | Failure mode |
|---|---|---|---|
| Alert-centered | Alert queue and alert detail | Direct granular triage and investigative pivots | Related signals may remain fragmented |
| Workflow-centered | Triage → Investigate → Remediate → Resolve | Clear next steps and operational stages | Forces expert work into staged navigation |
| Resource-centered | Asset/service inventory | Strong system and ownership context | Makes global severity triage difficult |
| Incident-centered | Correlated incident queue | Related alerts can become coherent cases | Depends on accurate grouping and accessible raw alerts |

## Provisional comparison (illustrative scores, not research)

Using authored fit estimates from `security-alert-ia.json`, the preference model ranks:

1. Alert-centered: **87.79/100**
2. Incident-centered: **80.96/100**
3. Workflow-centered: **74.91/100**
4. Resource-centered: **73.58/100**

These numbers are a deliberately simplified preference exercise. The model does **not** know which architecture matches users' mental models or whether these fit assumptions are true. Reweighting only for guidance changes the top estimate to workflow-centered, illustrating that the result depends on selected values.

## Conditional working recommendation

**Primary IA:** alert-centered around a stable alert object.

**Secondary aids:** workflow next-step guidance in the alert context; resource/asset filters and cross-links; related incident grouping only when trustworthy; AI assistance where investigation happens rather than as a competing top-level destination.

The hybrid must retain a single declared primary organizing principle. The other structures are contextual overlays, not four equal competing primary entry points.

### Reasons to reverse

- If validated correlation substantially improves investigation task success, consider incident-first.
- If the primary jobs actually start from known services/resources, consider resource-first.
- If novice or regulated remediation is dominant, test workflow-first with explicit decision steps.

## Evidence and validation required before UI commitment

1. Interview/observe analysts and responders; identify actual entry points, object vocabulary, and frequency of non-linear pivots.
2. Compare candidate hierarchies in tree tests on the same triage, investigation and resource-location tasks.
3. Task-test low-fidelity navigation with deep links, missing evidence, grouped alerts and permission restrictions.
4. Measure findability, wrong turns, task completion, context switches and recovery; do not fabricate click counts or completion times.
5. Audit security and accessibility constraints separately from preference fit. Validate incident correlation before relying on incident-first organization.

**Design agent handoff:** do not finalize screen layout from this preference ranking alone. Use the `design-information-architecture` skill, record gaps and risk, then proceed to screen-level exploration only with a labeled provisional IA or validated decision.
