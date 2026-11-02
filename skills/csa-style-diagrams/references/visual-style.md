# Visual composition guide

This is independent Architecture Center-inspired guidance, not a Microsoft
standard. A supplied reference takes precedence in faithful recreation.

## Hierarchy and visual language

- White canvas; one ordinary sans-serif such as Arial or Aptos.
- Modest overall title; stronger section headers expose responsibilities.
- Blue/cyan header strips and pale grouping fills suit lifecycle diagrams.
  Network diagrams often benefit from outline-only containers.
- Label boundary meaning: tenant, workspace, network, deployment stage, or
  logical phase. Solid/dashed outlines have no universal Azure meaning.
- Prefer prominent service symbols with short adjacent/below-symbol captions.
  Use flat process boxes for approval and other activities. Do not turn every
  service into an identical card or invent a logo for every verb.
- Use dark neutral primary connectors; distinguish control/telemetry explicitly,
  not solely through color. Preserve recognizable official icon colors.
- Green numbered circles can mark meaningful lifecycle stages, not every object.
  Map them to notes; omit them for topologies without a sequence.
- Align repeated components and environments without imposing a dashboard grid.
  Crop unused margins but retain useful routing and caption space.
- Keep detailed assumptions and tradeoffs in notes. Legends explain ambiguous
  notation; they are not filler. No decorative shields, check marks, locks,
  glows, giant headings, slogans or claimed certification.

For a reference canvas around 1400-1800 units wide, start with 44-64-unit symbols,
18-unit service names, 14-unit captions, 20-24-unit section titles, 32-44-unit
header bands and 24-32-unit numbered circles. Reserve roughly 16-24 units of
padding where practical. These are adjustable starting points, not density
quotas. Presentation output needs larger text and less detail; recreation
preserves the source. Always judge the actual export at its target size.

## Composition families

| Architecture | Useful arrangement |
| --- | --- |
| Data/ML lifecycle | Source estate, preparation/development, approved inference/consumption, adjacent monitoring, perimeter feedback |
| Environment lifecycle | Development beside registration/release; repeated environments aligned only when in scope |
| Request path | Client-to-service flow; dependencies below or alongside |
| Shared platform | Shared capabilities near consumers; access and ownership explicit |
| Hub-spoke | Central hub, repeated spoke/subnet boundaries, differentiated peering and diagnostics |
| Landing zone | Labeled environment/region scopes, nested networks, project associations separate from network links |

Use the MLOps reference's loops only when the requested responsibilities exist.
Do not add staging, production, CI/CD, online inference or automatic retraining
to fill the layout. For Fabric, use Fabric-native services and the selected
batch/online pattern, not Azure ML capabilities copied from an image.

In landing zones, locate private endpoints within their subnet, not the whole
managed service. Keep endpoint representations and shared services distinct.
Place project associations near workloads without turning them into a network
boundary. A dashed cross-zone association does not establish routing or trust.

## Symbols, rights and portability

Prefer verified native service shapes, then official SVGs with suitable terms,
then authorized user vectors, then disclosed neutral symbols. Verify stencil
names by rendering; do not guess them. Never use an unrelated logo.

Use [Azure icon guidance](https://learn.microsoft.com/en-us/azure/architecture/icons/)
or [Fabric icon guidance](https://learn.microsoft.com/en-us/fabric/fundamentals/icons).
Retain source/terms information, colors, aspect ratios and orientation.
Software licenses do not necessarily grant trademark rights or endorsement.

Reference-image crops are a last resort for faithful recreation. Disclose that
they remain embedded rasters, not editable vector paths; do not invent
redistribution permission. Embed approved assets or include supported local
dependencies, never personal paths or expiring URLs. If rendering fails,
report the missing symbol rather than accepting a blank substitution.
