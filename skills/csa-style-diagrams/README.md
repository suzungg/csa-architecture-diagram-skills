# CSA-style diagrams

A standalone skill for **Microsoft Azure Architecture Center-inspired**
technical diagrams: recognizable service symbols, structured sections, typed
boundaries, purposeful color, readable workflows and clear feedback loops.
It avoids decorative dashboards without banning useful section bars or numbering.

The default visual target is the appropriate Architecture Center reference, not
one fixed template. A supplied reference takes precedence for faithful recreation.
This is an independent skill, not an official Microsoft standard or endorsement.

## Install

Copy this directory into your supported agent host's skill location. For
repository-local GitHub Copilot skills, use:

```text
.github\skills\csa-style-diagrams\SKILL.md
```

Copy the **whole folder**, including `scripts`, `references`, `tests`, `examples`,
`assets`, `benchmarks` and their licenses. Confirm your host supports skills and refresh its discovery.
The repository's `skills/` distribution directory is not automatically a host
skill location. No installation was performed as part of this upgrade.

### Verify activation separately

Start a fresh session in your chosen host and request this skill by name.
Check the host's discovery/invocation trace for the actual `SKILL.md` path;
an assistant merely saying "I used CSA" is not sufficient evidence. If that
trace is unavailable, report activation as unverified. Reading this repository
file directly is useful but must be described as direct application, not
successful host-loader activation. Use a synthetic two-component brief first.
The benchmark used fresh model contexts with direct file instructions, not
verified host-loader activation.

## Use

> Use csa-style-diagrams to recreate this reference as an editable
> draw.io diagram. Match its layout and visual language. Preserve its labels;
> flag ambiguities separately instead of silently redesigning it.

Or:

> Use csa-style-diagrams to design an end-to-end Fabric data science
> architecture in the visual style of Azure Architecture Center. Use official
> Fabric icons, blue section headers, numbered lifecycle stages and perimeter
> feedback loops. Show batch scoring and Power BI, not Azure ML online endpoints.
> Keep process groups distinct from workspace boundaries.

## Visual reference families

Start at [Browse Azure Architectures](https://learn.microsoft.com/en-us/azure/architecture/browse/).
The following actual diagrams were inspected for this skill revision on
2026-11-02; they demonstrate different compositions, not one universal notation:

| Reference | Visual conventions to borrow |
| --- | --- |
| [MLOps v2](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/machine-learning-operations-v2) | Blue/cyan section bands, green numbered stages, development/deployment loops, nested environments, monitoring alongside and feedback around the perimeter |
| [Baseline App Service](https://learn.microsoft.com/en-us/azure/architecture/web-apps/app-service/architectures/baseline-zone-redundant) | Prominent service symbols, light grouping fills, nested network scope, endpoint/service separation, supporting identity and monitoring groups |
| [Hub-spoke topology](https://learn.microsoft.com/en-us/azure/architecture/networking/architecture/hub-spoke) | Repeated spoke/subnet boundaries, central shared services and differentiated connectivity/diagnostic paths |

Use the reference's appearance without importing its products, automatic
triggers or security assumptions into another platform. For example, an Azure ML
diagram is not evidence that Fabric has the same serving or model-monitoring
capabilities. No reference screenshots are bundled; the curated official icons
below retain their separate Microsoft usage terms.

## Runnable support and complete examples

The skill now includes optional **standard-library Python 3.10+ helpers**:

- Reusable native components, reserved captions, typed boundaries and explicit
  symbol ports in [csa_drawio.py](scripts/csa_drawio.py).
- A [checker](scripts/check_diagram.py) for IDs/references, graph contracts,
  conservative geometry, output-mode font floors and source/preview hashes.
- A [local export wrapper](scripts/render_diagram.py) for an explicitly selected
  draw.io Desktop executable. It never installs or downloads a renderer.
- An [annotated Fabric example](examples/fabric-batch/README.md) with editable
  source, preview, generator and contract. It deliberately uses disclosed neutral
  symbols so the example does not require redistributing a product icon pack.
- [13 official Foundry and companion icons](assets/foundry/README.md), local
  hash-checked `icon_path(...)` lookup, [Foundry guidance](references/foundry.md)
  and an [editable icon reference sheet](examples/foundry-icons/README.md).
- A [complete multi-project Foundry example](examples/foundry-multi-project/README.md)
  separating applications, project-owned agents, shared models, retrieval and telemetry.
- [Eight official Fabric item icons](assets/fabric/README.md) and an
  [official-icon Fabric lifecycle example](examples/fabric-official/README.md).
- Optional [rendered-text, connector-clarity and scope/intent checks](references/quality-checks.md).
- [Regression tests](tests/test_diagrams.py), an executed
  [CSA/no-skill pilot with preserved evidence](benchmarks/README.md), and a
  [broader comparison protocol](examples.md#repeatable-withwithout-skill-comparison).

Start with [tooling commands and limitations](references/tooling.md). Choose
`presentation`, `reference`, or `recreate` independently of design/revision mode.
The [visual guide](references/visual-style.md) carries detailed composition advice.

## Why this is different

| Common unwanted output | This skill's direction |
| --- | --- |
| Every component becomes a rounded card | Prominent service icons; activity boxes only where useful |
| Decorative dashboard grid | Layout reflects topology, responsibilities and workflow |
| Huge banners or overly sparse icon rows | Modest overall title, purposeful section bars and compact readable groups |
| Numbering every object | Number meaningful workflow stages and explain them in notes |
| Feedback cutting through services | Labeled perimeter loops and clear main flow |
| Styling copied as product functionality | Visual alignment without invented platform capabilities |
| Invented arrows | Explicit relationship semantics |
| A screenshot inside a draw.io file | Separate editable objects and connectors |
| Raster icons described as fully vector-editable | Honest asset/editability disclosure |
| Artificial iterations or XML growth | Defect-driven checks |

## Scope and limits

This is an instruction skill with drawing/checking helpers, **not** a bundled
renderer, layout engine or cloud architecture validator. Foundry/Azure assets
retain Microsoft's permitted-use terms, **not MIT**. The Fabric archive instead
includes Microsoft's own MIT license; retain it and follow official icon usage
guidance. No reference screenshots are redistributed. Basic checks use
conservative geometry; the optional local browser check measures actual
SVG text layout, not PNG pixels. Scope/intent checks compare declarations, not
cloud capabilities, RBAC or security. Explicit route waypoints can need rerouting
after a component moves. Errors, warnings and
unsupported input are distinguished; a clean check does not replace image review.

The skill does not mandate a model or subagents, does not depend on the earlier
draw.io skills, and does not authorize cloud deployment or public publication.

The four bundled examples were generated, locally exported and inspected.
The pilot found a real first-draft defect in each condition across its two cases
and a route-edit limitation in one CSA output. It does **not** establish overall
CSA superiority, speed or cost savings. Its author-reviewed single trials and
parent-applied corrections are documented rather than presented as a full benchmark.
