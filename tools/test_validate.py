import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from validate import ROOT, SECRET, git_blob, load_json, markdown_targets, safe_path, validate_index, validate_mcp


class ValidatorTests(unittest.TestCase):
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
