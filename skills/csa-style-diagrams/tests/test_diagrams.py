import base64
import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from csa_drawio import ASSET_ROOT, Diagram, icon_path, safe_svg
from check_diagram import check, digest
from render_diagram import render

PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII="
)


class DiagramTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="csa tests ")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.source = self.base / "architecture.drawio"
        self.png = self.base / "architecture.png"
        self.contract = self.base / "contract.json"
        self.drawing = Diagram("Synthetic test", 900, 600)
        self.drawing.component("a", "Source", 100, 100, workspace="W1", width=120)
        self.drawing.component("b", "Consumer", 500, 100, workspace="W2", width=150)
        self.drawing.connect("edge", "a", "b", kind="data", meaning="test data")
        self.drawing.save(self.source)
        self.contract.write_text(json.dumps({
            "nodes": {"a": {"workspace": "W1"}, "b": {"workspace": "W2"}},
            "edges": [{"source": "a", "target": "b", "kind": "data"}],
        }))

    def mutate(self, fn):
        doc = ET.parse(self.source)
        fn(doc)
        doc.write(self.source, encoding="utf-8")

    def codes(self, **kwargs):
        return {i["code"] for i in check(self.source, **kwargs)["issues"]}

    def test_clean_contract_and_reserved_ports(self):
        self.assertEqual(check(self.source, contract=self.contract), {"errors": 0, "warnings": 0, "issues": []})

    def test_duplicate_ids(self):
        self.mutate(lambda d: d.find(".//mxCell[@id='b']").set("id", "a"))
        self.assertIn("invalid-input", self.codes())

    def test_missing_and_nonvertex_endpoints(self):
        self.mutate(lambda d: d.find(".//mxCell[@id='edge']").set("target", "missing"))
        self.assertIn("missing-reference", self.codes())
        self.mutate(lambda d: d.find(".//mxCell[@id='edge']").set("target", "1"))
        self.assertIn("invalid-endpoint", self.codes())

    def test_parent_cycle(self):
        self.mutate(lambda d: d.find(".//mxCell[@id='a']").set("parent", "a-title"))
        self.assertIn("invalid-input", self.codes())

    def test_topology_direction_type_and_duplicates(self):
        self.mutate(lambda d: d.find(".//mxCell[@id='edge']").set("kind", "control"))
        self.assertIn("topology", self.codes(contract=self.contract))
        self.mutate(lambda d: d.find(".//mxCell[@id='edge']").set("source", "b"))
        self.assertIn("topology", self.codes(contract=self.contract))
        self.drawing.connect("duplicate", "a", "b", kind="data", meaning="duplicate")
        self.drawing.save(self.source)
        self.assertIn("topology", self.codes(contract=self.contract))

    def test_extra_components_and_ownership(self):
        self.drawing.component("extra", "Extra", 100, 350, workspace="W1")
        self.drawing.save(self.source)
        self.assertIn("component-inventory", self.codes(contract=self.contract))
        self.mutate(lambda d: d.find(".//mxCell[@id='a']").set("workspace", "wrong"))
        self.assertIn("workspace", self.codes(contract=self.contract))

    def test_scope_ownership_and_foundry_boundaries(self):
        drawing = Diagram("Foundry scopes", 1000, 650)
        drawing.boundary("resource", "Foundry", (40, 100, 920, 490), kind="resource")
        drawing.boundary("project", "Project", (80, 200, 360, 330), kind="project")
        drawing.component("agent", "Agent", 130, 300, scope="project:a")
        drawing.component("model", "Model", 650, 300, scope="resource")
        drawing.connect("request", "agent", "model", kind="data", meaning="inference")
        drawing.save(self.source)
        self.contract.write_text(json.dumps({
            "nodes": {"agent": {"scope": "project:a"}, "model": {"scope": "resource"}},
            "edges": [{"source": "agent", "target": "model", "kind": "data"}],
        }))
        self.assertEqual(check(self.source, contract=self.contract), {"errors": 0, "warnings": 0, "issues": []})
        self.mutate(lambda d: d.find(".//mxCell[@id='agent']").set("scope", "wrong"))
        self.assertIn("scope", self.codes(contract=self.contract))
        drawing.save(self.source)
        self.mutate(lambda d: d.find(".//mxCell[@id='agent']").set("workspace", "wrong"))
        self.assertIn("ownership", self.codes(contract=self.contract))

    def test_ownership_requires_exactly_one_nonempty_field(self):
        for kwargs in ({}, {"workspace": ""}, {"scope": " "}, {"scope": 1},
                       {"workspace": "W", "scope": "P"}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                self.drawing.component("invalid", "Invalid", 100, 350, **kwargs)
        for node in ({}, {"scope": ""}, {"scope": None}, {"scope": "P", "workspace": "W"}):
            self.contract.write_text(json.dumps({"nodes": {"a": node}, "edges": []}))
            self.assertIn("invalid-input", self.codes(contract=self.contract))

    def test_all_curated_icons_have_valid_local_hashes_and_svg(self):
        catalog = json.loads((ASSET_ROOT / "catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(len(catalog["icons"]), 13)
        for name in catalog["icons"]:
            with self.subTest(name=name):
                self.assertTrue(icon_path(name).is_file())
        with self.assertRaisesRegex(ValueError, "Unknown icon"):
            icon_path("not-a-real-icon")

    def test_icon_lookup_refuses_bad_paths_missing_files_and_modified_bytes(self):
        svg = b'<svg xmlns="http://www.w3.org/2000/svg"><rect width="20" height="20"/></svg>'
        path = self.base / "icon.svg"
        path.write_bytes(svg)
        entry = {"path": "icon.svg", "sha256": hashlib.sha256(svg).hexdigest()}
        def write_catalog():
            (self.base / "catalog.json").write_text(json.dumps({
                "schema_version": 1, "icons": {"test": entry}}))
        with patch("csa_drawio.ASSET_ROOT", self.base):
            write_catalog()
            self.assertEqual(icon_path("test"), path.resolve())
            for unsafe in ("../escape.svg", "/absolute.svg", "C:/absolute.svg",
                           r"icons\escape.svg", "https://example.invalid/icon.svg", "not-svg.png"):
                entry["path"] = unsafe
                write_catalog()
                with self.subTest(path=unsafe), self.assertRaises(ValueError):
                    icon_path("test")
            entry["path"] = "missing.svg"
            write_catalog()
            with self.assertRaises(FileNotFoundError):
                icon_path("test")
            entry["path"] = "icon.svg"
            write_catalog()
            path.write_bytes(svg + b"\n")
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                icon_path("test")
            path.write_bytes(b'<svg xmlns="http://www.w3.org/2000/svg"><script>bad()</script></svg>')
            entry["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
            write_catalog()
            with self.assertRaises(ValueError):
                icon_path("test")

    def test_icon_lookup_refuses_resolved_escape(self):
        (self.base / "catalog.json").write_text(json.dumps({
            "schema_version": 1, "icons": {"test": {"path": "icon.svg", "sha256": "0"*64}}}))
        original_resolve = Path.resolve
        outside = self.base.parent / "outside.svg"
        def resolve(path):
            return outside if path == self.base / "icon.svg" else original_resolve(path)
        # Model a symlink escape without requiring Windows symlink privileges.
        with patch("csa_drawio.ASSET_ROOT", self.base), patch.object(Path, "resolve", resolve):
            with self.assertRaisesRegex(ValueError, "under its asset directory"):
                icon_path("test")

    def test_label_overlap(self):
        self.drawing.text("one", "One", (100, 350, 100, 30))
        self.drawing.text("two", "Two", (130, 360, 100, 30))
        self.drawing.save(self.source)
        self.assertIn("label-overlap", self.codes())

    def test_route_through_unrelated_symbol_and_label(self):
        self.drawing.component("block", "Block", 300, 100, width=100, workspace="W1")
        self.drawing.save(self.source)
        report = check(self.source)
        self.assertTrue(any("block-symbol" in i["message"] for i in report["issues"]))
        self.assertIn("route-collision", self.codes())

    def test_floating_group_port_and_bottom_guard(self):
        self.drawing.component("service", "Caption", 300, 200, workspace="W2", symbol="note")
        self.drawing.save(self.source)
        def move(d):
            edge = d.find(".//mxCell[@id='edge']")
            edge.set("source", "service")
            edge.set("style", edge.get("style").replace("exitX=1.0", "exitX=0.5")
                     .replace("exitY=0.5", "exitY=1.0"))
        self.mutate(move)
        self.assertIn("floating-port", self.codes())
        with self.assertRaises(ValueError):
            self.drawing.port("service", "bottom")

    def test_route_through_its_own_caption_is_not_exempt(self):
        self.drawing.component("service", "Caption", 300, 200, workspace="W2",
                               symbol="note", caption="Reserved caption")
        self.drawing.save(self.source)
        def cross_caption(doc):
            edge = doc.find(".//mxCell[@id='edge']")
            edge.set("source", "service")
            edge.set("style", edge.get("style").replace("exitX=1.0", "exitX=0.5")
                     .replace("exitY=0.5", f"exitY={56/144}"))
            points = ET.SubElement(edge.find("mxGeometry"), "Array", {"as": "points"})
            for x, y in ((375, 390), (450, 390), (450, 145)):
                ET.SubElement(points, "mxPoint", x=str(x), y=str(y))
        self.mutate(cross_caption)
        issues = check(self.source)["issues"]
        self.assertTrue(any(i["code"] == "route-collision" and "service-caption" in i["message"]
                            for i in issues))

    def test_explicit_routes_cannot_be_diagonal(self):
        with self.assertRaises(ValueError):
            self.drawing.connect("diagonal", "a", "b", kind="data", meaning="", via=((350, 160),))

    def test_unknown_renderer_routing_is_not_silently_checked(self):
        self.mutate(lambda d: d.find(".//mxCell[@id='edge']").set("style", "edgeStyle=orthogonalEdgeStyle;"))
        self.assertIn("route-unchecked", self.codes())
        self.drawing.save(self.source)
        self.mutate(lambda d: d.find(".//mxCell[@id='edge']").set(
            "style", d.find(".//mxCell[@id='edge']").get("style") + "curved=1;"))
        self.assertIn("route-unchecked", self.codes())

    def test_nonfinite_and_relative_geometry(self):
        self.mutate(lambda d: d.find(".//mxCell[@id='a']/mxGeometry").set("x", "nan"))
        self.assertIn("invalid-input", self.codes())
        self.drawing.save(self.source)
        self.mutate(lambda d: d.find(".//mxCell[@id='a']/mxGeometry").set("relative", "1"))
        self.assertIn("invalid-input", self.codes())

    def test_page_and_mode_warnings(self):
        self.drawing.text("outside", "Outside", (880, 400, 100, 30))
        self.drawing.save(self.source)
        self.assertIn("outside-page", self.codes())
        self.assertIn("small-text", self.codes(mode="presentation"))

    def test_presentation_components_raise_their_default_font_sizes(self):
        drawing = Diagram("Presentation", 900, 600, mode="presentation")
        drawing.component("item", "Readable", 200, 200, workspace="W1", caption="Caption", symbol="note")
        drawing.save(self.source)
        self.assertEqual(check(self.source)["warnings"], 0)

    def test_empty_canvas_is_not_a_valid_architecture(self):
        Diagram("Empty", 900, 600).save(self.source)
        self.assertIn("invalid-input", self.codes())

    def test_compressed_multiple_and_wrapped_pages_rejected(self):
        self.source.write_text('<mxfile><diagram>compressed</diagram></mxfile>')
        self.assertIn("invalid-input", self.codes())
        self.drawing.save(self.source)
        self.mutate(lambda d: ET.SubElement(d.getroot(), "diagram", id="second"))
        self.assertIn("invalid-input", self.codes())
        self.drawing.save(self.source)
        self.mutate(lambda d: ET.SubElement(d.find(".//root"), "object", id="wrapped"))
        self.assertIn("invalid-input", self.codes())

    def test_external_image_rejected(self):
        self.mutate(lambda d: d.find(".//mxCell[@id='a-symbol']").set("style", "image=https://example.invalid/icon.svg;"))
        self.assertIn("image-format", self.codes())

    def test_svg_embedding_and_active_content(self):
        svg = self.base / "icon.svg"
        svg.write_text('<svg xmlns="http://www.w3.org/2000/svg"><rect width="20" height="20"/></svg>')
        self.drawing.component("icon", "Icon", 100, 350, workspace="W1", svg=svg)
        self.drawing.save(self.source)
        self.assertEqual(check(self.source)["errors"], 0)
        for content in ('<script>bad()</script>', '<image href="https://example.invalid/a"/>',
                        '<rect onload="bad()"/>', '<style>@import "x";</style>'):
            with self.subTest(content=content), self.assertRaises(ValueError):
                safe_svg(f'<svg xmlns="http://www.w3.org/2000/svg">{content}</svg>'.encode())
        safe_svg(b'<svg xmlns="http://www.w3.org/2000/svg"><rect fill="url(#gradient)"/></svg>')
        safe_svg(b"""<svg xmlns="http://www.w3.org/2000/svg"><rect fill="url('#gradient')"/></svg>""")

    def stamp(self):
        self.png.write_bytes(PNG)
        self.png.with_suffix(".render.json").write_text(json.dumps({
            "source_sha256": digest(self.source), "png_sha256": digest(self.png)}))

    def test_preview_hashes_not_modification_time(self):
        self.stamp()
        self.assertEqual(check(self.source, preview=self.png)["errors"], 0)
        self.source.write_bytes(self.source.read_bytes() + b"\n")
        self.assertIn("stale-preview", self.codes(preview=self.png))
        self.stamp()
        self.png.write_bytes(PNG + b"changed")
        self.assertIn("stale-preview", self.codes(preview=self.png))

    def test_missing_or_malformed_preview_and_contract(self):
        self.assertIn("invalid-input", self.codes(preview=self.png))
        for invalid in ("[]", '{"nodes":{},"nodes":{}}', '{"nodes":{},"edges":null}',
                        '{"nodes":{"a":{"workspace":null}},"edges":[]}'):
            self.contract.write_text(invalid)
            self.assertIn("invalid-input", self.codes(contract=self.contract))
        self.stamp()
        self.png.with_suffix(".render.json").write_text("[]")
        self.assertIn("invalid-input", self.codes(preview=self.png))
        self.png.write_bytes(b"not a PNG")
        self.assertIn("invalid-input", self.codes(preview=self.png))

    def test_explicit_label_slot_required(self):
        with self.assertRaises(ValueError):
            self.drawing.connect("labelled", "a", "b", kind="data", meaning="", label="Data")

    def test_strict_cli_exit(self):
        self.drawing.text("small", "Small", (100, 400, 100, 20), size=10)
        self.drawing.save(self.source)
        tool = Path(__file__).resolve().parents[1] / "scripts" / "check_diagram.py"
        for strict, expected in (([], 0), (["--strict"], 1)):
            run = subprocess.run([sys.executable, "-B", str(tool), str(self.source), *strict],
                                 capture_output=True, text=True)
            self.assertEqual(run.returncode, expected, run.stderr)

    def test_render_explicit_executable_and_provenance(self):
        exe = self.base / "local drawio.exe"
        exe.touch()
        def export(args, **kwargs):
            self.assertEqual(args[0], str(exe.resolve()))
            self.assertNotIn("shell", kwargs)
            Path(args[-2]).write_bytes(PNG)
        with patch("render_diagram.subprocess.run", side_effect=export):
            render(self.source, exe, self.png)
        self.assertEqual(check(self.source, preview=self.png)["errors"], 0)
        with self.assertRaises(ValueError):
            render(self.source, exe, self.png)

    def test_render_failure_or_concurrent_edit_preserves_old_output(self):
        exe = self.base / "local drawio.exe"
        exe.touch()
        self.stamp()
        before = self.png.read_bytes()
        with patch("render_diagram.subprocess.run", side_effect=subprocess.CalledProcessError(1, ["drawio"])):
            with self.assertRaises(subprocess.CalledProcessError):
                render(self.source, exe, self.png, overwrite=True)
        self.assertEqual(self.png.read_bytes(), before)
        def changed(args, **kwargs):
            Path(args[-2]).write_bytes(PNG)
            self.source.write_bytes(self.source.read_bytes() + b"\n")
        with patch("render_diagram.subprocess.run", side_effect=changed):
            with self.assertRaisesRegex(ValueError, "changed during"):
                render(self.source, exe, self.png, overwrite=True)
        self.assertEqual(self.png.read_bytes(), before)

    def test_packaged_example_and_generator_agree(self):
        for folder in ("fabric-batch", "foundry-icons", "fabric-official", "foundry-multi-project"):
            with self.subTest(folder=folder):
                example = Path(__file__).resolve().parents[1] / "examples" / folder
                report = check(example / "architecture.drawio", contract=example / "contract.json",
                               preview=example / "architecture.png", clarity=True)
                self.assertEqual(report, {"errors": 0, "warnings": 0, "issues": []})
                measurement = example / "architecture.text.json"
                if measurement.exists():
                    recorded = json.loads(measurement.read_text())
                    self.assertEqual(recorded["source_sha256"], digest(example / "architecture.drawio"))
                    self.assertEqual((recorded["errors"], recorded["warnings"]), (0, 0))
                build = runpy.run_path(str(example / "build.py"))["build"]
                output = self.base / folder
                build(output)
                for name in ("architecture.drawio", "contract.json"):
                    self.assertEqual((example / name).read_bytes(), (output / name).read_bytes())
                with self.assertRaises(ValueError):
                    build(output)


if __name__ == "__main__":
    unittest.main()
