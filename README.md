# CSA architecture diagram skills

A private, curated toolkit for editable architecture diagrams, diagram-as-code,
and supporting research. **13 complete skill folders are bundled**: seven
diagram skills (including Aymen's two originals and `natural-architecture-diagrams`)
and six official Anthropic skills. No skills or MCP servers are installed on
your machine by cloning this repository.

**Not everything is vendored.** Excalidraw is external because its pinned source
has no explicit license. Anthropic's full 19-skill catalog is included, but its
restricted document skills and seven other skills remain external. See
[the catalog](CATALOG.md), [Anthropic setup](ANTHROPIC.md), and
[license boundaries](THIRD_PARTY_NOTICES.md).

## Quick start

Clone with an account that can access this private repository:

```powershell
git clone https://github.com/suzungg/csa-architecture-diagram-skills.git
Set-Location csa-architecture-diagram-skills
python .\tools\validate.py
```

Python 3.10+ is needed only for this structural check and Python-based tools.
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

> Use natural-architecture-diagrams to design a conventional three-tier
> architecture from my brief. Use thin boundaries, short labels and meaningful
> connections, not a dashboard. Deliver editable draw.io source and a matching
> locally rendered PNG. Distinguish assumptions from verified product claims.

## Which skill should I use?

| Task | Skill | Editable source and outputs |
| --- | --- | --- |
| Conventional architect-style diagrams; faithful recreation or scoped revisions | [natural-architecture-diagrams](skills/natural-architecture-diagrams/SKILL.md) | Object-editable `.drawio`, matching PNG; optional SVG |
| Research-led, dense initial visual pitch on one A5 sheet | [drawio-pitch](skills/drawio-pitch/SKILL.md), Aymen original | `.drawio` + PNG + source/asset credits |
| Aymen's prescribed publication-refinement cycle | [drawio-iterate](skills/drawio-iterate/SKILL.md), Aymen original | Separate `.drawio`/PNG pair per pass |
| Mermaid authoring: sequence, C4, ER, flow and other software diagrams | [mermaid-diagrams](skills/mermaid-diagrams/SKILL.md), Softaworks | Text-editable Mermaid; export depends on renderer |
| Themed Mermaid rendering for docs and terminals | [pretty-mermaid](skills/pretty-mermaid/SKILL.md), imxv | `.mmd` + SVG, PNG or ASCII/Unicode; supports a subset of Mermaid |
| Inventory an existing Azure resource group | [azure-resource-visualizer](skills/azure-resource-visualizer/SKILL.md), Microsoft | Markdown + Mermaid; requires authorized Azure read access |
| Azure icon diagrams and diagrams generated from IaC | [azure-diagrams](skills/azure-diagrams/SKILL.md), Carl Brindle | Python/IaC input + PNG; optional SVG; not native draw.io objects |
| Excalidraw visual explanations | [Excalidraw upstream](https://github.com/coleam00/excalidraw-diagram-skill/tree/8646fcc9f74f38539c6cdb4c969723336a96ddcd), external | Editable `.excalidraw` JSON + PNG; rights and renderer setup required |
| Skill authoring, MCP development, themes and communication | [Anthropic collection](ANTHROPIC.md) | Six bundled supporting skills; full official catalog and install routes |

Retain Mermaid/Python source when future editing matters. PNG is not object
editable; SVG is not automatically equivalent to a native diagram document.
The upstream Azure Diagrams skill discards throwaway Python scripts by default:
explicitly request retained source if needed. Embedded raster icons in draw.io
remain raster even when their surrounding objects and labels are editable.

### Aymen originals versus the custom skill

The Aymen files are **unchanged**, including 2-3 GPT-6 Astra research agents for
`drawio-pitch`, one A5 sheet, and `drawio-iterate`'s at least **9x meaningful XML
size** and **four post-pitch PNG review passes**. These requirements can consume
substantial credits and time, require a capable agent host, and may conflict
with a sparse technical-diagram goal. A larger XML file is not proof of a better
architecture. If the model, agents or renderer are unavailable, report the
limitation rather than silently substituting a different workflow.

The custom `natural-architecture-diagrams` skill has **no fixed model, agent
count, pass count or growth quota**. Choose it for defect-driven refinement.

## Prerequisites and platforms

| Component | Requirements / limits |
| --- | --- |
| Instruction-only skills | A skill-capable agent host; tools and model access vary by host |
| draw.io workflows | A locally approved draw.io-compatible editor/exporter plus actual image inspection; no renderer or icon library bundled |
| Pretty Mermaid | Node.js and npm; upstream declares Node >=16, use a maintained Node LTS; bundled dependency lockfile; native PNG package must support your platform |
| Azure Diagrams | Python + `diagrams>=0.25.1`, system Graphviz (`dot` on PATH); optional matplotlib/CairoSVG and native libraries |
| Azure inventory | Separately configured Azure CLI or Azure MCP and suitable read permissions; Learn MCP does **not** read subscriptions |
| Excalidraw (external) | Upstream Python/uv + Playwright/Chromium renderer; review rights, browser dependencies and network behavior before setup |
| Anthropic helpers | Some are instructions only; MCP evaluations use Python packages and Anthropic API access; skill-creator optimization requires Claude CLI and may incur costs |
| Remote MCP examples | Compatible HTTP MCP client; no Docker or Node needed for these two hosted endpoints; GitHub authentication required |

Windows PowerShell, macOS and Linux setup notes are in [SETUP.md](SETUP.md).
Vendor examples may use POSIX shell syntax. The original skill-creator evaluation
helpers use POSIX-style pipe polling and are **not certified for native Windows**;
use a supported environment such as WSL and verify your chosen workflow.

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
resources, install packages, call models or launch agents. Pretty Mermaid can
automatically run `npm install` when dependencies are missing. Review scripts
and prepare dependencies explicitly before using it in a restricted environment.

Use synthetic briefs for evaluation, least-privilege accounts for inventory, and
human review for tool calls. Read-only GitHub tools can still disclose private
data to the model; they do not constrain the agent's shell or other MCP servers.
Product logos have separate usage rules. Appearance is not evidence of
architectural correctness, runtime support or vendor endorsement.

## Maintenance and verification

[SOURCES.json](SOURCES.json) pins repositories, licenses, selections and
omissions. [SOURCE-LOCK.json](SOURCE-LOCK.json) records every bundled file's
SHA-256, upstream Git blob, size and provenance; the original custom pack is
also hashed. [ANTHROPIC-CATALOG.json](ANTHROPIC-CATALOG.json) covers all 19
official skills at the reviewed revision.

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
