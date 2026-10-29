# Natural architecture diagrams

A standalone skill for conventional, architect-style diagrams: recognizable
service symbols, thin technical boundaries, restrained labels and meaningful
connections. It avoids the dashboard/infographic look unless requested.

The visual target is the style of the Agent Landing Zones example, not a fixed
template or a rule that every architecture must look identical.

## Install

Copy this directory into your supported agent host's skill location. For
repository-local GitHub Copilot skills, use:

```text
.github\skills\natural-architecture-diagrams\SKILL.md
```

Keep `LICENSE.txt` and `examples.md` with it. Confirm your host supports skills
and refresh its skill discovery if needed. This package has not been installed
or exercised through your host's skill loader.

## Use

> Use natural-architecture-diagrams to recreate this reference as an editable
> draw.io diagram. Match its layout and visual language. Preserve its labels;
> flag ambiguities separately instead of silently redesigning it.

Or:

> Use natural-architecture-diagrams to design an Azure agent landing-zone
> diagram from this brief. Use a white canvas, official service icons where
> available, thin boundaries and short labels. Ask about material missing
> requirements before inventing network connections.

## Why this is different

| Common unwanted output | This skill's direction |
| --- | --- |
| Every component becomes a rounded card | Service icons with small direct labels |
| Decorative dashboard grid | Layout reflects topology and ownership |
| Huge banners and excessive color | Modest titles, white canvas, restrained styling |
| Invented arrows | Explicit relationship semantics |
| A screenshot inside a draw.io file | Separate editable objects and connectors |
| Raster icons described as fully vector-editable | Honest asset/editability disclosure |
| Artificial iterations or XML growth | Defect-driven checks |

## Scope and limits

This is an instruction skill, not a renderer or automated architecture validator.
It does not include Microsoft icons or redistribute the supplied screenshot.
Official/native symbols depend on the available libraries and usage rights.
Local drawing/export tools and image inspection are needed for a verified preview.

The skill does not mandate a model or subagents, does not depend on the earlier
draw.io skills, and does not authorize cloud deployment or public publication.

See `examples.md` for trial prompts and expected behavior. These scenarios
are provided for testing; they have not been run as end-to-end skill executions.
