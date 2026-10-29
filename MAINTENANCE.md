# Maintaining the toolkit

## Routine offline checks

From the repository root, using Python 3.10+:

```powershell
python .\tools\validate.py
python -m unittest discover -s tools -p "test_*.py"
git diff --check -- . ':(exclude)skills' ':(exclude)third-party'
```

The validator checks this toolkit's JSON shapes and invariants, source-lock
integrity, bundled-file inventory, skill entrypoint metadata/resource paths,
local Markdown link targets, Python syntax and common credential signatures.
It is not a full YAML parser, Markdown renderer, secret scanner, dependency
audit or semantic architecture checker. No upstream code is imported or run,
and no network connection is made.

Whitespace checks exclude the byte-preserved vendor/original folders: their
upstream trailing whitespace and line endings are intentional snapshot data,
not changes to normalize. The integrity check still covers every such file.

After staging, also run `python .\tools\validate.py --index`. This verifies that
every locked file will actually be committed with its original Git blob and
executable mode. Some upstream tracked files match their own `.gitignore`
patterns (notably Pretty Mermaid theme SVGs); explicitly force-add only those
reviewed lockfile paths when needed. On Windows, preserve upstream executable
bits in the index with `git update-index --chmod=+x -- <reviewed-path>`.
Do not force-add an entire worktree or environment to work around an ignored file.

Run upstream tests separately when changing runtime code. Pretty Mermaid
provides `npm test` and `npm run validate` after an approved `npm ci`.
Azure Diagrams' [eval guide](skills/azure-diagrams/evals/README.md) describes
its installation/import/render checks. These are opt-in and can create output,
need runtimes, or incur costs; do not execute third-party scripts merely to
prove that a folder was copied.

## Updating a pinned source

1. Work on a branch with a clean baseline. Use `SOURCES.json` to identify the
   selected upstream folder, extra license files and excluded paths.
2. Resolve an explicit new commit from the official repository. Review the
   diff and **all applicable license/notice changes** before downloading
   redistributable source. Recheck external entries too; never infer license
   continuity from the old version or GitHub's top-level license badge.
3. Obtain the complete selected folder into a separate review directory.
   Include referenced scripts, assets, templates, fixtures and dependency
   manifests. Do not bring upstream hooks, MCP registrations or CI into this
   repository automatically. Avoid symlinks/submodules and oversized binaries
   without review.
4. Replace only the reviewed selection. Preserve exact bytes and licenses;
   `.gitattributes` disables line-ending conversion for `skills/` and
   `third-party/`. Compare local file bytes with the pinned Git tree blobs.
5. Update the corresponding `SOURCES.json` ref and selections. For every
   affected file, update its `SOURCE-LOCK.json` record: local path, source ID,
   upstream path, size, mode, SHA-256, and Git blob SHA-1. The Git blob digest is
   SHA-1 over `b"blob " + decimal_byte_length + b"\0" + file_bytes`, **not**
   SHA-1 over file bytes alone. Remove records for files actually removed and
   add new files only after reviewing them. Never refresh hashes just to hide
   unexpected local modifications.
6. For Anthropic, enumerate every immediate `skills/*/SKILL.md` again, review
   each license and regenerate `ANTHROPIC-CATALOG.json`; update its human table
   and official marketplace mapping in `ANTHROPIC.md`. Keep restricted or
   unclear files external. Update counts and review dates as the catalog changes.
7. Recheck host/MCP official docs and configuration schemas if relevant.
   Run offline validation, then applicable approved runtime tests. Record
   exactly what was and was not exercised in the commit/release description.
8. Review the complete diff, licenses and credential scan before publishing.
   Use an ordinary commit and non-force push; never overwrite concurrent work.

The user-authored pack has no upstream GitHub source revision separate from
this toolkit. Its initial four files are hashed as the supplied 2026-10-29
snapshot. Subsequent deliberate changes should get a new descriptive revision
and reviewed lock records, without publishing private source filesystem paths.

## Original versus adapted skills

Keep Aymen's originals pinned and byte-identical if advertised as originals.
Do not remove the specified model/research agents, A5 target, ninefold XML
growth or minimum four review passes to make tests pass. If a different
workflow is needed, use the custom skill or clearly name and document an
adaptation with its original attribution and license.

All current vendor files are unchanged. If you intentionally adapt another
third-party file, record the original blob and the modification prominently
(including Apache modification notices where applicable), then extend the
manifest/validator to distinguish adapted content. The current lockfile
intentionally expects equality with upstream bytes.

## Release checklist

Confirm the intended repository visibility, no credentials/customer outputs,
complete license notices, resolvable local links, current prerequisite notes,
and explicit bundled/external status. Do not describe a structural pass as a
rendered-diagram test or authenticated MCP smoke test. Do not install this
toolkit into someone's global agent configuration as part of a release.
