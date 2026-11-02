# Foundry-specific diagram guidance

Use this reference for Foundry diagrams in addition to the general CSA workflow.
The [curated icon set](../assets/foundry/README.md) and its
[editable reference sheet](../examples/foundry-icons/README.md) are ready for
offline diagram authoring. They are not a mandatory landing-zone architecture.

## Select symbols by meaning

| Concept | Icon key / representation | Do not imply |
| --- | --- | --- |
| Microsoft Foundry resource | `foundry`; label the actual resource scope | All connected services are hosted inside that resource |
| Foundry project | `foundry-project`; `kind="project"` for its boundary | A separate VNet, a separate model deployment by default, or an inference proxy hop |
| Models / model deployments | `foundry-models`; name the actual deployment and scope | Every project owns a duplicate deployment or every model uses the same API |
| Foundry Agent Service | `foundry-agent-service`; name the agent type/runtime | Arbitrary application-owned orchestration runs in Agent Service |
| Customer application hosting | Its real hosting icon or a labeled process | A Container Apps **environment** icon is the individual application |
| Private endpoint | `private-endpoint` inside the client VNet/subnet | The whole managed Foundry service lives inside the VNet |
| Search, Cosmos DB, Storage, Key Vault | Their own symbols and governance scopes | Every workload requires every service or inherits Foundry networking/RBAC automatically |

Keep actual ownership labels visible. Use `scope="foundry-resource"` or
`scope="project:use-case-a"` in helper metadata; reserve `workspace=...` for
actual workspace ownership. The contract checker accepts exactly one of these
fields per component. `kind="resource"` and `kind="project"` boundaries are
available alongside the existing logical/network/workspace types.
Metadata does not create physical containment or validate access policy.

## Foundry architecture guardrails

- Declare whether the diagram represents the current Foundry resource/project
  model or a classic hub-based project architecture. Do not mix their resource
  types, endpoints or network assumptions.
- In the current model, a Foundry resource is an `AIServices` account and a
  project is its `accounts/projects` subresource. Resource-level governance
  includes model deployments; projects scope development assets and can reuse
  existing deployments/connections. Show the real ownership instead of using
  a project icon as a generic runtime router.
- State whether orchestration is application-owned or uses a Foundry agent.
  Distinguish prompt/hosted agent choices and the chosen data/network setup.
  Verify their actual dependencies; do not make standard/BYO resources
  mandatory for every basic setup.
- Connected Azure services remain independently governed resources. Identify
  data access, managed identities, RBAC and network dependencies separately.
  An association or project membership is not a request path.
- Separate inbound private access from outbound agent/data access. A private
  endpoint needs approval, DNS and reachability; it does not establish peering,
  outbound isolation or permission to access another service.
- Do not draw the whole managed service in a customer subnet merely because
  it has a private endpoint. If an agent runtime uses a documented delegated
  subnet/injection model, label that runtime precisely and verify the selected
  networking mode instead of moving the whole Foundry resource into it.
- If another landing zone or gateway calls models, show the configured path.
  Do not assume transitive peering, automatic cross-cloud identity federation,
  private cross-cloud TLS, or provider fallback simply from an arrow/icon.
- Verify deployment type, region/data-processing scope, API support and preview
  status for the actual design. Generic model icons do not prove these choices.

## Use the local lookup

After importing the bundled helper in a local generator:

```python
from csa_drawio import Diagram, icon_path

d = Diagram("Foundry ownership example", 1000, 650)
d.boundary("resource", "Foundry resource", (40, 100, 920, 490), kind="resource")
d.boundary("project-a", "Project A", (80, 200, 360, 330), kind="project")
d.component("agent", "Foundry Agent Service", 130, 300, width=260,
            scope="project:use-case-a", caption="Agent configuration / assets",
            svg=icon_path("foundry-agent-service"))
d.component("models", "Shared model deployments", 600, 300, width=270,
            scope="foundry-resource", caption="Resource scope",
            svg=icon_path("foundry-models"))
```

This snippet expresses ownership only, not a complete runtime or network design.
Add only relationships supported by the actual brief. Inspect the final export
and retain icon terms with packaged assets. The standalone
[reference-sheet generator](../examples/foundry-icons/build.py) exercises every
lookup key and provides a complete build/export starting point.

## Authoritative references

Reviewed **2026-11-02**; check them again when making new capability or networking
claims. These references establish product semantics, not an immutable template.

- [Foundry architecture and resource/project hierarchy](https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture)
- [Foundry network isolation](https://learn.microsoft.com/en-us/azure/foundry/how-to/configure-private-link)
- [Azure architecture icon terms and usage](https://learn.microsoft.com/en-us/azure/architecture/icons/)
