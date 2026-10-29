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
$name = 'natural-architecture-diagrams'
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
When distributing an Anthropic skill separately, also retain the
[upstream notices](third-party/anthropic/THIRD_PARTY_NOTICES.md).

Start a fresh host session, check skill discovery, and explicitly ask for the
skill by name. Discovery does not guarantee invocation. Test with synthetic
input and inspect actual tool activity. Some Anthropic skills refer to tools,
Claude-specific paths or subagents that another host may not provide.

## Pretty Mermaid

Install a maintained Node.js LTS and npm from an approved source. The upstream
manifest declares Node >=16; that is a minimum, not a recommendation to use an
end-of-life release. From this repository root, in PowerShell:

```powershell
New-Item -ItemType Directory -Force .\output | Out-Null
Push-Location .\skills\pretty-mermaid
try {
    npm ci
    if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed; do not invoke the renderer' }
    node .\scripts\render.mjs --input ..\..\examples\three-tier.mmd --output ..\..\output\three-tier.svg --theme github-light
    if ($LASTEXITCODE -ne 0) { throw 'Rendering failed' }
} finally {
    Pop-Location
}
```

Change `--output` to a `.png` path and add `--format png` for PNG.
For plain terminal output use `--format ascii --use-ascii --color-mode none`.
These flags are taken from the pinned renderer; generated output still needs
inspection. For macOS/Linux use `/` separators and `cd`/`mkdir` equivalents.

Run `npm test` and `npm run validate` from the skill directory after an approved
dependency install when changing this renderer. The CLI supports flowchart,
sequence, state, class, ER and XY diagrams, not every Mermaid feature described
by the broader Softaworks authoring skill. Use a separately approved Mermaid
renderer for unsupported syntax; do not silently simplify the diagram.

The bundled CLI's missing-dependency path runs `npm install` automatically.
Even a "local" renderer therefore may initiate a network install. Install
dependencies deliberately, inspect the lockfile and keep network restrictions
in place when appropriate. Native PNG support varies by OS/architecture.

## Azure Diagrams: Python + Graphviz

See the pinned [upstream setup guide](https://github.com/cmb211087/azure-diagrams-skill/blob/d7513005f62ad8042c36987cd7da515a114701d1/SETUP.md)
for platform-specific troubleshooting. This root page also supplies the
`../../SETUP.md` target used by the unchanged bundled skill README.

Graphviz is a **system package**, not just a Python module. Reviewed upstream
commands (execute only the one for your OS, with installation approval):

| Platform | Graphviz installation |
| --- | --- |
| Windows | `winget install -e --id Graphviz.Graphviz` |
| macOS | `brew install graphviz` |
| Debian/Ubuntu | `sudo apt-get install graphviz` |

Restart the terminal and check `dot -V`. On Windows, ensure Graphviz's `bin`
directory is on PATH; do not replace PATH wholesale. Then from the toolkit root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\skills\azure-diagrams\requirements.txt
.\.venv\Scripts\python.exe .\skills\azure-diagrams\scripts\verify_installation.py
```

On macOS/Linux use `python3 -m venv .venv` and `.venv/bin/python`.
Optional extras are in
[requirements-extras.txt](skills/azure-diagrams/requirements-extras.txt);
CairoSVG can need native Cairo libraries, especially on Windows.
Python requirement ranges are upstream's, not a fully locked Python environment.

Run the upstream generator from its skill directory, following
[SKILL.md](skills/azure-diagrams/SKILL.md). Prefer PNG for portable sharing;
Graphviz SVG may reference local icon files. Inspect or embed required assets
before claiming a portable SVG. Request retained Python source explicitly if
you need diagram-as-code editing after generation.

## draw.io workflows

Bring an approved local draw.io-compatible editor/exporter. The three bundled
draw.io instruction skills do not ship a renderer, service icon pack or model
runtime. Discover the installed renderer's actual commands; no universal export
command is assumed here. Verify separately editable objects and export from the
final source, then view the actual PNG.

For Aymen's pitch, the original 2-3 research agents and named model must be
available; ask how to proceed if they are not. Iteration needs A5 inspection,
the specified XML measurement and at least four post-pitch review passes.
Use the custom skill for a different workflow instead of silently changing
Aymen's originals.

## Azure inventory

Azure Resource Visualizer needs separately authorized Azure CLI or Azure MCP
access. Microsoft Learn MCP provides public documentation, **not** resource
inventory. Scope Azure permissions to the resources being inspected and do not
grant access to secret values for a diagram. This toolkit does not configure
Azure authentication or deploy anything.

## Excalidraw: external, permission-gated

The [pinned upstream README](https://github.com/coleam00/excalidraw-diagram-skill/blob/8646fcc9f74f38539c6cdb4c969723336a96ddcd/README.md)
documents cloning the repository, copying it to
`.claude/skills/excalidraw-diagram`, then running `uv sync` and
`uv run playwright install chromium` from its `references` folder.
Those are the upstream instructions, **not a redistribution grant**.
No explicit license was found in that revision's complete tree or README.
Obtain suitable rights before copying or distributing it, then follow upstream
installation in a separate approved location and pin the reviewed commit.
Do not copy only `SKILL.md`: rendering also uses Python, HTML and reference files.
Review browser resource/network access before processing private diagrams.

## Anthropic and MCP

Use [ANTHROPIC.md](ANTHROPIC.md) for official marketplace/service installation
and the full catalog. Use [MCP.md](MCP.md) for host-specific configuration and
authentication. Neither is registered by this setup document.
