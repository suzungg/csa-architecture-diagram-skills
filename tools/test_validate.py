import copy
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from validate import ROOT, SECRET, git_blob, load_json, markdown_targets, safe_path, validate, validate_asset_source, validate_index, validate_mcp


class ValidatorTests(unittest.TestCase):
    def test_current_four_skill_toolkit(self):
        output = io.StringIO()
        with redirect_stdout(output):
            validate()
        self.assertIn("PASS: 4 skills;", output.getvalue())
        self.assertIn("3 MCP configs;", output.getvalue())

    def test_changed_skill_selection_rejected(self):
        for selections in ([], [{"upstream": "skills/extra", "local": "skills/extra"}]):
            with self.subTest(selections=selections), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source = copy.deepcopy(load_json(ROOT / "SOURCES.json")["sources"][0])
                source["selections"] = selections
                (root / "SOURCES.json").write_text(
                    json.dumps({"schema_version": 1, "sources": [source]}), encoding="utf-8")
                (root / "SOURCE-LOCK.json").write_text(
                    '{"schema_version": 1, "files": []}', encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "four approved architecture skills"):
                    validate(root)

    def test_official_icon_archive_source(self):
        source = next(s for s in load_json(ROOT / "SOURCES.json")["sources"] if s["status"] == "bundled-assets")
        self.assertEqual(len(validate_asset_source(ROOT, source)), 14)
        for key, value in (("url", "https://example.invalid/icons"), ("archive_url", "https://example.invalid/icons.zip"),
                           ("archive_sha256", "not-a-hash"), ("license", "MIT"),
                           ("license_path", "missing.pdf"), ("ref", "latest")):
            changed = copy.deepcopy(source)
            changed[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_asset_source(ROOT, changed)
        changed = copy.deepcopy(source)
        upstream = next(iter(changed["files"]))
        changed["files"][upstream] = "skills/csa-style-diagrams/outside.svg"
        with self.assertRaisesRegex(ValueError, "outside"):
            validate_asset_source(ROOT, changed)

    def test_icon_catalog_mapping_and_hash_must_match(self):
        source = next(s for s in load_json(ROOT / "SOURCES.json")["sources"] if s["status"] == "bundled-assets")
        catalog = load_json(ROOT / source["catalog"])
        alias = next(iter(catalog["icons"]))
        for key, value in (("sha256", "0"*64), ("upstream_path", "missing.svg"), ("path", "../escape.svg")):
            changed = copy.deepcopy(catalog)
            changed["icons"][alias][key] = value
            with self.subTest(key=key), patch("validate.load_json", return_value=changed), self.assertRaises(ValueError):
                validate_asset_source(ROOT, source)

    def test_official_fabric_archive_and_distinct_license(self):
        source = next(s for s in load_json(ROOT / "SOURCES.json")["sources"] if s["id"] == "microsoft-fabric-icons-6.1.0")
        self.assertEqual(len(validate_asset_source(ROOT, source)), 9)
        for key, value in (("license", "Microsoft Azure architecture icon terms"),
                           ("ref", "main"), ("archive_url", source["archive_url"].replace(source["ref"], "main")),
                           ("license_path", "LICENSE")):
            changed = copy.deepcopy(source)
            changed[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_asset_source(ROOT, changed)

    def test_microsoft_asset_cannot_be_attributed_to_original_mit_source(self):
        lock_path = ROOT / "SOURCE-LOCK.json"
        lock = copy.deepcopy(load_json(lock_path))
        entry = next(e for e in lock["files"] if e["source"] == "microsoft-azure-icons-v24")
        entry["source"] = "csa-style-diagrams"
        entry["upstream_path"] = entry["path"].removeprefix("skills/csa-style-diagrams/")
        original_load = load_json
        def replaced(path):
            return lock if path == lock_path else original_load(path)
        with patch("validate.load_json", side_effect=replaced):
            with self.assertRaisesRegex(ValueError, "not in declared source selection"):
                validate()

    def config(self, variant):
        return load_json(ROOT / "examples/mcp" / (variant + ".json"))

    def test_valid_mcp_examples(self):
        for variant in ("vscode-oauth", "vscode-pat", "copilot-portable"):
            with self.subTest(variant=variant):
                validate_mcp(self.config(variant), variant)

    def test_writable_github_endpoint_rejected(self):
        config = self.config("vscode-oauth")
        config["servers"]["github"]["url"] = "https://api.githubcopilot.com/mcp/"
        with self.assertRaisesRegex(ValueError, "read-only"):
            validate_mcp(config, "vscode-oauth")

    def test_wrong_host_schema_rejected(self):
        with self.assertRaisesRegex(ValueError, "shape"):
            validate_mcp(self.config("copilot-portable"), "vscode-oauth")

    def test_literal_credentials_and_unmasked_input_rejected(self):
        config = self.config("vscode-pat")
        unsafe = copy.deepcopy(config)
        unsafe["servers"]["github"]["headers"]["Authorization"] = "Bearer example-literal"
        with self.assertRaisesRegex(ValueError, "header"):
            validate_mcp(unsafe, "vscode-pat")
        config["inputs"][0]["password"] = False
        with self.assertRaisesRegex(ValueError, "password"):
            validate_mcp(config, "vscode-pat")

    def test_learn_auth_rejected(self):
        config = self.config("vscode-oauth")
        config["servers"]["microsoft-learn"]["headers"] = {"Authorization": "unexpected"}
        with self.assertRaisesRegex(ValueError, "unauthenticated"):
            validate_mcp(config, "vscode-oauth")

    def test_safe_paths(self):
        self.assertEqual(safe_path(ROOT, "skills/example/SKILL.md"),
                         ROOT / "skills" / "example" / "SKILL.md")
        for value in ("../escape", "/absolute", "C:/absolute", r"skills\escape", ""):
            with self.subTest(value=value), self.assertRaises(ValueError):
                safe_path(ROOT, value)

    def test_duplicate_json_keys_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            file = Path(directory) / "duplicate.json"
            file.write_text('{"servers": {}, "servers": {}}')
            with self.assertRaisesRegex(ValueError, "Duplicate"):
                load_json(file)

    def test_git_blob_includes_header(self):
        self.assertEqual(git_blob(b""), "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391")
        self.assertNotEqual(git_blob(b"data"), git_blob(b"data\n"))

    def test_index_requires_original_blob_and_mode(self):
        digest = git_blob(b"")
        entry = {"path": "skills/test/script.py", "mode": "100755", "git_blob": digest}
        output = f"100755 {digest} 0\tskills/test/script.py\0".encode()
        with patch("validate.subprocess.check_output", return_value=output):
            validate_index(ROOT, [entry])
            with self.assertRaisesRegex(ValueError, "missing or differs"):
                validate_index(ROOT, [{**entry, "mode": "100644"}])
        with patch("validate.subprocess.check_output", return_value=b""):
            with self.assertRaisesRegex(ValueError, "missing or differs"):
                validate_index(ROOT, [entry])

    def test_markdown_examples_are_not_file_links(self):
        text = "[real](README.md)\n```md\n[example](not-a-file.md)\n```\n[end](MCP.md)\n"
        self.assertEqual(markdown_targets(text), ["README.md", "MCP.md"])

    def test_credential_signature_and_placeholder(self):
        self.assertIsNotNone(SECRET.search("gh" + "p_" + "a" * 36))
        self.assertIsNone(SECRET.search("Bearer ${input:github_mcp_pat}"))


if __name__ == "__main__":
    unittest.main()
