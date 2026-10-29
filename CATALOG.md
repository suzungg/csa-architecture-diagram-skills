# Diagram skill catalog

Snapshot review: **2026-10-29**. These are source descriptions, not adoption
metrics or claims of successful execution. The
[machine-readable manifest](SOURCES.json) contains full commits and mappings;
[SOURCE-LOCK.json](SOURCE-LOCK.json) covers every bundled file.

| Component | Pinned upstream | Local status | License |
| --- | --- | --- | --- |
| Excalidraw Diagram | [coleam00/excalidraw-diagram-skill @ 8646fcc](https://github.com/coleam00/excalidraw-diagram-skill/tree/8646fcc9f74f38539c6cdb4c969723336a96ddcd) | External; [permission-gated setup](SETUP.md#excalidraw-external-permission-gated) | No explicit license found |
| Pretty Mermaid | [imxv/Pretty-mermaid-skills @ e234ab7](https://github.com/imxv/Pretty-mermaid-skills/tree/e234ab73c2992f03c36db04fd55ebb90abca9c45) | [Complete root skill](skills/pretty-mermaid); upstream `.github` automation excluded | MIT |
| Mermaid Diagrams | [softaworks/agent-toolkit @ 3027f20](https://github.com/softaworks/agent-toolkit/tree/3027f20f3181758385a1bb8c022d4041dfb4de84/skills/mermaid-diagrams) | [Complete selected folder](skills/mermaid-diagrams) + inherited root license | MIT |
| Azure Resource Visualizer | [microsoft/azure-skills @ e484244](https://github.com/microsoft/azure-skills/tree/e484244aad82d80bd640d44b2bea92b03bddf559/skills/azure-resource-visualizer) | [Complete selected folder](skills/azure-resource-visualizer) + inherited root license | MIT |
| Azure Diagrams | [cmb211087/azure-diagrams-skill @ d751300](https://github.com/cmb211087/azure-diagrams-skill/tree/d7513005f62ad8042c36987cd7da515a114701d1/skills/azure-diagrams) | [Complete selected folder](skills/azure-diagrams), including dependency manifests and scripts | MIT |
| Draw.io Pitch | [aymenfurter/skills @ 071fa88](https://github.com/aymenfurter/skills/tree/071fa8835d0ffe0bb72a54573a465672fc7ba8cc/skills/drawio-pitch) | [Original skill and license](skills/drawio-pitch) | MIT |
| Draw.io Iterate | [aymenfurter/skills @ 071fa88](https://github.com/aymenfurter/skills/tree/071fa8835d0ffe0bb72a54573a465672fc7ba8cc/skills/drawio-iterate) | [Original skill and license](skills/drawio-iterate) | MIT |
| Natural Architecture Diagrams | User-authored pack supplied 2026-10-29; content hashes in lockfile | [All four original files](skills/natural-architecture-diagrams) | MIT |
| Anthropic official collection | [anthropics/skills @ ca45fc4](https://github.com/anthropics/skills/tree/ca45fc496a3436251f191354091d557da31c15b5) | Six bundled, 13 external; [full catalog and official setup](ANTHROPIC.md) | Mixed; per-skill terms |

## Packaging choices

The diagram selection is deliberately not a mirror of all Azure or Softaworks
skills. Runtime resources stay with their selected skill. No `node_modules`,
virtual environments, cloud credentials, personal paths or customer diagrams
are packaged. Small upstream theme previews and renderer examples remain where
referenced; large repository-level sample collections are not copied.

Aymen's only files in each selected folder are the original `SKILL.md` and
`LICENSE.txt`, so those folders are complete, not missing a renderer. The
custom skill's four-file pack is likewise an instruction package, not a
rendering application.

Excalidraw is represented here by provenance and upstream installation
instructions, **not source code**. Public visibility and a clone command do
not establish redistribution permission.

## Runtime compatibility is separate from packaging

Mermaid authoring and Pretty Mermaid rendering are complementary, but Pretty
Mermaid does not implement every Mermaid diagram type. Azure Resource
Visualizer needs live read access; the other diagram skills can work from
synthetic briefs without access to Azure. GitHub MCP and Learn MCP provide
research context, not diagram editors.

For prerequisites, editable formats, privacy boundaries and Aymen's potentially
costly workflow requirements, start with the [README](README.md).
