# Optional deeper checks

These are diagram-consistency checks, not Azure/Fabric deployment validation.
Keep the original graph check and visual inspection. A warning is a review
finding, not automatically a defect; unsupported geometry is not a pass.

## Browser-measured text

`check_rendered.py` exports a fresh SVG using an explicitly selected draw.io
Desktop, then measures its text with an explicitly selected Chromium/Edge
browser. It uses actual DOM text ranges after local fonts are ready, rather
than guessing character widths. It reports text beyond reserved rectangles,
overlapping text rectangles, and less than four CSS pixels of separation.
Two CSS pixels of overflow tolerance accommodate renderer rounding.

```powershell
python .\scripts\check_rendered.py .\output\architecture.drawio --drawio 'C:\path\draw.io.exe' --browser 'C:\path\msedge.exe' --strict
```

The browser uses an isolated temporary profile, not the user's signed-in
profile. The review document has a restrictive content-security policy;
external images/styles and active export content are refused. No packages,
browsers or renderers are automatically installed. Only plain-text labels and
the inspected draw.io SVG structure are supported. Missing measurements fail
strict mode rather than silently passing.

This is **browser-laid-out SVG text**, not OCR of the PNG or an assertion that
every renderer/font/zoom looks identical. Fonts, anti-aliasing, exact glyph
contours, accessibility, icon meaning and arrowhead clarity still require
visual review. The JSON includes source hashes and measurements; retain it with
the example and regenerate it after source changes.

## Connector clarity

Add `--clarity` to `check_diagram.py` to flag overlapping collinear connector
segments and proper crossings without an explicit `arc`/`gap` jump marker.
This option is also enabled by the rendered checker.

Shared fan-out lanes may be intentional; review the reported pair rather than
deleting a required relationship. A marker declaration is not proof the
renderer drew the jump correctly. Tangencies, endpoint junctions, curved or
automatic routes and arrowheads still need image inspection.

## Declared ownership versus drawn boundaries

Add an optional `scopes` object to the existing graph contract:

```json
{
  "nodes": {"agent": {"scope": "project-a"}},
  "edges": [],
  "scopes": {
    "foundry": {"boundary": "resource-box", "kind": "resource"},
    "project-a": {"boundary": "project-box", "kind": "project", "parent": "foundry"}
  }
}
```

Every owner must then be declared. Use `"boundary": null` for an explicitly
unbounded/external scope. Boundary vertices carry `csaRole="boundary"` and
`boundaryKind`; helper-created boundaries already do so.

Checks compare whole component rectangles with their declared owner, detect
placement inside an unrelated scope, verify boundary kinds/parent containment,
and reject missing or cyclic scope parents. They **do not infer** ownership,
network isolation, RBAC, subnet membership or product support. Model one clearly
explained containment dimension; logical process groups need not be ownership
boundaries. Existing contracts without `scopes` keep their previous behavior.

## Relationship intent

Optional edge `intent` is `runtime`, `association`, `control` or `telemetry`,
corresponding to `kind` values `data`, `association`, `control` and `telemetry`.
Pass the same explicit intent to `Diagram.connect`; the checker compares the
directed intent inventory. Association intent uses a dashed, arrowless connector
and warns when rendered as a solid/request-style arrow. Explain the legend.
This checks declared semantics and presentation, not whether an API exists.

See the [multi-project Foundry example](../examples/foundry-multi-project/README.md)
for a complete ownership contract and a documented logical request view.
