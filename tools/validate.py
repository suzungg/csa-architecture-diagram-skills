"""Offline structural checks for the curated toolkit; standard library only."""
import argparse
import ast
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
IGNORED = {".git", "node_modules", ".venv", "__pycache__", "output", "artifacts"}
REQUIRED_SKILLS = {
    "skills/azure-diagrams",
    "skills/mermaid-diagrams",
    "skills/drawio-pitch",
    "skills/drawio-iterate",
    "skills/csa-style-diagrams",
}
RESOURCE = re.compile(
    r"(?<![\w/])(?:references?|scripts|assets|agents|eval-viewer|themes)/[\w./-]+\.[A-Za-z0-9]+"
)
SECRET = re.compile(
    r"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{40,}"
    r"|sk-ant-[A-Za-z0-9_-]{30,}|AKIA[A-Z0-9]{16}"
    r"|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)"
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)


def safe_path(root, value):
    require(isinstance(value, str) and bool(value), "Expected non-empty relative path")
    path = PurePosixPath(value)
    require(
        not path.is_absolute() and "\\" not in value and ":" not in value
        and ".." not in path.parts,
        f"Unsafe repository path: {value}",
    )
    result = root.joinpath(*path.parts)
    require(result.resolve().is_relative_to(root.resolve()), f"Path escapes repository: {value}")
    return result


def files_under(root):
    return sorted(
        path for path in root.rglob("*")
        if path.is_file() and not set(path.relative_to(root).parts) & IGNORED
    )


def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def validate_index(root, entries):
    output = subprocess.check_output(["git", "ls-files", "--stage", "-z"], cwd=root)
    index = {}
    for record in output.split(b"\0"):
        if record:
            metadata, path = record.decode("utf-8").split("\t", 1)
            mode, digest, stage = metadata.split()
            require(stage == "0", f"Unmerged index entry: {path}")
            index[path] = (mode, digest)
    for entry in entries:
        require(index.get(entry["path"]) == (entry["mode"], entry["git_blob"]),
                f"Staged file missing or differs in bytes/mode: {entry['path']}")


def validate_mcp(config, variant):
    portable = variant == "copilot-portable"
    key = "mcpServers" if portable else "servers"
    expected_keys = {key, "inputs"} if variant == "vscode-pat" else {key}
    require(set(config) == expected_keys, f"{variant}: wrong host configuration shape")
    servers = config[key]
    github_id = "github-mcp-server" if portable else "github"
    require(set(servers) == {"microsoft-learn", github_id}, f"{variant}: unexpected servers")
    require(servers["microsoft-learn"] == {
        "type": "http", "url": "https://learn.microsoft.com/api/mcp"
    }, f"{variant}: Learn must be the public, unauthenticated HTTP endpoint")
    github = servers[github_id]
    require(set(github) == {"type", "url", "headers"}, f"{variant}: unexpected GitHub properties")
    require(github["type"] == "http", f"{variant}: wrong GitHub transport")
    require(github["url"] == "https://api.githubcopilot.com/mcp/readonly",
            f"{variant}: GitHub read-only endpoint required")
    headers = {"X-MCP-Toolsets": "repos,issues,pull_requests"}
    if portable:
        headers["Authorization"] = "Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN}"
    elif variant == "vscode-pat":
        headers["Authorization"] = "Bearer ${input:github_mcp_pat}"
        inputs = config["inputs"]
        require(len(inputs) == 1, "PAT example must define one input")
        require(set(inputs[0]) == {"id", "type", "description", "password"}, "Wrong PAT input shape")
        require(inputs[0]["id"] == "github_mcp_pat" and inputs[0]["type"] == "promptString"
                and inputs[0]["password"] is True and bool(inputs[0]["description"]),
                "PAT input must be a named password prompt")
    require(github["headers"] == headers, f"{variant}: unsafe or unsupported header configuration")


def markdown_targets(text):
    text = re.sub(r"^```[^\n]*\n.*?^```[^\n]*$", "", text, flags=re.M | re.S)
    return re.findall(r"\[[^\]\n]*\]\(([^\s)]+)(?:\s+[^)]*)?\)", text)


