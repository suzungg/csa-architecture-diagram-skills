"""Small native draw.io primitives; Python 3.10+, no renderer or downloads."""
import base64
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import re
import xml.etree.ElementTree as ET

MODES = {"reference": 14, "presentation": 20, "recreate": 0}
ASSET_ROOT = Path(__file__).resolve().parents[1] / "assets" / "foundry"
PORTS = {"left": (0, .5), "right": (1, .5), "top": (.5, 0),
         "bottom": (.5, 1), "right-low": (1, .75), "left-low": (0, .75)}


def icon_path(name, *, family="foundry"):
    """Resolve a curated official icon locally; never download or substitute."""
    if family not in {"foundry", "fabric"}:
        raise ValueError(f"Unknown icon family: {family}")
    asset_root = ASSET_ROOT if family == "foundry" else ASSET_ROOT.parent / family
    catalog = json.loads((asset_root / "catalog.json").read_text(encoding="utf-8"))
    if not isinstance(catalog, dict) or catalog.get("schema_version") != 1 or not isinstance(catalog.get("icons"), dict):
        raise ValueError("Invalid Foundry icon catalog")
    if name not in catalog["icons"]:
        raise ValueError(f"Unknown icon {name!r}; available: {', '.join(sorted(catalog['icons']))}")
    entry = catalog["icons"][name]
    if not isinstance(entry, dict) or not isinstance(entry.get("path"), str) or not isinstance(entry.get("sha256"), str):
        raise ValueError(f"Invalid icon entry: {name}")
    relative = PurePosixPath(entry["path"])
    if relative.is_absolute() or ".." in relative.parts or "\\" in entry["path"] or ":" in entry["path"]:
        raise ValueError(f"Unsafe icon path: {name}")
    path = (asset_root / relative).resolve()
    if not path.is_relative_to(asset_root.resolve()) or path.suffix.lower() != ".svg":
        raise ValueError(f"Icon must be a local SVG under its asset directory: {name}")
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != entry["sha256"]:
        raise ValueError(f"Icon hash mismatch: {name}; review the source rather than substituting")
    safe_svg(data)
    return path


def safe_svg(data):
    """Reject active content and external dependencies; not a full SVG sanitizer."""
    root = ET.fromstring(data)
    if root.tag != "{http://www.w3.org/2000/svg}svg":
        raise ValueError("Expected an SVG document with the SVG namespace")
    for element in root.iter():
        if element.tag.split("}")[-1].lower() in {"script", "foreignobject"}:
            raise ValueError("Active SVG content is not supported")
        for key, value in element.attrib.items():
            name = key.split("}")[-1].lower()
            if name.startswith("on") or (name in {"href", "src"} and not value.startswith("#")):
                raise ValueError("SVG event handlers and external references are not supported")
    text = data.decode("utf-8")
    urls = re.findall(r"url\((.*?)\)", text, re.I | re.S)
    if re.search(r"@import", text, re.I) or any(
        not value.strip().strip("'\"").startswith("#") for value in urls
    ):
        raise ValueError("SVG styles must not load external resources")
    return data


