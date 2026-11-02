# CSA architecture diagram skills

A private, curated toolkit for editable architecture diagrams, diagram-as-code,
and supporting research. **Four complete architecture skill folders are bundled**:
`mermaid-diagrams`, Aymen's original `drawio-pitch` and `drawio-iterate`,
and `csa-style-diagrams`. No skills or MCP servers are installed on
your machine by cloning this repository.

These support three approaches: Mermaid authoring, Aymen's combined pitch-and-
refinement workflow, and Azure Architecture Center-inspired CSA-style diagrams. Microsoft
Learn MCP and GitHub MCP remain available as opt-in research integrations. See
[the catalog](CATALOG.md) and [license boundaries](THIRD_PARTY_NOTICES.md).

## Quick start

Clone with an account that can access this private repository:

```powershell
git clone https://github.com/suzungg/csa-architecture-diagram-skills.git
Set-Location csa-architecture-diagram-skills
python .\tools\validate.py
```

Python 3.10+ is needed for this toolkit's structural checks and CSA's optional
drawing/checking/export helpers.
You can read and copy instruction-only skills without Python.

1. Choose one skill below and review its full folder, not just `SKILL.md`.
2. Follow [SETUP.md](SETUP.md) to copy that folder into your target project's
   supported skill location. `skills/` here is a distribution directory, not
   an automatically registered host location. Avoid duplicate skill names.
3. Add only the renderers you need. For technical research, review and merge
   one of the opt-in [MCP examples](MCP.md); do not copy it over an existing
   configuration.
4. Start a fresh agent session and explicitly name the skill. Check that the
   host actually loads it, then inspect the editable output and matching export.

Start with this synthetic request:

> Use csa-style-diagrams to design a three-tier architecture from my brief in
> the visual style of Azure Architecture Center. Use official service icons,
> clear section hierarchy, typed boundaries and meaningful connections, not a
> dashboard. Deliver editable draw.io source and a matching
> locally rendered PNG. Distinguish assumptions from verified product claims.

## Which skill should I use?

| Task | Skill | Editable source and outputs |
| --- | --- | --- |
| Architecture Center-inspired diagrams; faithful recreation or scoped revisions | [csa-style-diagrams](skills/csa-style-diagrams/SKILL.md) | Object-editable `.drawio`, matching PNG; optional SVG |
| Research-led, dense initial visual pitch on one A5 sheet | [drawio-pitch](skills/drawio-pitch/SKILL.md), Aymen original | `.drawio` + PNG + source/asset credits |
| Aymen's prescribed publication-refinement cycle | [drawio-iterate](skills/drawio-iterate/SKILL.md), Aymen original | Separate `.drawio`/PNG pair per pass |
| Mermaid authoring: sequence, C4, ER, flow and other software diagrams | [mermaid-diagrams](skills/mermaid-diagrams/SKILL.md), Softaworks | Text-editable Mermaid; export depends on renderer |

Retain Mermaid/draw.io source when future editing matters. PNG is not object
editable; SVG is not automatically equivalent to a native diagram document.
Embedded raster icons in draw.io
remain raster even when their surrounding objects and labels are editable.

### Aymen originals versus the custom skill

The Aymen files are **unchanged**, including 2-3 GPT-6 Astra research agents for
`drawio-pitch`, one A5 sheet, and `drawio-iterate`'s at least **9x meaningful XML
size** and **four post-pitch PNG review passes**. These requirements can consume
substantial credits and time, require a capable agent host, and may conflict
with a sparse technical-diagram goal. A larger XML file is not proof of a better
architecture. If the model, agents or renderer are unavailable, report the
limitation rather than silently substituting a different workflow.

