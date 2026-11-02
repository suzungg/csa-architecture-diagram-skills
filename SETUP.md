# Setup

Nothing below is run automatically. Review the skill, package manifests and
scripts before installation. Keep output in a separate, approved project.

## Copy a bundled skill

VS Code's [official Agent Skills documentation](https://code.visualstudio.com/docs/agent-customization/agent-skills)
documents project folders such as `.github/skills/` and `.claude/skills/`.
Copy the **whole folder**, including licenses, references and assets.
The following PowerShell example deliberately refuses an existing destination:

```powershell
# Run from this toolkit's root. Replace the target with your own project.
$target = 'C:\path\to\your-project'
$name = 'csa-style-diagrams'
$parent = Join-Path $target '.github\skills'
$destination = Join-Path $parent $name
if (-not (Test-Path -LiteralPath $target -PathType Container)) { throw 'Target project does not exist' }
if (Test-Path -LiteralPath $destination) { throw 'Skill already exists; review before updating' }
New-Item -ItemType Directory -Force -Path $parent | Out-Null
Copy-Item -LiteralPath (Join-Path '.\skills' $name) -Destination $destination -Recurse
```

For Claude Code, use the target project's `.claude\skills` parent instead.
On macOS/Linux use equivalent native paths and copy the entire folder with
your file manager, refusing merges/overwrites. Do not copy `node_modules`,
virtual environments or generated output from an already-used installation.

Start a fresh host session, check skill discovery, and explicitly ask for the
skill by name. Discovery does not guarantee invocation. Test with synthetic
input and inspect actual tool activity. The retained skills may refer to tools
or subagents that another host does not provide.

## Mermaid authoring

Use [mermaid-diagrams](skills/mermaid-diagrams/SKILL.md) to author text-based
flowcharts, sequence diagrams, C4 views, ER diagrams and other supported types.
Retain the Mermaid source for future editing; PNG and SVG are exports.

No Mermaid renderer or Node dependency tree is bundled. Choose an approved local
Mermaid-capable editor or exporter and verify support for the requested syntax
and version. The [three-tier example](examples/three-tier.mmd) provides synthetic
input for a smoke check. Inspect the actual export rather than assuming that a
successful parse guarantees a readable layout. Do not send private material to
online editors without approval.

## Azure Diagrams

Copy the complete [azure-diagrams folder](skills/azure-diagrams) using the
bundled-skill procedure above. It requires Graphviz's `dot` executable on PATH
and Python packages listed in its [core requirements](skills/azure-diagrams/requirements.txt).
After approving installation, choose the Graphviz package for your platform:
`winget install -e --id Graphviz.Graphviz` on Windows,
`brew install graphviz` on macOS, or `sudo apt-get install graphviz` on Debian/Ubuntu.
Reopen the terminal and check `dot -V`.

Use an isolated Python environment. For example, from this toolkit's root on
Windows, after approving dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\skills\azure-diagrams\requirements.txt
```

On macOS/Linux use `python3 -m venv .venv`, then
`.venv/bin/python -m pip install -r skills/azure-diagrams/requirements.txt`.
[Optional extras](skills/azure-diagrams/requirements-extras.txt) support additional
diagram types and SVG processing; review native Cairo requirements before use.
None of these installations or upstream scripts were run for this addition.

Prefer PNG for sharing: ordinary Graphviz SVG output may reference local icon
paths. Neither output is a native draw.io document. The original skill normally
removes throwaway generation scripts; explicitly request a retained generator
if reproducible, code-editable output is needed. Treat IaC analysis as guidance,
not proof that every deployed resource or relationship was discovered.

## Excalidraw: external option

See [EXCALIDRAW.md](EXCALIDRAW.md) for the pinned upstream, unresolved license,
conditional setup and network dependencies. It is not a sixth bundled folder
and cannot be installed by the copy procedure above. Obtain suitable rights
before copying it; no placeholder or modified substitute is included.

## draw.io workflows

Bring an approved local draw.io-compatible editor/exporter. The three bundled
draw.io skills do not ship a renderer or model runtime. CSA does include a
[curated Foundry subset and original terms](skills/csa-style-diagrams/assets/foundry/README.md)
and [Fabric subset with its original Microsoft MIT license](skills/csa-style-diagrams/assets/fabric/README.md),
not a complete Azure/Fabric icon library. Discover the installed renderer's actual commands; no universal export
command is assumed here. Verify separately editable objects and export from the
final source, then view the actual PNG.

CSA additionally includes optional Python 3.10+ standard-library drawing/checking
helpers and a local draw.io Desktop export wrapper. See its
[tooling guide](skills/csa-style-diagrams/references/tooling.md) for executable
selection, non-overwriting commands, checks and limitations. Copying these
scripts does not register a skill or install/launch a renderer.
Copy the whole skill folder, including assets and terms, to retain the offline
Foundry/Fabric lookup. No Azure access or subscription is needed to use these symbols.
Optional [rendered-text checks](skills/csa-style-diagrams/references/quality-checks.md)
also require an explicitly selected local Edge/Chromium executable. They use a
temporary browser profile, not your signed-in profile, and install nothing.
Review the PNG separately; text measurements are not a complete visual audit.

For Aymen's pitch, the original 2-3 research agents and named model must be
available; ask how to proceed if they are not. Iteration needs A5 inspection,
the specified XML measurement and at least four post-pitch review passes.
Use the custom skill for a different workflow instead of silently changing
Aymen's originals.

## Research MCP integrations

Use [MCP.md](MCP.md) for the preserved Microsoft Learn and GitHub host-specific
configuration examples and authentication guidance. Learn provides public
documentation, not Azure resource inventory. GitHub's examples select read-only
access and still require appropriate repository authorization. Neither server is
registered by this setup document.