def validate_asset_source(root, source):
    """Validate reviewed Microsoft icon archives, not additional skills."""
    if source["url"] == "https://learn.microsoft.com/en-us/azure/architecture/icons/":
        require(re.fullmatch(r"V[0-9]+", source["ref"]), "Unversioned icon archive")
        archive_url = f"https://arch-center.azureedge.net/icons/Azure_Public_Service_Icons_{source['ref']}.zip"
        family, terms = "foundry", "Microsoft_Terms_of_Use.pdf"
        require(source["license"] == "Microsoft Azure architecture icon terms",
                "Microsoft Foundry icons must retain their own permitted-use terms, not MIT")
    elif source["url"] == "https://learn.microsoft.com/en-us/fabric/fundamentals/icons":
        require(re.fullmatch(r"[0-9a-f]{40}", source["ref"]), "Unpinned Fabric archive")
        archive_url = f"https://raw.githubusercontent.com/microsoft/fabric-samples/{source['ref']}/docs-samples/Icons.zip"
        family, terms = "fabric", "LICENSE"
        require(source["license"] == "MIT (Microsoft archive license); follow Microsoft Fabric icon usage guidance",
                "Preserve the Fabric archive license and usage guidance")
    else:
        raise ValueError("Unsupported asset provider URL")
    require(source["archive_url"] == archive_url, "Unexpected icon archive URL")
    require(re.fullmatch(r"[0-9a-f]{64}", source["archive_sha256"]), "Unpinned archive digest")
    mapping = source["files"]
    prefix = f"skills/csa-style-diagrams/assets/{family}/"
    require(isinstance(mapping, dict) and bool(mapping), "Asset source needs an explicit file mapping")
    require(len(set(mapping.values())) == len(mapping), "Duplicate asset destinations")
    for upstream, local in mapping.items():
        safe_path(root, upstream)
        safe_path(root, local)
        require(local.startswith(prefix), "Asset outside the declared asset folder")
    require(source["license_path"] in mapping, "Original asset terms must be included")
    require(mapping[source["license_path"]] == prefix + terms,
            "Unexpected terms destination")
    catalog_path = safe_path(root, source["catalog"])
    require(source["catalog"] == prefix + "catalog.json", "Unexpected icon catalog location")
    catalog = load_json(catalog_path)
    require(catalog["schema_version"] == 1, "Unsupported icon catalog schema")
    for key in ("archive_url", "archive_sha256", "license"):
        require(catalog[key] == source[key], f"Icon catalog/source disagree: {key}")
    require(catalog["source_url"] == source["url"], "Icon source URL differs")
    require(catalog["terms_file"] == terms, "Icon terms file differs")
    icons = catalog["icons"]
    require(isinstance(icons, dict) and bool(icons), "Icon catalog must not be empty")
    selected = {source["license_path"]}
    for alias, icon in icons.items():
        require(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", alias), "Invalid icon alias")
        local = prefix + icon["path"]
        path = safe_path(root, local)
        require(path.suffix == ".svg" and icon["path"].startswith("icons/"), "Expected local icon SVG")
        require(mapping.get(icon["upstream_path"]) == local, "Icon catalog/archive mapping differs")
        require(icon["upstream_path"] not in selected, "Duplicate icon source in catalog")
        selected.add(icon["upstream_path"])
        require(hashlib.sha256(path.read_bytes()).hexdigest() == icon["sha256"], "Icon catalog hash differs")
    require(selected == set(mapping), "Catalog and asset selection differ")
    return set(mapping.values())


def validate(root=ROOT, check_index=False):
    all_files = files_under(root)
    for file in all_files:
        if file.suffix == ".json":
            load_json(file)
    manifest = load_json(root / "SOURCES.json")
    lock = load_json(root / "SOURCE-LOCK.json")
    for document in (manifest, lock):
        require(document["schema_version"] == 1, "Unsupported manifest schema")
    sources = manifest["sources"]
    by_id = {s["id"]: s for s in sources}
    require(len(by_id) == len(sources), "Duplicate source ID")
    expected_skills = set()
    asset_paths = set()
    for source in sources:
        if source["status"] == "bundled-assets":
            paths = validate_asset_source(root, source)
            require(not asset_paths & paths, "Asset has multiple declared sources")
            asset_paths.update(paths)
            continue
        require(source["url"].startswith("https://github.com/"), "Expected canonical upstream URL")
        if "repository" in source:
            require(source["url"] == "https://github.com/" + source["repository"], "Repository URL mismatch")
            require(re.fullmatch(r"[0-9a-f]{40}", source["ref"]), f"Unpinned source: {source['id']}")
            require(source["status"] in {"bundled", "partial", "external"}, "Unknown source status")
            for selection in source["selections"]:
                safe_path(root, selection["local"])
                require(selection["local"].startswith("skills/"), "Skill outside distribution directory")
                expected_skills.add(selection["local"])
            if source["status"] == "external":
                require(not source["selections"], "External source has bundled files")
        else:
            require(source["status"] == "bundled-original", "Unknown local source status")
            expected_skills.add(source["local"])
            for name in source["required_files"]:
                require(safe_path(root, source["local"] + "/" + name).is_file(), f"Missing original file: {name}")
    require(expected_skills == REQUIRED_SKILLS,
            "Source selections must contain exactly the five approved architecture skills")
    require({s["id"] for s in sources if s["status"] == "external"} == {"excalidraw-diagram"},
            "Excalidraw must remain explicitly cataloged as external until redistribution rights are reviewed")

    locked_paths = set()
    for entry in lock["files"]:
        local = entry["path"]
        require(local not in locked_paths, f"Duplicate lock path: {local}")
        locked_paths.add(local)
        require(entry["source"] in by_id, f"Unknown lock source: {local}")
        source = by_id[entry["source"]]
        require(source["status"] != "external", f"External source was copied: {local}")
        safe_path(root, entry["upstream_path"])
        if source["status"] == "bundled-assets":
            mapped = source["files"].get(entry["upstream_path"]) == local
        elif source["status"] == "bundled-original":
            mapped = local == source["local"] + "/" + entry["upstream_path"] and local not in asset_paths
        else:
            mapped = source.get("notices", {}).get(entry["upstream_path"]) == local
            for selection in source["selections"]:
                prefix = selection["upstream"] + "/" if selection["upstream"] else ""
                upstream = entry["upstream_path"]
                if upstream.startswith(prefix):
                    relative = upstream[len(prefix):]
                    excluded = any(relative.startswith(p) for p in selection.get("exclude_prefixes", []))
                    mapped |= not excluded and local == selection["local"] + "/" + relative
                extra = selection.get("extra_files", {}).get(upstream)
                mapped |= extra is not None and local == selection["local"] + "/" + extra
        require(mapped, f"Lock path is not in declared source selection: {local}")
        file = safe_path(root, local)
        data = file.read_bytes()
        require(entry["mode"] in {"100644", "100755"}, f"Unsupported file mode: {local}")
        require(len(data) == entry["bytes"], f"Size differs: {local}")
        require(hashlib.sha256(data).hexdigest() == entry["sha256"], f"SHA-256 differs: {local}")
        require(git_blob(data) == entry["git_blob"], f"Upstream Git blob differs: {local}")
    actual = {p.relative_to(root).as_posix() for folder in ("skills", "third-party")
              for p in files_under(root / folder)}
    require(actual == locked_paths, f"Bundle/lock inventory mismatch: {sorted(actual ^ locked_paths)}")
    if check_index:
        validate_index(root, lock["files"])

    skills = list((root / "skills").glob("*/SKILL.md"))
    require({p.parent.relative_to(root).as_posix() for p in skills} == expected_skills,
            "Skill inventory differs from source selections")
    for file in skills:
        text = file.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
        require(match is not None, f"Missing frontmatter: {file}")
        front = match.group(1)
        name = re.search(r"^name:\s*([a-z0-9]+(?:-[a-z0-9]+)*)\s*$", front, re.M)
        require(name is not None and name.group(1) == file.parent.name, f"Skill name mismatch: {file}")
        require(re.search(r"^description:\s*\S", front, re.M), f"Missing description: {file}")
        require(any((file.parent / p).is_file() for p in ("LICENSE", "LICENSE.txt")), f"Missing license: {file}")
        for resource in set(RESOURCE.findall(text)):
            require((file.parent / resource).is_file(), f"Missing skill resource: {file}: {resource}")
    for variant in ("vscode-oauth", "vscode-pat", "copilot-portable"):
        validate_mcp(load_json(root / "examples/mcp" / (variant + ".json")), variant)
    links = 0
    for file in all_files:
        if file.suffix == ".py":
            ast.parse(file.read_text(encoding="utf-8"), filename=str(file))
        if file.suffix == ".md":
            for target in markdown_targets(file.read_text(encoding="utf-8")):
                if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                    continue
                path = unquote(target.split("#", 1)[0])
                if path:
                    require((file.parent / path).exists(), f"Broken Markdown link: {file}: {target}")
                    links += 1
        if file.suffix.lower() in {".md", ".py", ".mjs", ".json", ".txt", ".html", ".xml", ".mmd"}:
            text = file.read_text(encoding="utf-8")
            require(SECRET.search(text) is None, f"Possible credential in {file}; inspect privately")
    print(f"PASS: {len(skills)} skills; {len(locked_paths)} byte-verified bundled files; "
          f"3 MCP configs; {links} local Markdown targets.")
    print("JSON, Python syntax, skill resources and common credential signatures checked. "
          "No skill execution, rendering, network or MCP authentication performed.")
    if check_index:
        print("Git index: every locked file is staged with its original blob and mode.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", action="store_true", help="Also verify bundled blobs/modes in the Git index")
    args = parser.parse_args()
    try:
        validate(check_index=args.index)
    except (OSError, ValueError, KeyError, TypeError, SyntaxError, subprocess.CalledProcessError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
