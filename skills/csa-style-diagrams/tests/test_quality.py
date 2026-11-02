import hashlib
import json
from pathlib import Path
import runpy
import sys
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from csa_drawio import Diagram, icon_path
from check_diagram import check, route_clarity
from check_rendered import inspect_svg


class QualityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.source = self.base / "architecture.drawio"
        self.contract = self.base / "contract.json"
        d = Diagram("Scope check", 1000, 600)
        d.boundary("one", "One", (50, 50, 300, 300), kind="project")
        d.boundary("two", "Two", (450, 50, 300, 300), kind="project")
        d.component("a", "One", 100, 150, scope="A")
        d.component("b", "Two", 500, 150, scope="B")
        d.connect("association", "a", "b", kind="association", intent="association", meaning="Reference")
        d.save(self.source)
        self.spec = {
            "nodes": {"a": {"scope": "A"}, "b": {"scope": "B"}},
            "edges": [{"source": "a", "target": "b", "kind": "association", "intent": "association"}],
            "scopes": {"A": {"boundary": "one", "kind": "project"}, "B": {"boundary": "two", "kind": "project"}},
        }

    def report(self):
        self.contract.write_text(json.dumps(self.spec))
        return check(self.source, contract=self.contract, clarity=True)

    def mutate(self, fn):
        tree = ET.parse(self.source)
        fn(tree)
        tree.write(self.source)

    def test_scopes_and_association_pass(self):
        self.assertEqual(self.report()["errors"], 0)
        self.assertEqual(self.report()["warnings"], 0)

    def test_outside_owner_and_inside_wrong_scope(self):
        self.mutate(lambda t: t.find(".//mxCell[@id='a']/mxGeometry").set("x", "500"))
        codes = {i["code"] for i in self.report()["issues"]}
        self.assertTrue({"scope-containment", "scope-conflict"} <= codes)

    def test_scope_parent_cycle_kind_and_missing_owner(self):
        self.spec["scopes"]["A"]["parent"] = "A"
        self.assertIn("invalid-input", {i["code"] for i in self.report()["issues"]})
        self.spec["scopes"]["A"].pop("parent")
        self.spec["scopes"]["A"]["kind"] = "network"
        self.assertIn("scope-kind", {i["code"] for i in self.report()["issues"]})
        self.spec["scopes"].pop("A")
        self.assertIn("invalid-input", {i["code"] for i in self.report()["issues"]})

    def test_child_scope_must_fit_parent(self):
        self.spec["scopes"]["A"]["parent"] = "B"
        self.assertIn("scope-parent", {i["code"] for i in self.report()["issues"]})

    def test_malformed_referenced_scope_is_reported(self):
        self.spec["scopes"]["A"]["parent"] = "B"
        for invalid in (None, [], "not-an-object", {"boundary": []}, {"boundary": "two", "parent": {}}):
            with self.subTest(invalid=invalid):
                self.spec["scopes"]["B"] = invalid
                self.assertIn("invalid-input", {i["code"] for i in self.report()["issues"]})

    def test_intent_mismatch_and_association_appearance(self):
        self.mutate(lambda t: t.find(".//mxCell[@id='association']").set("intent", "runtime"))
        self.assertIn("relationship-intent", {i["code"] for i in self.report()["issues"]})
        self.mutate(lambda t: t.find(".//mxCell[@id='association']").set("intent", "association"))
        self.mutate(lambda t: t.find(".//mxCell[@id='association']").set("style", "endArrow=block;"))
        self.assertIn("association-style", {i["code"] for i in self.report()["issues"]})

    def test_route_clarity_crossing_marker_and_overlap(self):
        issues = []
        issue = lambda level, code, message: issues.append(code)
        a = ("a", [(0, 10), (100, 10)], {})
        b = ("b", [(50, 0), (50, 50)], {})
        route_clarity([a, b], issue)
        self.assertEqual(issues, ["ambiguous-crossing"])
        issues.clear()
        route_clarity([a, (b[0], b[1], {"jumpStyle": "arc"})], issue)
        self.assertEqual(issues, [])
        route_clarity([a, ("c", [(20, 10), (90, 10)], {})], issue)
        self.assertEqual(issues, ["route-overlap"])

    def test_fabric_icons_and_family_validation(self):
        for alias in ("lakehouse", "notebook", "experiment", "model", "pipeline", "dataflow-gen2", "semantic-model", "report"):
            self.assertTrue(icon_path(alias, family="fabric").is_file())
        with self.assertRaises(ValueError):
            icon_path("model", family="../fabric")

    def test_exported_svg_refuses_active_and_remote_content(self):
        for body in ('<script>bad()</script>', '<image href="https://example.invalid/a"/>',
                     '<rect onclick="bad()"/>', '<style>@import "bad.css"</style>',
                     '<foreignObject><iframe src="file:///private"/></foreignObject>'):
            with self.subTest(body=body), self.assertRaises(ValueError):
                inspect_svg(f'<svg xmlns="http://www.w3.org/2000/svg">{body}</svg>')
        inspect_svg('<svg xmlns="http://www.w3.org/2000/svg"><foreignObject><div xmlns="http://www.w3.org/1999/xhtml">Plain text</div></foreignObject></svg>')


class BenchmarkTests(unittest.TestCase):
    root = Path(__file__).resolve().parents[1] / "benchmarks"

    def scorer(self):
        return runpy.run_path(str(self.root / "score.py"))["score"]

    def test_recorded_results_recompute_and_keep_negative_evidence(self):
        rows = self.scorer()()
        self.assertEqual(rows, json.loads((self.root / "results.json").read_text()))
        self.assertEqual(len(rows), 12)
        first = {(r["case"], r["condition"]): r for r in rows if r["stage"] == "first"}
        self.assertEqual(first["foundry", "csa"]["contract_errors"], 1)
        self.assertEqual(first["fabric", "baseline"]["text_findings"], 2)
        edit = next(r for r in rows if (r["case"], r["condition"], r["stage"]) == ("fabric", "csa", "edit"))
        self.assertIn("route-unchecked", edit["issue_codes"])
        self.assertTrue(all(r["measurement_errors"] == 0 and r["text_cells_measured"] > 0 for r in rows))

    def test_stale_measurements_rejected(self):
        score = self.scorer()
        original = score.__globals__["load_json"]
        def stale(path):
            result = original(path)
            if path.name.endswith(".text.json"):
                result["source_sha256"] = "0"*64
            return result
        with patch.dict(score.__globals__, {"load_json": stale}):
            with self.assertRaisesRegex(ValueError, "Stale browser measurements"):
                score()

    def test_trial_input_snapshot_is_preserved(self):
        metadata = json.loads((self.root / "run-metadata.json").read_text())
        archive = self.root / "input-snapshot.zip"
        self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(), metadata["input_snapshot_sha256"])
        with zipfile.ZipFile(archive) as snapshot:
            self.assertEqual(set(snapshot.namelist()), set(metadata["inputs_sha256"]))
            for name, digest in metadata["inputs_sha256"].items():
                self.assertEqual(hashlib.sha256(snapshot.read(name)).hexdigest(), digest)


if __name__ == "__main__":
    unittest.main()