class Diagram:
    """Absolute placement, reserved caption slots, explicit orthogonal routes.

    Symbols are neutral native shapes unless the caller supplies an approved
    self-contained SVG. This helper chooses neither services nor topology.
    """

    def __init__(self, title, width, height, mode="reference"):
        if mode not in MODES or not all(math.isfinite(n) and n > 0 for n in (width, height)):
            raise ValueError("Use a supported output mode and positive finite canvas dimensions")
        self.doc = ET.Element("mxfile", host="csa-style-diagrams")
        page = ET.SubElement(self.doc, "diagram", id="architecture", name=title)
        model = ET.SubElement(page, "mxGraphModel", page="1", pageScale="1",
                              pageWidth=str(width), pageHeight=str(height),
                              background="#FFFFFF", csaMode=mode)
        self.root = ET.SubElement(model, "root")
        ET.SubElement(self.root, "mxCell", id="0")
        ET.SubElement(self.root, "mxCell", id="1", parent="0")
        self.cells = {"0", "1"}
        self.nodes = {}
        self.label_size = max(18, MODES[mode])
        self.caption_size = max(14, MODES[mode])
        self.shape("canvas", "", (0, 0, width, height),
                   "fillColor=#FFFFFF;strokeColor=none;", role="canvas")

    def shape(self, id, label, rect, style, *, parent="1", role="symbol"):
        if id in self.cells or parent not in self.cells:
            raise ValueError(f"Duplicate ID or missing parent: {id} / {parent}")
        x, y, w, h = rect
        if not all(math.isfinite(n) for n in rect) or w <= 0 or h <= 0:
            raise ValueError(f"Invalid geometry: {id}")
        cell = ET.SubElement(self.root, "mxCell", id=id, parent=parent, value=label,
                             vertex="1", csaRole=role,
                             style="fontFamily=Arial;fontColor=#26333F;" + style)
        ET.SubElement(cell, "mxGeometry", x=str(x), y=str(y), width=str(w),
                      height=str(h), **{"as": "geometry"})
        self.cells.add(id)
        return cell

    def text(self, id, label, rect, *, size=None, bold=False, align="left",
             color="#26333F", parent="1"):
        size = self.label_size if size is None else size
        return self.shape(
            id, label, rect,
            f"text;html=0;whiteSpace=wrap;spacing=0;align={align};verticalAlign=middle;"
            f"fontSize={size};fontStyle={int(bold)};fontColor={color};",
            parent=parent, role="label",
        )

    def boundary(self, id, title, rect, *, kind, number=None, title_width=None):
        if kind not in {"logical", "workspace", "tenant", "network", "environment", "resource", "project"}:
            raise ValueError("Boundary kind must declare its meaning")
        _, _, w, _ = rect
        cell = self.shape(id, "", rect, "fillColor=#FBFCFD;strokeColor=#A2BBD0;",
                          role="boundary")
        cell.set("boundaryKind", kind)
        self.shape(id + "-header", "", (0, 0, w, 44),
                   "fillColor=#0078D4;strokeColor=none;", parent=id, role="header")
        left = 46 if number is not None else 14
        # A bounded text slot, not measured glyph extents; inspect the export.
        width = title_width if title_width is not None else min(w-left-14, len(title)*15+12)
        self.text(id + "-title", title, (left, 6, width, 32), size=22,
                  bold=True, color="#FFFFFF", parent=id)
        if number is not None:
            self.shape(id + "-number", str(number), (8, 8, 28, 28),
                       "ellipse;fillColor=#16813B;strokeColor=#FFFFFF;"
                       f"fontColor=#FFFFFF;fontSize={self.label_size};align=center;",
                       parent=id, role="badge")
        return cell

    def component(self, id, title, x, y, *, workspace=None, scope=None, caption="", width=150,
                  symbol="process", svg=None):
        if (workspace is None) == (scope is None):
            raise ValueError("Specify exactly one ownership field: workspace or scope")
        owner_key, owner = ("workspace", workspace) if scope is None else ("scope", scope)
        if not isinstance(owner, str) or not owner.strip():
            raise ValueError("Ownership must be a nonempty string")
        if symbol not in {"process", "cylinder", "note", "document", "ellipse"}:
            raise ValueError(f"Unsupported neutral symbol: {symbol}")
        process = symbol == "process" and svg is None
        large = self.caption_size >= 20
        height = (112 if large else 90) if process else (166 if large else 144)
        cell = self.shape(id, "", (x, y, width, height),
                          "group;fillColor=none;strokeColor=none;", role="component")
        cell.set(owner_key, owner)
        symbol_rect = (0, 0, width, height) if process else ((width-56)/2, 0, 56, 56)
        if svg is not None:
            data = safe_svg(Path(svg).read_bytes())
            encoded = base64.b64encode(data).decode("ascii")
            style = f"shape=image;imageAspect=1;image=data:image/svg+xml,{encoded};"
        else:
            shape = "rectangle" if process else symbol
            style = f"shape={shape};fillColor=#F0F5F8;strokeColor=#526675;strokeWidth=1.5;"
        self.shape(id + "-symbol", "", symbol_rect, style, parent=id)
        if process:
            self.text(id + "-title", title, (8, 8, width-16, 52 if large else 44), bold=True,
                      align="center", parent=id + "-symbol")
            self.text(id + "-caption", caption, (8, 72 if large else 58, width-16, 32 if large else 22), size=self.caption_size,
                      align="center", parent=id + "-symbol")
        else:
            self.text(id + "-title", title, (0, 70, width, 52 if large else 44), bold=True,
                      align="center", parent=id)
            self.text(id + "-caption", caption, (0, 132 if large else 120, width, 32 if large else 22), size=self.caption_size,
                      align="center", color="#4A5968", parent=id)
        self.nodes[id] = ((x, y, width, height), symbol_rect, process)
        return cell

    def port(self, id, side):
        rect, symbol, process = self.nodes[id]
        if side not in PORTS or (side == "bottom" and not process):
            raise ValueError(f"{id}: choose a port clear of its below-symbol caption")
        sx, sy = PORTS[side]
        px, py = symbol[0]+sx*symbol[2], symbol[1]+sy*symbol[3]
        return (px/rect[2], py/rect[3]), (rect[0]+px, rect[1]+py)

    def connect(self, id, source, target, *, kind, meaning, via=(),
                start="right", end="left", label="", label_rect=None, intent=None):
        if id in self.cells or kind not in {"data", "control", "telemetry", "association"}:
            raise ValueError(f"Duplicate edge ID or unsupported relationship kind: {id}")
        if label and label_rect is None:
            raise ValueError("Visible edge labels need an explicit reserved rectangle")
        intents = {"runtime": "data", "association": "association", "control": "control", "telemetry": "telemetry"}
        if intent is not None and (intent not in intents or intents[intent] != kind):
            raise ValueError("Relationship intent must match its declared kind")
        p, a = self.port(source, start)
        q, b = self.port(target, end)
        points = [a, *via, b]
        for u, v in zip(points, points[1:]):
            if not all(math.isfinite(n) for n in (*u, *v)):
                raise ValueError(f"Nonfinite route: {id}")
            if not (math.isclose(u[0], v[0], abs_tol=1e-6) or
                    math.isclose(u[1], v[1], abs_tol=1e-6)):
                raise ValueError(f"Route must be explicitly orthogonal: {id}: {u} -> {v}")
        control = kind == "control"
        cell = ET.SubElement(
            self.root, "mxCell", id=id, parent="1", edge="1", source=source,
            target=target, kind=kind, meaning=meaning,
            style=f"noEdgeStyle=1;rounded=0;endArrow={'none' if kind == 'association' else 'block'};"
            f"endFill={0 if kind == 'association' else 1};strokeWidth=1.8;"
            f"strokeColor={'#087E8B' if control else '#354552'};dashed={int(control or kind == 'association')};"
            f"exitX={p[0]};exitY={p[1]};entryX={q[0]};entryY={q[1]};"
            "exitPerimeter=0;entryPerimeter=0;jumpStyle=arc;jumpSize=8;",
        )
        if intent is not None:
            cell.set("intent", intent)
        geo = ET.SubElement(cell, "mxGeometry", relative="1", **{"as": "geometry"})
        if via:
            array = ET.SubElement(geo, "Array", **{"as": "points"})
            for x, y in via:
                ET.SubElement(array, "mxPoint", x=str(x), y=str(y))
        self.cells.add(id)
        if label:
            self.text(id + "-label", label, label_rect, size=self.caption_size)
        return cell

    def save(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        ET.indent(self.doc, space="  ")
        ET.ElementTree(self.doc).write(path, encoding="utf-8", xml_declaration=True)
