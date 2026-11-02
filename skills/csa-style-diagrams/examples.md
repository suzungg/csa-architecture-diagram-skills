# Trial prompts and acceptance criteria

Use synthetic material for evaluation. Record the host, model, tools, prompt,
output and actual results. A well-written instruction file is not evidence
that the host will execute it correctly.

The [annotated Fabric example](examples/fabric-batch/README.md) is a real editable,
rendered example; the scenarios below are broader host/model trials. The
[regression tests](tests/test_diagrams.py) exercise synthetic structural and
geometry defects locally, not the agent's skill invocation.

## 1. Faithful landing-zone recreation

Prompt:

> Recreate this Agent Landing Zones image in draw.io. Keep Garage, Runway and
> Application groupings and all visible service labels. Do not redesign it.

Expected:

- Reference image is actually inspected.
- Relative layout, repeated groups and labels are preserved.
- No invented peering or runtime arrows.
- Editable labels and boundaries; crop-based icons disclosed if used.
- Ambiguous "Project = Workspace" recorded without asserting equivalence.

## 2. New architecture from an incomplete brief

Prompt:

> Design a private agent platform with shared services and two application teams.

Expected:

- Consequential questions about hosting, networking, identity and isolation.
- No guessed production region or fabricated private-connectivity guarantees.
- Typed boundaries and prominent native/official service symbols where available.
- Proposed choices and unknowns distinguished from verified support.

## 3. No icon library

Prompt:

> Make a diagram for services outside the bundled Foundry icon subset, but no
> suitable local icons or network downloads are available.

Expected:

- Use available supported native shapes, or disclose labeled neutral substitutes.
- No invented shape identifiers, broken image URLs or fake logos.
- No claims that neutral symbols are official icons.

## 4. Missing renderer

Prompt:

> Create an editable diagram and preview with the available tools.

Environment: source writing works, but local export or image viewing is absent.

Expected:

- Available editable source delivered.
- Preview or visual review explicitly reported incomplete.
- No upload to an external rendering site as a hidden workaround.

## 5. Revise one component

Prompt:

> Replace the application database in this draw.io file; leave the rest unchanged.

Expected:

- Reads existing source and preserves unrelated edits/layout.
- Clarifies replacement technology if unspecified.
- Updates only relevant symbols, labels and relationships.
- New PNG is exported from the revised source, not reused from the baseline.

## 6. Resist infographic styling

Prompt:

> Create a clean enterprise architecture diagram, not a presentation infographic.

Expected:

- White canvas; modest overall title; short labels; clear section hierarchy.
- Blue/cyan section bars, light group fills and meaningful step markers are
  allowed; they must not be rejected as inherently infographic-like.
- Layout follows relationships rather than equal-sized cards.
- No unnecessary huge legend, slogan, shadows or decorative gradient.
- Clean alignment without forcing unrelated groups into a grid.

## 7. Inspectability and portability

Open the final draw.io file in the target editor, move an individual service,
edit its label and inspect the export.

Expected:

- Separate objects remain editable.
- No personal paths, expiring URLs or external private dependencies.
- Final image matches the final source.
- Asset rights and raster/vector limitations are documented.

## 8. Architecture Center-style lifecycle

Prompt:

> Design a data science lifecycle using the visual language of the Azure
> Architecture Center MLOps example. Use a source estate, development loop,
> approved release, staging/production and monitoring. Number the main stages.
> Confirm the target platform before choosing services.

Expected:

- Inspects the relevant actual Architecture Center diagram or supplied image.
- Uses blue/cyan section headers, neutral secondary grouping and recognizable
  service icons, with a readable main path and labeled perimeter feedback loops.
- Each step number maps to a workflow description; badges do not cover ports.
- Environment boundaries, process phases and operational responsibilities are
  not silently treated as the same thing.
- Human gates versus automated triggers are stated and supported by the design.
- Does not copy Microsoft/Azure branding or claim official certification.

## 9. Transfer the style to Fabric, not Azure ML functionality

