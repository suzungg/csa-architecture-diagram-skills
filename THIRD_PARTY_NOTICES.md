# Licensing and provenance

The root [MIT license](LICENSE) applies only to this repository's original
documentation, configuration examples and validation tooling. It **does not
relicense third-party files** or grant rights to externally referenced content.
The user's custom skill has its own unchanged MIT license.

| Bundled material | License and retained notice |
| --- | --- |
| imxv Pretty Mermaid | [MIT](skills/pretty-mermaid/LICENSE) |
| Softaworks Mermaid Diagrams | [MIT](skills/mermaid-diagrams/LICENSE), copied from its upstream root |
| Microsoft Azure Resource Visualizer | [MIT](skills/azure-resource-visualizer/LICENSE), copied from its upstream root |
| Carl Brindle Azure Diagrams | [MIT](skills/azure-diagrams/LICENSE) |
| Aymen drawio-pitch and drawio-iterate | [Pitch MIT](skills/drawio-pitch/LICENSE.txt), [iterate MIT](skills/drawio-iterate/LICENSE.txt) |
| Natural architecture diagrams | [MIT](skills/natural-architecture-diagrams/LICENSE.txt) |
| Six Anthropic skill folders | Each folder's `LICENSE.txt` is Apache-2.0; see [catalog](ANTHROPIC.md) |

The Anthropic [upstream third-party notices](third-party/anthropic/THIRD_PARTY_NOTICES.md)
are retained verbatim for attribution. They cover the wider upstream product;
their presence does **not** mean this toolkit bundles every listed component
(for example, FFmpeg), nor does it change the individual skills' licenses.
Preserve applicable notices when copying skills onward.

All bundled upstream files are unmodified snapshots. The only packaging
additions inside skill folders are inherited MIT licenses for Softaworks and
Microsoft. Pretty Mermaid's repository automation is excluded; its complete
skill runtime, package lockfile, documentation and assets are retained. Aymen's
repository-level samples are not included.

Excalidraw has no explicit license at the reviewed commit, so no source is
redistributed here. Anthropic's `docx`, `pdf`, `pptx` and `xlsx` license files
state service-governed restrictions including prohibitions on reproduction,
derivatives and redistribution. They are **not open source**, not copied into
this repository, and not covered by its MIT license. Use only through official
channels under applicable terms. `doc-coauthoring` lacks a per-skill license
file at the pin; this toolkit conservatively leaves it external.

Dependency packages are not vendored. Installing them introduces their own
licenses and notices. Cloud-service names, logos, bundled promotional images
and brand examples do not imply trademark permission, certification or
endorsement. Obtain suitable asset rights for your own diagrams.

[SOURCES.json](SOURCES.json), [SOURCE-LOCK.json](SOURCE-LOCK.json), and
[ANTHROPIC-CATALOG.json](ANTHROPIC-CATALOG.json) record exact provenance,
file hashes and external status. Do not assume that a later upstream revision
has the same license.
