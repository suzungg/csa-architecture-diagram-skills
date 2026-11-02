# Excalidraw diagram skill: external option

The requested [coleam00 Excalidraw diagram skill](https://github.com/coleam00/excalidraw-diagram-skill)
is cataloged here, **not bundled or installed**.

Reviewed revision:
[`8646fcc9f74f38539c6cdb4c969723336a96ddcd`](https://github.com/coleam00/excalidraw-diagram-skill/tree/8646fcc9f74f38539c6cdb4c969723336a96ddcd),
checked 2026-11-02. Its complete tree, README and skill entrypoint contain no
explicit license grant. A public repository is not permission to redistribute
its contents. The Excalidraw application's license does not apply automatically
to this independently authored skill.

**Obtain suitable permission or an explicit upstream license before copying,
installing or redistributing it.** If permission is obtained, review its scope
and notices, then update the source manifest and packaging deliberately. There
is no placeholder `SKILL.md` claiming that this option is installed.

## What the upstream option provides

It authors native `.excalidraw` JSON for editable diagrams, with layout guidance,
element templates, a color palette and a local PNG render/review workflow.
The PNG is a preview, not the editable source. It is an alternative visual
language to CSA's Microsoft Architecture Center-inspired diagrams.

## Setup reference, conditional on permission

The pinned [upstream README](https://github.com/coleam00/excalidraw-diagram-skill/blob/8646fcc9f74f38539c6cdb4c969723336a96ddcd/README.md)
documents placing the complete folder in a compatible host's
`.claude/skills/excalidraw-diagram` directory. Host discovery must be verified
separately; do not assume every agent scans that location.

Its [dependency manifest](https://github.com/coleam00/excalidraw-diagram-skill/blob/8646fcc9f74f38539c6cdb4c969723336a96ddcd/references/pyproject.toml)
requires Python 3.11+ and Playwright 1.40+. The documented renderer setup, from
the skill's `references` directory after reviewing and approving dependencies,
is `uv sync`, then `uv run playwright install chromium`. These commands work
with uv on Windows, macOS and Linux; browser/system prerequisites vary.
They have **not** been executed as part of this repository addition.

The [render template](https://github.com/coleam00/excalidraw-diagram-skill/blob/8646fcc9f74f38539c6cdb4c969723336a96ddcd/references/render_template.html)
imports Excalidraw code from `https://esm.sh/`. Thus its local browser rendering
is not an offline-only workflow. Review network access and third-party code
loading before using private diagrams. Local rendering also does not imply
local model inference.

Until redistribution rights are resolved, use the bundled CSA, Azure Diagrams,
Aymen or Mermaid options without copying this skill into the toolkit.
