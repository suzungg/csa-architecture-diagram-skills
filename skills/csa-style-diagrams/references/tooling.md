# Local drawing, checking and export

Python 3.10+ and its standard library are sufficient for the helpers and tests.
There is no pip dependency, automatic install, network fetch, model call or cloud
deployment. Rendering additionally needs an explicitly selected, approved local
draw.io Desktop executable. Review scripts and assets before use.

## Reusable primitives

Import `Diagram` from [csa_drawio.py](../scripts/csa_drawio.py) in a local
generator. The [Fabric generator](../examples/fabric-batch/build.py) is a complete
working example rather than a mandatory template.

| Primitive | Responsibility |
| --- | --- |
| `Diagram(title, width, height, mode=...)` | One uncompressed editable page; `reference`, `presentation` or `recreate` |
| `boundary(..., kind=...)` | Typed scope, header and optional stage badge; does not assign workspace membership |
| `component(..., workspace=... OR scope=..., symbol=..., svg=...)` | Exactly one ownership field; stable ID, visible symbol, separate editable title/caption, reserved slots |
| `icon_path("foundry")` / `icon_path("lakehouse", family="fabric")` | Local curated SVG lookup with path, hash and common unsafe-content checks; no fetch or fallback |
| `port(id, side)` | Anchor on the visible symbol, not the oversized caption group |
| `connect(..., kind=..., intent=..., meaning=..., via=...)` | Attached orthogonal centerline; associations are dashed/arrowless; other kinds directed |
| `text(...)` | Explicit annotation rectangle; labels are never invisibly auto-positioned |

Coordinates are canvas units. Component placement is absolute; symbol/title/
caption children use relative offsets within their groups. `workspace` or `scope`
is ownership metadata, not containment; supply exactly one nonempty string.
Existing `workspace=...` calls remain valid. Boundary kinds are `logical`,
`workspace`, `tenant`, `network`, `environment`, `resource`, and `project`;
explain their actual meaning in notes. See [Foundry guidance](foundry.md).

Neutral native symbols are `process`, `cylinder`, `note`, `document`, and
`ellipse`. They are not vendor logos. `svg=Path(...)` embeds an approved local
self-contained SVG without changing its colors. The helper rejects common
active/external SVG constructs; this is not a comprehensive sanitizer or a
substitute for reviewing asset provenance.

For the [13 bundled official symbols](../assets/foundry/README.md), use
`svg=icon_path("foundry-agent-service")`. Unknown aliases and missing or modified
assets fail explicitly. The catalog is portable with the whole skill folder;
preserve the Microsoft terms. Hashes detect changes relative to the bundled
catalog, not malicious replacement of both the catalog and its assets.
For the [eight Fabric icons](../assets/fabric/README.md), pass `family="fabric"`;
their archive has its own Microsoft MIT license rather than the Azure icon terms.

Service symbols reserve space below for labels, so their bottom port is
deliberately unavailable. Use left/right/top or left-low/right-low ports and
route around captions. Process boxes can use their bottom port. Route points
must align orthogonally with the selected ports. Plan lanes first; there is no
automatic layout or topology selection.
After moving a component, reroute explicit waypoints as needed; attached endpoints
alone do not guarantee that the old route remains orthogonal.

For visible relationship text, supply both `label` and `label_rect`; the full
relationship description can remain in `meaning`. Use short explicit line
breaks. Text rectangles are reserved space, not measured glyph bounds. A font
change or long caption can still wrap outside its slot: inspect the render.

Reference defaults use 18-unit names and 14-unit captions. Presentation mode
raises default labels/captions to at least 20 and expands component slots;
it does not shrink the architecture or choose a slide's content for you.
Recreate mode imposes no checker font floor. The defaults are not accessibility
guarantees and cannot replace review at the actual display/print size.

## Generate and check

PowerShell examples below run from the **skill folder**. On macOS/Linux use
`python3` if needed and native `/` path separators. The scripts themselves are
cross-platform; the external renderer was exercised on Windows only.

Generate to a new directory so prior/user-edited output is not overwritten:

```powershell
python .\examples\fabric-batch\build.py --output-dir .\output\fabric
python .\scripts\check_diagram.py .\output\fabric\architecture.drawio --contract .\output\fabric\contract.json --strict
```

