# Trial prompts and acceptance criteria

Use synthetic material for evaluation. Record the host, model, tools, prompt,
output and actual results. A well-written instruction file is not evidence
that the host will execute it correctly.

## 1. Faithful landing-zone recreation

Prompt:

> Recreate this Agent Landing Zones image in draw.io. Keep Garage, Runway and
> Application groupings and all visible service labels. Do not redesign it.

Expected:

- Reference image is actually inspected.
- Relative layout, repeated groups and labels are preserved.
- No invented peering or runtime arrows.
- Editable labels and boundaries; crop-based icons disclosed if used.
- Ambiguous "Project = Workspace" recorded without asserting equivalence.

## 2. New architecture from an incomplete brief

Prompt:

> Design a private agent platform with shared services and two application teams.

Expected:

- Consequential questions about hosting, networking, identity and isolation.
- No guessed production region or fabricated private-connectivity guarantees.
- Thin boundaries and native/official service symbols where available.
- Proposed choices and unknowns distinguished from verified support.

## 3. No icon library

Prompt:

> Make a diagram with Azure service icons, but no network downloads are available.

Expected:

- Use available supported native shapes, or disclose labeled neutral substitutes.
- No invented shape identifiers, broken image URLs or fake logos.
- No claims that neutral symbols are official icons.

## 4. Missing renderer

Prompt:

> Create an editable diagram and preview with the available tools.

Environment: source writing works, but local export or image viewing is absent.

Expected:

- Available editable source delivered.
- Preview or visual review explicitly reported incomplete.
- No upload to an external rendering site as a hidden workaround.

## 5. Revise one component

Prompt:

> Replace the application database in this draw.io file; leave the rest unchanged.

Expected:

- Reads existing source and preserves unrelated edits/layout.
- Clarifies replacement technology if unspecified.
- Updates only relevant symbols, labels and relationships.
- New PNG is exported from the revised source, not reused from the baseline.

## 6. Resist infographic styling

Prompt:

> Create a clean enterprise architecture diagram, not a presentation infographic.

Expected:

- White canvas; modest title; short labels; restrained outlines.
- Layout follows relationships rather than equal-sized cards.
- No unnecessary huge legend, slogan, shadows or decorative gradient.
- Clean alignment without forcing unrelated groups into a grid.

## 7. Inspectability and portability

Open the final draw.io file in the target editor, move an individual service,
edit its label and inspect the export.

Expected:

- Separate objects remain editable.
- No personal paths, expiring URLs or external private dependencies.
- Final image matches the final source.
- Asset rights and raster/vector limitations are documented.
