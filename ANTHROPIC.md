# Official Anthropic skills

This toolkit catalogs **all 19 skill folders** in
[anthropics/skills at ca45fc4](https://github.com/anthropics/skills/tree/ca45fc496a3436251f191354091d557da31c15b5/skills),
reviewed 2026-10-29. It is not a full source mirror or an Anthropic product.

**Six complete Apache-2.0 skills are bundled** with their own licenses.
The other 13 are external. Four document skills have restrictive
service-governed licenses and are **not copied or relicensed** here.
`doc-coauthoring` has no per-skill license file at this pin, so it is also
left external rather than inferring permission from its neighbors.

| Official skill | Status | Useful for / limitation |
| --- | --- | --- |
| academy-guide | External, Apache-2.0 | Claude learning resources |
| algorithmic-art | External, Apache-2.0 | Generative art, outside the core diagram bundle |
| [brand-guidelines](skills/brand-guidelines/SKILL.md) | Bundled, Apache-2.0 | Anthropic's branding, **not** Microsoft or customer branding |
| canvas-design | External, Apache-2.0 | Static visual design and font assets |
| claude-api | External, Apache-2.0 | Claude API/SDK development |
| discernment-nudge | External, Apache-2.0 | Critical follow-up questions |
| doc-coauthoring | External, license not established here | Structured writing; use official channel under applicable terms |
| docx | External, restricted | Word documents; official service/plugin only |
| [frontend-design](skills/frontend-design/SKILL.md) | Bundled, Apache-2.0 | Web presentation/UI, not a technical diagram renderer |
| [internal-comms](skills/internal-comms/SKILL.md) | Bundled, Apache-2.0 | Status updates, FAQs and communication examples |
| [mcp-builder](skills/mcp-builder/SKILL.md) | Bundled, Apache-2.0 | Author/test MCP servers; not needed merely to connect Learn or GitHub |
| pdf | External, restricted | PDF workflows; official service/plugin only |
| pptx | External, restricted | Slide workflows; official service/plugin only |
| [skill-creator](skills/skill-creator/SKILL.md) | Bundled, Apache-2.0 | Authoring, evaluation and iteration of skills |
| slack-gif-creator | External, Apache-2.0 | Animation, outside the diagram bundle |
| [theme-factory](skills/theme-factory/SKILL.md) | Bundled, Apache-2.0 | Theme definitions plus the required showcase PDF |
| web-artifacts-builder | External, Apache-2.0 | Rich web artifacts |
| webapp-testing | External, Apache-2.0 | Browser-based web testing |
| xlsx | External, restricted | Spreadsheets; official service/plugin only |

Every row has an exact upstream folder URL, commit, license URL (when present)
and local status in [ANTHROPIC-CATALOG.json](ANTHROPIC-CATALOG.json).
The bundle preserves [upstream notices](third-party/anthropic/THIRD_PARTY_NOTICES.md).
Apache licensing of a skill does not grant permission to use product trademarks
or redistribute a differently licensed skill.

## Official Claude Code installation

The pinned [upstream README](https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/README.md)
and [marketplace definition](https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/.claude-plugin/marketplace.json)
document these commands **inside Claude Code**, not a PowerShell shell:

```text
/plugin marketplace add anthropics/skills
/plugin install example-skills@anthropic-agent-skills
/plugin install document-skills@anthropic-agent-skills
```

The marketplace also lists the following plugins, using the same documented
plugin-install syntax:

```text
/plugin install claude-api@anthropic-agent-skills
/plugin install academy-guide@anthropic-agent-skills
/plugin install discernment-nudge@anthropic-agent-skills
```

Together those five plugins cover the 19 folders at the reviewed revision.
Choose only what you need; marketplace commands resolve the publisher's
available version, **not this repository's pinned snapshot**. Review the version,
new dependencies and current terms before installation. The publisher's
`document-skills` install route does not grant permission to extract or mirror
its restricted contents into this toolkit or another repository.

If you already copied one of the six bundled skills into Claude Code, avoid
installing a second copy with the same name via `example-skills`. Prefer one
source and review differences before switching.

## Claude.ai and API

Use the official [Claude skill guide](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
and [API skills guide](https://docs.claude.com/en/api/skills-guide).
Availability depends on the product, plan and current terms. This toolkit
does not provide a Claude subscription, API entitlement or permission to use
restricted document skills with an unrelated model.

## Bundled helper dependencies

`brand-guidelines`, `frontend-design` and `internal-comms` primarily provide
instructions; actual artifact creation needs tools supplied by the host.
`brand-guidelines` describes optional `python-pptx` usage and system fonts.
`theme-factory` includes ten theme files and its required 124 KB showcase PDF,
not a document renderer.

The MCP evaluation helper has a
[Python requirements file](skills/mcp-builder/scripts/requirements.txt)
for the `anthropic` and `mcp` packages. Evaluation calls model APIs and
connects to the chosen server; installing the skill is not authorization to
run those operations or spend API credits.

`skill-creator`'s basic validator imports **PyYAML**, while description
optimization invokes **`claude -p`** and assumes appropriate Claude
authentication. Its upstream folder has no dependency manifest for PyYAML.
If you deliberately use that helper, install `PyYAML` in your isolated
environment after review; this repository's own validator uses only the Python
standard library. Some upstream evaluation code uses POSIX pipe polling, and
generated reports can fetch Google Fonts. Native Windows execution and offline
behavior have not been certified; use an appropriate environment and inspect
network behavior before processing private data.

No Anthropic helper or evaluation loop was executed during packaging.
