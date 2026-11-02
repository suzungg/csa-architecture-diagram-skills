# Two-case pilot: CSA package versus no diagram skill

**Executed 2026-11-02. No general quality, speed or cost advantage established.**
Four fresh generation contexts produced two paired first drafts. The pilot
demonstrates useful quality gates and exposes limitations; it is not a
statistically meaningful or fully controlled model benchmark.

## What was held constant

Both conditions received [the same technical briefs](briefs.json), canonical
graph/ownership/intent metadata, 1600 x 1000 source canvas, minimum 14-unit Arial
labels, approved asset access, native draw.io requirements and evaluation
criteria. No private customer content or live cloud access was involved.

The baseline was explicitly prohibited from reading any diagram skill,
helper/example/checker source or sibling output. CSA read the repository skill
directly and could use its helpers/examples. Both conditions could select
official icons or neutral symbols. Baselines chose neutral shapes; CSA chose
official icons. This tests the **package**, not prose alone.

The host used its default general-purpose agent configuration; exact resolved
model/settings, seed, token cost and comparable elapsed generation time were
not exposed/recorded. There was no host-loader activation. Agent declarations
of material read are recorded in [run metadata](run-metadata.json); they are
self-reports, not an independent access audit.

## First-draft findings

Counts below are automated findings, **not an overall quality score**.
Coverage warnings are separated from defects. The parent inspected all images;
review was not blinded and was performed by the skill author.

| Case / condition | Graph/ownership errors | Reserved-box warnings | Browser text findings | Coverage warnings | Confirmed material issue |
| --- | ---: | ---: | ---: | ---: | --- |
| Foundry / no skill | 0 | 1 | 0 | 7 | None observed; box overlap did not overlap actual text |
| Foundry / CSA | 1 | 0 | 0 | 0 | Support-agent caption/group extended outside its project |
| Fabric / no skill | 0 | 0 | 2 | 16 | Scoring title exceeded its slot and crowded its caption; one underlying layout issue |
| Fabric / CSA | 0 | 1 | 0 | 0 | None observed; overlapping reserved label boxes had separated actual text |

No required nodes or directed graph relationships were missing in any first
draft. Automatic routing/edge-label placement accounts for the baseline
coverage warnings; these are **not counted as visual defects**. Browser
measurement caught the baseline Fabric issue and the ownership check caught
the CSA Foundry issue.

## Correction-stage deviation

One feedback opportunity per condition was planned and attempted. The host
rejected all four follow-up messages because synchronous task agents cannot
receive follow-ups. No agent repair turns or repair-time advantage can be
claimed.

Instead, the parent made documented, minimal derivatives:
Foundry/CSA project height 190 -> 220; Fabric/baseline title y/height 16/28 ->
8/44 and caption y 49 -> 60. The other two drafts were copied unchanged.
[corrections.json](corrections.json) records every operation. This is **one
parent correction pass for each affected condition**, not autonomous model
repair performance. All original first drafts remain byte-preserved.

Both confirmed issues were resolved. The two visually harmless reserved-box
warnings remain visible; findings were not suppressed merely to obtain green
results. The `final` filename denotes the reviewed derivative, not a deployment
approval; original first-draft footer text is retained where present.

## Rename/move exercise

On separate copies, the parent appended ` v2` to the first component's label and
moved its parent geometry 20 units right; nested descendants moved with it.
This was a programmatic XML edit, **not an interactive draw.io UI usability test**.
All endpoints and graph relationships remained attached.

Three copies introduced no new observed issue. Fabric/CSA developed a diagonal
first segment on an explicit-waypoint route, confirmed in the image and flagged
as unchecked geometry. Its original evidence is retained, not repaired to
inflate the result. Explicit routes offer checkability at the cost of manual
rerouting after some edits. Always rerun checks and inspect after moving nodes.

## Evidence and reproduction

[results.json](results.json) contains all first/derivative/edit measurements.
The [input snapshot](input-snapshot.zip) preserves the text/scripts/catalogs
available during the trials; file hashes are in the run metadata. It excludes
binary previews and SVG assets, which remain separately pinned in their catalogs.
Each run folder retains source, PNG, render hashes, checker output and browser
measurements, including the negative cases.

| Run | First draft | Reviewed derivative | Edit exercise |
| --- | --- | --- | --- |
| Foundry / no skill | [PNG](runs/foundry-baseline/first.png) / [source](runs/foundry-baseline/first.drawio) | [PNG](runs/foundry-baseline/final.png) | [PNG](runs/foundry-baseline/edit.png) |
| Foundry / CSA | [PNG](runs/foundry-csa/first.png) / [source](runs/foundry-csa/first.drawio) | [PNG](runs/foundry-csa/final.png) | [PNG](runs/foundry-csa/edit.png) |
| Fabric / no skill | [PNG](runs/fabric-baseline/first.png) / [source](runs/fabric-baseline/first.drawio) | [PNG](runs/fabric-baseline/final.png) | [PNG](runs/fabric-baseline/edit.png) |
| Fabric / CSA | [PNG](runs/fabric-csa/first.png) / [source](runs/fabric-csa/first.drawio) | [PNG](runs/fabric-csa/final.png) | [PNG](runs/fabric-csa/edit.png) |

Run `python .\benchmarks\score.py` from the skill folder to recompute source,
contract and preview findings and verify recorded browser measurements against
source hashes. Fresh browser measurements require the optional
[local rendered checker](../references/quality-checks.md); `score.py` does not
silently claim to rerender. PNGs use the same draw.io width setting; draw.io
crops to content, so different margins can change apparent text scale.

The test cases resemble bundled examples and may favor package/template reuse.
Only one generation per condition/case was performed. Reliable performance
claims require repeated cases, recorded model/settings/cost, a supported
agent-feedback mechanism, blind reviewers and more varied architectures.
Microsoft's respective [Foundry](../assets/foundry/README.md) and
[Fabric](../assets/fabric/README.md) terms/notices still apply to embedded icons.
