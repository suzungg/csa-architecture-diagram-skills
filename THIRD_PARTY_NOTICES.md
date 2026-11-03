# Licensing and provenance

The root [MIT license](LICENSE) applies only to this repository's original
documentation, configuration examples and validation tooling. It **does not
relicense third-party files** or grant rights to externally referenced content.
The user's custom code/text/layouts have their own unchanged MIT license;
embedded or separately bundled Microsoft artwork is excluded from that grant.

| Bundled material | License and retained notice |
| --- | --- |
| Softaworks Mermaid Diagrams | [MIT](skills/mermaid-diagrams/LICENSE), copied from its upstream root |
| Carl Brindle Azure Diagrams | [Original MIT license](skills/azure-diagrams/LICENSE), retained with all 32 selected skill files |
| Aymen drawio-pitch and drawio-iterate | [Pitch MIT](skills/drawio-pitch/LICENSE.txt), [iterate MIT](skills/drawio-iterate/LICENSE.txt) |
| CSA-style diagrams original code/text/layouts | [MIT](skills/csa-style-diagrams/LICENSE.txt); original copyright notice retained |
| Microsoft Foundry/core companion icons and terms | [Original Microsoft terms](skills/csa-style-diagrams/assets/foundry/Microsoft_Terms_of_Use.pdf); copied unchanged from official Azure icons V24 |
| Microsoft Fabric item icons | [Original Microsoft MIT license](skills/csa-style-diagrams/assets/fabric/LICENSE), copied unchanged from the official v6.1.0 archive |

All bundled upstream files are unmodified snapshots. The only packaging
addition inside a third-party skill folder is the inherited MIT license for
Softaworks. Aymen's repository-level samples are not included. Preserve applicable
notices and licenses when copying skills onward.

The separately authored [Excalidraw diagram skill](EXCALIDRAW.md) is linked only.
No explicit license was found at the pinned revision, so its files are not
redistributed. Excalidraw application's license does not license this skill.
Do not add its source until suitable rights and notices have been reviewed.

For the Azure/Foundry subset, Microsoft permits copying, distribution and display only in
architecture diagrams, training materials or documentation, unless explicit
permission grants another use. All other rights are reserved. Do not crop,
flip, rotate, distort or use them to represent your own product. This applies
also to icons embedded in the Foundry examples and benchmark source/previews;
the original layout/generator does not relicense that artwork.
See [asset provenance and lookup keys](skills/csa-style-diagrams/assets/foundry/README.md)
and the [official usage page](https://learn.microsoft.com/en-us/azure/architecture/icons/).

The Fabric archive has a **different license**: MIT, copyright 2025 Microsoft
Corporation. Preserve its notice, including when distributing embedded icons.
The [official Fabric usage guidance](https://learn.microsoft.com/en-us/fabric/fundamentals/icons)
also asks that appearance/proportions be retained and product icons not represent
your own service. See the [Fabric asset catalog](skills/csa-style-diagrams/assets/fabric/README.md).
Neither license transfers Microsoft's trademarks or implies endorsement.

Skill runtime dependency packages are not vendored. Installing them introduces their own
licenses and notices. Cloud-service names and logos do not imply trademark
permission, certification or
endorsement. Obtain suitable asset rights for your own diagrams.

[SOURCES.json](SOURCES.json) and [SOURCE-LOCK.json](SOURCE-LOCK.json) record exact
provenance and file hashes. Do not assume that a later upstream revision
has the same license.
For archive assets, `git_blob` is a digest computed from the selected file bytes,
not evidence of an upstream Git commit; archive version/SHA-256 and exact member
paths provide the acquisition pin.

## Presentation archive

The [presentation ZIP](presentations/architecture-diagrams.zip) contains local
Reveal.js 6.0.2 assets under MIT (`vendor/reveal/LICENSE`) and Mona Sans v2.0.27
under SIL OFL (`assets/fonts/OFL.txt`). Paths here are relative to the extracted
`architecture-diagrams-brand-deck` folder. Microsoft Fabric artwork and CSA
layout/code notices are retained at `assets/LICENSE-Fabric` and
`sources/LICENSE-CSA.txt`; additional notices accompany the nested diagram-source
ZIP. The presentation's README and provenance manifest describe its sources.

The user-supplied Cowork screenshot is included as part of this requested
presentation; no separate redistribution license is asserted. The repository's
MIT license does not relicense that screenshot or third-party assets. The deck
is independent and does not imply GitHub, Microsoft or Anthropic endorsement.
