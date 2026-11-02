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
executable mode. If upstream tracked files match ignore patterns, explicitly
force-add only reviewed lockfile paths when needed. On Windows, preserve upstream executable
bits in the index with `git update-index --chmod=+x -- <reviewed-path>`.
Do not force-add an entire worktree or environment to work around an ignored file.

The five bundled skills have instruction entrypoints; CSA also has local
drawing/checking/export helpers and a rendered example. Test host invocation and
rendering separately with synthetic briefs and approved tools; these checks can
create output, need runtimes or incur costs. Do not execute third-party commands
merely to prove that a folder was copied.

## Updating a pinned source

1. Work on a branch with a clean baseline. Use `SOURCES.json` to identify the
   selected upstream folder, extra license files and excluded paths.
2. Resolve an explicit new commit from the official repository. Review the
   diff and **all applicable license/notice changes** before downloading
   redistributable source. Never infer license
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
6. Keep the approved five-skill selection and external Excalidraw reference in
   the catalog, manifest and validator aligned. Ask before removing or broadening
   that selection. Recheck Excalidraw's license before any redistribution. Update the README,
   setup guidance and third-party notices when the selection changes.
7. Recheck host/MCP official docs and configuration schemas if relevant.
   Run offline validation, then applicable approved runtime tests. Record
   exactly what was and was not exercised in the commit/release description.
8. Review the complete diff, licenses and credential scan before publishing.
   Use an ordinary commit and non-force push; never overwrite concurrent work.

The user-authored pack has no upstream GitHub source revision separate from
this toolkit. Its initial four files are hashed as the supplied 2026-10-29
snapshot. Subsequent deliberate changes should get a new descriptive revision
and reviewed lock records, without publishing private source filesystem paths.
The initial 2026-11-02 revision renamed that pack to `csa-style-diagrams` without
changing its behavior. A subsequent user-requested revision on the same date,
`user-authored-architecture-center-2026-11-02`, deliberately changes its visual
defaults toward Azure Architecture Center examples and extends its trial
scenarios. Keep visual-reference citations and distinguish style transfer from
product capabilities. The lockfile records the current revision; Git history
preserves the initial snapshot and original name. Keep the original copyright
notice and do not bundle reference screenshots merely because they were viewed.

The `user-authored-csa-tooling-2026-11-02` revision adds original Python helpers,
regression tests, output modes, an activation/comparison protocol and an annotated
Fabric example with neutral native symbols. It does not modify Aymen's originals
or install the skill. For changes to this package, also run:

```powershell
python -m unittest discover -s .\skills\csa-style-diagrams\tests -p "test_*.py"
```

The tests include regenerated example/source equality and source/PNG hash checks.
For intentional example changes, regenerate from its reviewed generator,
re-export with an explicitly chosen local renderer, inspect the final PNG,
and then refresh **only the reviewed CSA entries** in `SOURCE-LOCK.json`.
Do not silently rehash vendor changes or include `__pycache__`, local executables
or scratch outputs. Keep the render record with the PNG; it is provenance,
not a visual-acceptance certificate. Host invocation and with/without-skill
performance still need separate testing.

The `user-authored-csa-foundry-2026-11-02` revision adds an offline official-icon
lookup, generic scope ownership, resource/project boundaries and Foundry guidance.
Microsoft SVGs/PDF are a separate `bundled-assets` source, pinned by official
archive URL/version/SHA-256 and exact member-to-local paths. They are **not**
part of the original MIT source. The generated reference sheet retains the
separate terms for embedded artwork.

For icon updates, review the official terms again, download the explicit archive,
verify its digest and select exact members. Preserve SVG/PDF bytes and filenames.
Record any identical category copies explicitly rather than choosing an
ambiguous match silently. Update the asset catalog and manifest together,
then refresh only reviewed Microsoft asset lock records. Rebuild/render/inspect
the icon sheet and update its original CSA records separately. `git_blob` for
archive files is a file-derived digest, not a GitHub commit pin. Do not count
an asset source as a new skill or install a renderer during this update.

The `user-authored-csa-quality-pilot-2026-11-02` revision adds a complete
multi-project Foundry example, an official-icon Fabric variant, browser-measured
text, optional declared scope/intent and route-clarity checks, and a preserved
CSA/no-skill pilot. Fabric SVGs and the original Microsoft MIT license form a
separate asset source pinned to commit/archive SHA-256; do not apply Azure's
non-MIT terms to them. Preserve their bytes and recheck official usage guidance.

For intentional example changes, refresh both render and text-measurement reports
from the final source and inspect the PNG. Browser checks require local draw.io
and Edge/Chromium; neither is bundled. Run the scorer without launching agents:

```powershell
python .\skills\csa-style-diagrams\benchmarks\score.py
```

Keep the pilot's first drafts, input snapshot and negative edit evidence immutable.
Its `final` files are disclosed parent derivatives, not model repair turns.
A changed checker may legitimately change scores; review differences rather than
silently replacing historical evidence. New trials should use new evidence sets.
The pilot does not replace repeated, blinded host-activation measurements.

## Original versus adapted skills

Keep Aymen's originals pinned and byte-identical if advertised as originals.
Do not remove the specified model/research agents, A5 target, ninefold XML
growth or minimum four review passes to make tests pass. If a different
workflow is needed, use the custom skill or clearly name and document an
adaptation with its original attribution and license.

All current vendor files are unchanged. If you intentionally adapt another
third-party file, record the original blob and the modification prominently
(including modification notices required by its license), then extend the
manifest/validator to distinguish adapted content. The current lockfile
intentionally expects equality with upstream bytes.

## Release checklist

Confirm the intended repository visibility, no credentials/customer outputs,
complete license notices, resolvable local links, current prerequisite notes,
and the approved five-bundled/one-external inventory. Do not describe a structural pass as a
rendered-diagram test or authenticated MCP smoke test. Do not install this
toolkit into someone's global agent configuration as part of a release.
