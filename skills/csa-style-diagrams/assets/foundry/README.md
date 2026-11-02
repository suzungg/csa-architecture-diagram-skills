# Curated official Foundry diagram icons

These are **Microsoft assets, not MIT-licensed CSA artwork**. They are bundled
only for use in architecture diagrams, training materials and documentation.
Copy this folder, including its original terms, when copying the skill.

The official [Azure Architecture Center icon terms](https://learn.microsoft.com/en-us/azure/architecture/icons/)
permit copying, distribution and display only for those uses unless Microsoft
grants explicit permission. Microsoft reserves all other rights. The unchanged
[Microsoft_Terms_of_Use.pdf](Microsoft_Terms_of_Use.pdf) from the archive is
included. The skill's MIT license does not relicense these assets or grant
trademark rights.

Do not crop, flip, rotate, distort or recolor the icons. Keep product labels
nearby and do not use Microsoft product icons to represent your own service.
In particular, do not use the Foundry Agent Service icon for an independently
hosted application merely because that application calls a model.

## Exact source

- Official archive: [Azure Public Service Icons V24](https://arch-center.azureedge.net/icons/Azure_Public_Service_Icons_V24.zip)
- Download and terms review: **2026-11-02**
- Archive SHA-256: `921594ccd1bf3d9c0a1bd7b6d924e050551a59342f2b353bb74bdcf761c35141`
- [catalog.json](catalog.json) records stable lookup keys, original archive
  paths and exact SVG hashes. All 13 selected SVGs are byte-identical to their
  archive members. Some archive categories contain identical copies; one exact
  member is recorded for each selected icon.

The complete archive and unrelated icons are not redistributed. The root
source manifest records these SVGs and the terms as a separate `bundled-assets`
source; the surrounding catalog/docs/code are original CSA material.

## Lookup keys

| Key | Symbol |
| --- | --- |
| `foundry` | Microsoft Foundry |
| `foundry-project` | Foundry project |
| `foundry-models` | Foundry Models |
| `foundry-agent-service` | Foundry Agent Service |
| `container-apps-environment` | Container Apps environment, not an individual application |
| `ai-search` | Azure AI Search |
| `cosmos-db` | Azure Cosmos DB |
| `storage-account` | Storage account |
| `key-vault` | Key Vault |
| `firewall` | Azure Firewall |
| `private-endpoint` | Private endpoint |
| `virtual-network` | Virtual network |
| `application-insights` | Application Insights |

Use `icon_path(key)` from the drawing helper. It verifies the local file hash
and rejects unknown keys, missing/modified files and unsafe paths; it does not
download assets or silently replace a symbol.

See the [rendered reference sheet](../../examples/foundry-icons/README.md) and
[Foundry-specific guidance](../../references/foundry.md). An icon's presence is
not proof that a capability exists in a region, deployment type or API version.