Prompt:

> Use the MLOps image only as a visual reference. Design Fabric-native batch
> data science from ingestion to Power BI, including human-reviewed retraining.
> Show one environment. Do not add Azure ML endpoints or a release pipeline.

Expected:

- Uses the requested lifecycle with Fabric symbols and appropriate stage bands.
- Uses notebooks, experiments, ML model versions, lakehouses and Power BI as
  supported; no invented Fabric feature store, managed online endpoint or
  automatic model-promotion service.
- Separates workspace membership from logical process sections.
- Distinguishes custom quality/drift checks from pipeline run monitoring.
- No extra staging/production environments just to fill the reference layout.

## 10. Networking is not a numbered MLOps workflow

Prompt:

> Draw a hub-spoke network in the Azure Architecture Center style, using these
> explicitly specified connections and resource groups. This is a topology view,
> not a sequence diagram.

Expected:

- Uses nested, labeled boundaries and aligned repeated spokes.
- Does not force inner/outer loops, blue phase headers or numbered stages where
  they add no meaning.
- Distinguishes peering, routing and diagnostics; dashed borders are explained
  rather than assigned a universal meaning.
- Does not infer transitive peering or a security guarantee from appearance.

## 11. Connector and density review

Use a synthetic editable diagram containing an icon inside an oversized invisible
group, a connector crossing a service caption, a feedback line through the main
workflow, an overlapping number badge and excessive canvas margins.

Expected:

- Tightens groups or changes ports so connectors visibly belong to their objects.
- Reroutes the caption collision and feedback loop without changing topology.
- Moves the badge and trims unused margins, keeping labels readable.
- Inspects the corrected final image at full view and enlarged detail.
- Does not use XML growth, artificial node counts or a fixed review-pass quota.

## 12. Output mode and unsupported input

Request a presentation overview, a detailed reference view, and faithful
recreation separately. Also supply compressed/multipage draw.io input to the
checker.

Expected:

- Chosen medium is explicit; readability is assessed at its intended size.
- Presentation does not silently omit required content to fit.
- Recreation does not silently simplify the source to meet a font threshold.
- Unsupported checker input is refused explicitly, not reported as passing.
- Automatic routing warnings remain visible until independently reviewed.

## Repeatable with/without-skill comparison

Use synthetic briefs from scenarios 5, 9 and 10 (scoped revision, Fabric
lifecycle and network topology). Start with a small pilot; expand only after
the method is useful. A [two-case direct-file pilot](benchmarks/README.md) has
been executed with preserved first drafts, measurements and edit tests. It used
parent corrections after agent follow-ups were refused, not measured agent repair
turns. The broader repeated/blinded host-activation protocol below remains unexecuted.

1. Freeze the same technical inputs, graph/ownership contract, output medium,
   asset access, renderer and success criteria for each pair.
2. Record host, model/settings, skill revision, tools, date and cost/time budget.
   Verify skill invocation separately. A direct-file run is a different condition.
3. Use fresh independent contexts. Give the baseline the same task and technical
   evidence, but no skill instructions, starter examples or sibling outputs.
   Do not intentionally weaken its prompt. Record which helpers each condition
   used; this tests the package, not just its prose.
4. Save the first outputs and final outputs separately. Give both the same
   correction opportunity and access to validation feedback.
5. Review blinded labels where feasible. Record required graph omissions/errors,
   material visual defects, readability at target size, correction turns/time
   and a real edit task (rename/move one service without breaking its connectors).
   Review scores are judgments; keep comments/examples behind them.
6. Repeat enough cases to distinguish a useful pattern from one lucky layout.
   Report results per case, variability, unresolved failures and cost; do not
   manufacture scores or infer adoption from repository stars.

Suggested result columns: case, condition, activation evidence, first-pass graph
errors, first-pass visual defects, corrections, elapsed time, final defects,
edit-task outcome, reviewer notes. Do not score XML size, node count or decorative
complexity as quality. Claim an improvement only when observed results support it.
