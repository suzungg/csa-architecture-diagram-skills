# Diagram skill catalog

Upstream snapshot review: **2026-10-29**. Selection narrowed to four architecture
skills with user approval on **2026-11-02**. These are source descriptions, not adoption
metrics or claims of successful execution. The
[machine-readable manifest](SOURCES.json) contains full commits and mappings;
[SOURCE-LOCK.json](SOURCE-LOCK.json) covers every bundled file.

| Component | Pinned upstream | Local status | License |
| --- | --- | --- | --- |
| Mermaid Diagrams | [softaworks/agent-toolkit @ 3027f20](https://github.com/softaworks/agent-toolkit/tree/3027f20f3181758385a1bb8c022d4041dfb4de84/skills/mermaid-diagrams) | [Complete selected folder](skills/mermaid-diagrams) + inherited root license | MIT |
| Draw.io Pitch | [aymenfurter/skills @ 071fa88](https://github.com/aymenfurter/skills/tree/071fa8835d0ffe0bb72a54573a465672fc7ba8cc/skills/drawio-pitch) | [Original skill and license](skills/drawio-pitch) | MIT |
| Draw.io Iterate | [aymenfurter/skills @ 071fa88](https://github.com/aymenfurter/skills/tree/071fa8835d0ffe0bb72a54573a465672fc7ba8cc/skills/drawio-iterate) | [Original skill and license](skills/drawio-iterate) | MIT |
| CSA-style diagrams | User-authored pack supplied 2026-10-29; revised on 2026-11-02 with drawing/checking/export helpers, Fabric example and Foundry support; current hashes in lockfile | [Complete skill and local tooling](skills/csa-style-diagrams) | MIT for original work; separate Microsoft terms for artwork |
| Foundry icon assets (part of CSA, not a fifth skill) | Official Azure icon archive V24, SHA-256 and exact member mappings in manifest | [13 unchanged SVGs and original terms](skills/csa-style-diagrams/assets/foundry/README.md) | Microsoft permitted-use icon terms, not MIT |
| Fabric icon assets (also part of CSA) | Official Fabric samples archive, pinned commit `564ec4139742b838468fcf8aa44dac4afe02ce92`, package v6.1.0 | [Eight unchanged SVGs and original license](skills/csa-style-diagrams/assets/fabric/README.md) | Microsoft's archive MIT license; official icon usage guidance |

## Packaging choices

The diagram selection is deliberately not a mirror of upstream collections.
References stay with their selected skill. No `node_modules`,
virtual environments, cloud credentials, personal paths or customer diagrams
are packaged. Renderers and complete vendor icon libraries are not bundled;
only the reviewed Foundry/companion and Fabric subsets are included.

Aymen's only files in each selected folder are the original `SKILL.md` and
`LICENSE.txt`, so those folders are complete, not missing a renderer. The
custom skill now includes standard-library Python drawing/checking helpers,
a wrapper for an explicitly selected local renderer, regression tests and an
original editable/rendered Fabric example with disclosed neutral native symbols.
Its Foundry addition supplies a portable icon lookup, resource/project guidance
and an editable reference sheet; this is not a mandatory deployment template.
The quality revision adds full Foundry and official-icon Fabric examples,
optional local-browser text measurements, declared scope/intent checks and an
[executed limited comparison](skills/csa-style-diagrams/benchmarks/README.md).
The pilot preserves negative results and does not prove general superiority.

## Runtime compatibility is separate from packaging

Mermaid authoring supports several diagram types; the chosen renderer must support
the requested syntax. All four skills can work from synthetic briefs without
access to an Azure tenant. GitHub MCP and Learn MCP provide research context,
not diagram editors.

For prerequisites, editable formats, privacy boundaries and Aymen's potentially
costly workflow requirements, start with the [README](README.md).
