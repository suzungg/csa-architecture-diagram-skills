# Microsoft Learn and GitHub MCP

Official documentation reviewed **2026-10-29**. These are **opt-in examples**,
not active server registrations. No MCP server was started or authenticated
while assembling this toolkit.

| Server | Endpoint | Authentication | Scope |
| --- | --- | --- | --- |
| Microsoft Learn | `https://learn.microsoft.com/api/mcp` | None | Public Microsoft documentation and code samples; no Azure tenant data |
| GitHub hosted | `https://api.githubcopilot.com/mcp/` | Supported host OAuth or PAT | Data available to the authenticated identity and enabled tools |
| GitHub read-only (used here) | `https://api.githubcopilot.com/mcp/readonly` | Same as above | Server exposes read tools only; examples further select `repos,issues,pull_requests` |

Both are remote HTTP MCP services. Opening the Learn endpoint in a browser may
return HTTP 405; it expects MCP Streamable HTTP, not a web page. Public access
does not authorize sending private content in search queries.

## VS Code OAuth example

[examples/mcp/vscode-oauth.json](examples/mcp/vscode-oauth.json) uses the
VS Code **`servers`** schema. In a compatible VS Code version (GitHub documents
1.101+ for remote MCP/OAuth), review and merge its two server entries into your
workspace `.vscode/mcp.json`, or use **MCP: Add Server** with the URLs above.
Do not overwrite other configured servers.

Follow server trust and GitHub sign-in prompts. Review the selected account,
requested access and organizational policies before consenting. Learn needs
no sign-in, token or API key. GitHub OAuth support is host-specific; an HTTP
endpoint alone does not make OAuth work in every client.

Current VS Code guidance labels `.vscode/mcp.json` a compatibility/deprecated
destination in the add-server flow; it remains documented and supported.
The portable Copilot format below is the current option for compatible
Copilot harness sessions. Choose deliberately rather than renaming JSON keys
and assuming all properties or authentication behaviors transfer.

## VS Code PAT fallback

[examples/mcp/vscode-pat.json](examples/mcp/vscode-pat.json) is an **alternative**,
not an additional GitHub server to run alongside the OAuth entry. It references
`Bearer ${input:github_mcp_pat}` and defines a password-style `promptString`
input. Supply a token through the VS Code input prompt; never insert the token
in the file, chat or shell history.

Prefer a short-lived fine-grained PAT restricted to the selected repositories.
For repository-content reads start with Contents: read; add Issues: read and
Pull requests: read only when those tools are needed. Exact permissions depend
on the operations, account type and organization policy. Verify against
[GitHub's PAT guidance](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens);
do not default to broad classic `repo` access just to clear a permission error.
Account/organization approval or SSO authorization may still be required.

VS Code's `${input:...}` mechanism belongs to the VS Code format. Current docs
say servers requiring interactive input are not forwarded to Copilot harness
sessions. Use the intended Local harness or the portable environment-reference
example where supported; do not claim that a saved JSON file proves connection.

## Portable Copilot environment-reference example

[examples/mcp/copilot-portable.json](examples/mcp/copilot-portable.json) uses
**`mcpServers`**, HTTP entries, and
`Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN}`. This is not VS Code's `${env:...}` or
`${input:...}` syntax. Review and merge it into a supported workspace-root
`.mcp.json` or Copilot user `mcp-config.json` location following the
[current format reference](https://code.visualstudio.com/docs/agents/reference/mcp-configuration).
Inject the token into the actual host process environment via an approved
secret manager. An unrelated terminal's environment will not configure a
desktop, remote host or container that is already running.

GitHub's [Copilot CLI installation guide](https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-copilot-cli.md)
documents a built-in GitHub MCP server, read-only by default. Inspect existing
configuration first; do not add a duplicate or assume this example restricts a
built-in server with a different ID. In that CLI, the `github-mcp-server` ID in
this example is documented to replace the built-in server. Other hosts can
have different identity and registration rules. This repository does not edit
any host's installed MCP configuration.

## Verify after opting in

1. Inspect the intended server's status/output in your host and finish its
   authentication/trust prompts.
2. Ask Learn to find official documentation for a **generic** Azure service
   feature. Confirm a Learn tool was called and returned source URLs.
3. Ask GitHub to read the README of one specifically authorized repository.
   Inspect the actual server/tool response and selected account.
4. Confirm the server's discovered tools are read-only and limited as expected.
   Do not test this by attempting a write. Review other active servers separately.

An agent answering plausibly from memory is not a successful MCP connection
test. A missing toolset, account policy or expired token is a blocker to report,
not a reason to broaden privileges automatically.

## Boundaries

`/readonly` is a documented server-side tool restriction, **not** a sandbox for
the whole agent, a repository ACL, or a reduction in the token's underlying
permissions. Scope the credential too. Other shell tools and MCP registrations
can still write. Reading private repository content can send it to your model
provider; use approved data-handling policies.

The examples target **github.com**, not GitHub Enterprise Server. Data-residency
GitHub Enterprise Cloud uses a different endpoint; GHES needs the documented
local-server approach. Follow the publisher's enterprise instructions rather
than substituting a hostname in these examples. No third-party bridging proxy
or locally executed MCP package is included.

## Official references

- [Microsoft Learn overview and authentication](https://learn.microsoft.com/en-us/training/support/mcp)
- [Microsoft Learn setup](https://learn.microsoft.com/en-us/training/support/mcp-get-started)
- [GitHub hosted server and OAuth/PAT setup](https://github.com/github/github-mcp-server#remote-github-mcp-server)
- [GitHub read-only URL and toolset headers](https://github.com/github/github-mcp-server/blob/main/docs/remote-server.md)
- [VS Code server setup](https://code.visualstudio.com/docs/agent-customization/mcp-servers)
- [VS Code and portable configuration schemas, inputs and secret handling](https://code.visualstudio.com/docs/agents/reference/mcp-configuration)