The optional graph contract has a `nodes` object keyed by canonical component
IDs (each with exactly one nonempty `workspace` or `scope`) and an `edges` array with `source`, `target`, and
`kind`. See the [complete contract](../examples/fabric-batch/contract.json).
It is a small comparison input, not a required enterprise modeling framework.

Checker output is JSON. Errors exit nonzero; warnings also exit nonzero with
`--strict`. Without a contract, a structurally valid but incomplete architecture
may pass: the checker cannot infer what the user intended.

| Coverage | Limits |
| --- | --- |
| Unique IDs, parents/cycles, vertex endpoints, geometry | One uncompressed page with plain `mxCell` objects only |
| Required IDs, workspace/scope ownership, exact typed edges | Requires a contract; extra **marked** components are detected; optional `scopes` adds declared containment checks, not product validation |
| Embedded SVG decoding and common external/active constructs | No icon-rights, trademark, authenticity or complete SVG security audit |
| Label/component rectangle overlaps and page overflow | Conservative bounds, not glyphs; intentional overlaps may need manual review |
| Explicit orthogonal routes crossing symbol/label rectangles; symbol ports | Requires `noEdgeStyle=1`, explicit normalized ports, zero perimeter adjustment |
| Mode-specific font floors | Actual zoom, contrast, line wrapping and accessibility remain visual checks |
| Preview/source content hashes | Requires the local export helper's `.render.json`; not proof of visual quality |

Compressed/multipage documents, object wrappers, relative/rotated/flipped vertices and
unsupported image formats are refused explicitly. Automatic/perimeter/diagonal
routing and automatic edge labels produce warnings rather than false geometry
assurance. Optional `--clarity` flags overlapping segments and unmarked crossings.
Curves, arrowheads, exact shape contours and undeclared architecture semantics
still need visual review.
Do not delete unsupported objects or required relationships to obtain a pass.
Use another appropriate check and document the limitation.

## Local PNG export

First confirm that the selected executable's `--help` supports the documented
flags. This wrapper was exercised with draw.io Desktop 32.6.1; other versions
and operating systems require their own smoke check. It is not a universal
renderer adapter.

```powershell
$drawio = 'C:\path\to\draw.io.exe'
python .\scripts\render_diagram.py .\output\fabric\architecture.drawio --drawio $drawio --output .\output\fabric\architecture.png --width 2400
python .\scripts\check_diagram.py .\output\fabric\architecture.drawio --contract .\output\fabric\contract.json --preview .\output\fabric\architecture.png --strict
```

Export uses argument lists, not shell interpolation. It checks the source,
renders to a temporary file, verifies a PNG header, and records source/PNG hashes
without personal paths in `architecture.render.json`. Failed exports and source
changes during export do not replace the previous preview. Existing outputs
require explicit `--overwrite`. If interrupted between replacing the PNG and
record, the hash check reports the mismatch; re-export both together.

Open the **actual PNG** and inspect the whole view and enlarged details. Correct
defects in the generator/source, re-export, and check again. The render record
intentionally does not assert visual acceptance. Document acceptance separately.
No automatic pass count, XML-growth target or density quota applies.

## Optional deeper checks

See [quality-checks.md](quality-checks.md) for explicit `scopes` and edge `intent`
contracts, connector-clarity checks and browser-measured SVG text.
`check_rendered.py` additionally requires an explicit Edge/Chromium executable,
exports a fresh local SVG and uses a temporary browser profile. It does not OCR
the PNG, validate cloud configuration or replace actual image review.
The [Foundry example](../examples/foundry-multi-project/README.md) and
[official-icon Fabric example](../examples/fabric-official/README.md) include
source-linked measurement reports.

## Regression tests

```powershell
python -m unittest discover -s .\tests -p "test_*.py"
```

Tests use synthetic local files and mocked renderer invocations; they do not
launch the renderer, invoke a model or test host skill discovery. The bundled
Fabric preview and [Foundry icon sheet](../examples/foundry-icons/README.md) are
separately rendered and inspected examples. Do not equate
either with an end-to-end host/model benchmark.
Tests also recompute the [pilot results](../benchmarks/README.md) against frozen
source/PNG/text evidence, including known failures; they do not rerun its agents.