The custom `csa-style-diagrams` skill has **no fixed model, agent
count, pass count or growth quota**. Its defaults now include purposeful
section bands, prominent service icons, meaningful workflow numbering and
perimeter feedback loops. It selects a reference style appropriate to the
workload, not a mandatory MLOps topology. Choose it for defect-driven refinement.
It now includes [reusable local helpers and quality checks](skills/csa-style-diagrams/references/tooling.md),
explicit presentation/reference/recreation modes, and an
[annotated editable Fabric example](skills/csa-style-diagrams/examples/fabric-batch/README.md).
The Fabric example uses disclosed neutral symbols. For Foundry, CSA also bundles
[13 official core/companion icons](skills/csa-style-diagrams/assets/foundry/README.md),
a local lookup, an editable icon sheet and
[Foundry-specific guidance](skills/csa-style-diagrams/references/foundry.md).
These icons retain Microsoft's permitted-use terms, separate from the MIT skill.
CSA now also includes a [complete multi-project Foundry example](skills/csa-style-diagrams/examples/foundry-multi-project/README.md),
[eight official Fabric icons](skills/csa-style-diagrams/assets/fabric/README.md)
under Microsoft's archive MIT license, and an
[official-icon Fabric example](skills/csa-style-diagrams/examples/fabric-official/README.md).
[Deeper optional checks](skills/csa-style-diagrams/references/quality-checks.md)
measure rendered SVG text and declared scope/relationship consistency.
The [executed CSA/no-skill pilot](skills/csa-style-diagrams/benchmarks/README.md)
preserves first drafts, findings and edit failures; it does not establish a general winner.

## Prerequisites and platforms

| Component | Requirements / limits |
| --- | --- |
| Instruction-only skills | A skill-capable agent host; tools and model access vary by host |
| CSA local helpers | Python 3.10+ standard library; optional local draw.io Desktop for PNG export and Edge/Chromium for rendered-text checks; no automatic installation |
| draw.io workflows | A locally approved editor/exporter plus actual image inspection; no renderer bundled; CSA includes curated Foundry and Fabric icons |
| Mermaid authoring | A Mermaid-capable viewer/editor or separately approved renderer supporting the requested syntax; no renderer bundled |
| Remote MCP examples | Compatible HTTP MCP client; no Docker or Node needed for these two hosted endpoints; GitHub authentication required |

Windows PowerShell, macOS and Linux setup notes are in [SETUP.md](SETUP.md).
Vendor examples may use POSIX shell syntax. Adapt command syntax to your platform
and verify the chosen host and renderer independently.

## MCP, safety and privacy

[MCP.md](MCP.md) explains the public **Microsoft Learn** endpoint and authenticated
**GitHub** endpoint. Opt-in examples select GitHub's real `/readonly` endpoint
and limit toolsets; they do not contain credentials. VS Code `servers` and
portable Copilot `mcpServers` examples are separate, with different secret syntax.

**Local rendering does not mean local model inference.** Prompts, attachments,
repository data and tool results may be sent to the configured model provider.
Never send customer diagrams, credentials or private identifiers to public
search, online renderers or external services without approval. Upstream skills
are preserved, not a security sandbox: some suggest online editors, fetch
resources, install packages, call models or launch agents. Review suggested
commands and prepare dependencies explicitly in a restricted environment.

Use synthetic briefs for evaluation, least-privilege accounts for research, and
human review for tool calls. Read-only GitHub tools can still disclose private
data to the model; they do not constrain the agent's shell or other MCP servers.
Product logos have separate usage rules. Appearance is not evidence of
architectural correctness, runtime support or vendor endorsement.

## Maintenance and verification

[SOURCES.json](SOURCES.json) pins repositories, licenses and selections.
[SOURCE-LOCK.json](SOURCE-LOCK.json) records every bundled file's
SHA-256, upstream Git blob, size and provenance; the current custom pack is
also hashed. Only the four selected architecture skills are distributed.

Run `python .\tools\validate.py` and
`python -m unittest discover -s tools -p "test_*.py"` after changes.
See [maintenance instructions](MAINTENANCE.md) before updating snapshots or
licenses. Bundled vendor files are byte-preserved; adaptations should be
explicitly attributed and reviewed rather than silently folded into originals.

**Verification scope:** source provenance, folder completeness, required
references, JSON/config shapes, local Markdown links, Python syntax and
credential-pattern checks. These checks do not execute skills, install
dependencies, render diagrams, authenticate MCP servers or deploy resources.
No end-to-end host/model/renderer compatibility is claimed.
CSA's helper tests, locally rendered examples and limited direct-file pilot are
separate from these repository checks; see the skill's tooling guide and pilot
report for coverage and limitations.
