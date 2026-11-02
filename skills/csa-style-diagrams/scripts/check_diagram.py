"""Offline checks for one uncompressed draw.io page. Warnings require review."""
import argparse
import base64
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import struct
import sys
import xml.etree.ElementTree as ET

from csa_drawio import MODES, safe_svg


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=unique_object)


def png_size(path):
    data = Path(path).read_bytes()
    if len(data) < 33 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError("Expected a nonempty PNG export")
    width, height = struct.unpack(">II", data[16:24])
    if not width or not height:
        raise ValueError("PNG dimensions must be positive")
    return width, height


def style_of(cell):
    return dict(part.split("=", 1) for part in cell.get("style", "").split(";") if "=" in part)


def number(value):
    value = float(value)
    if not math.isfinite(value):
        raise ValueError("Nonfinite geometry")
    return value


def overlap(a, b):
    return (min(a[0]+a[2], b[0]+b[2])-max(a[0], b[0]) > 1e-6 and
            min(a[1]+a[3], b[1]+b[3])-max(a[1], b[1]) > 1e-6)


def through(a, b, rect):
    x, y, w, h = rect
    if abs(a[1]-b[1]) < 1e-6:
        return y+1e-6 < a[1] < y+h-1e-6 and min(max(a[0], b[0]), x+w)-max(min(a[0], b[0]), x) > 1e-6
    if abs(a[0]-b[0]) < 1e-6:
        return x+1e-6 < a[0] < x+w-1e-6 and min(max(a[1], b[1]), y+h)-max(min(a[1], b[1]), y) > 1e-6
    return False


def on_border(point, rect):
    x, y, w, h = rect
    px, py = point
    return (x-1e-6 <= px <= x+w+1e-6 and y-1e-6 <= py <= y+h+1e-6 and
            min(abs(px-x), abs(px-x-w), abs(py-y), abs(py-y-h)) < 1e-6)


def contains(outer, inner):
    return (outer[0]-1e-6 <= inner[0] and outer[1]-1e-6 <= inner[1]
            and inner[0]+inner[2] <= outer[0]+outer[2]+1e-6
            and inner[1]+inner[3] <= outer[1]+outer[3]+1e-6)


def check_scopes(spec, ids, bounds, issue):
    scopes = spec["scopes"]
    if not isinstance(scopes, dict) or not scopes:
        raise ValueError("scopes must be a nonempty object")
    for name, scope in scopes.items():
        if not name.strip() or not isinstance(scope, dict) or "boundary" not in scope:
            raise ValueError("Each named scope needs a boundary ID or explicit null")
        if scope.get("parent") is not None and not isinstance(scope["parent"], str):
            raise ValueError("Scope parent must be an ID or null")
        if scope["boundary"] is not None and not isinstance(scope["boundary"], str):
            raise ValueError("Scope boundary must be an ID or null")
    chains, assigned = {}, set()
    for name, scope in scopes.items():
        chain, current = [], name
        while current is not None:
            if current not in scopes or current in chain:
                raise ValueError("Missing or cyclic scope parent")
            chain.append(current)
            current = scopes[current].get("parent")
        chains[name] = chain
        boundary = scope["boundary"]
        if boundary is None:
            continue
        if boundary not in bounds or ids[boundary].get("csaRole") != "boundary" or boundary in assigned:
            raise ValueError("Scope must name a unique boundary vertex")
        assigned.add(boundary)
        if ids[boundary].get("boundaryKind") != scope.get("kind"):
            issue("error", "scope-kind", f"{name}: declared boundary kind differs")
    for name, scope in scopes.items():
        parent = scope.get("parent")
        if parent is not None and scope["boundary"] is not None:
            outer = scopes[parent]["boundary"]
            if outer is None or not contains(bounds[outer], bounds[scope["boundary"]]):
                issue("error", "scope-parent", f"{name}: boundary is not inside its declared parent")
    for id, node in spec["nodes"].items():
        owner = node.get("scope", node.get("workspace"))
        if owner not in scopes:
            raise ValueError(f"{id}: owner is missing from scopes")
        if id not in bounds:
            continue
        boundary = scopes[owner]["boundary"]
        if boundary is not None and not contains(bounds[boundary], bounds[id]):
            issue("error", "scope-containment", f"{id}: outside declared owner {owner}")
        for name, scope in scopes.items():
            other = scope["boundary"]
            if other is not None and name not in chains[owner] and contains(bounds[other], bounds[id]):
                issue("error", "scope-conflict", f"{id}: drawn inside unrelated scope {name}")


def route_clarity(routes, issue):
    for i, (a_id, a_points, a_style) in enumerate(routes):
        for b_id, b_points, b_style in routes[i+1:]:
            codes = set()
            for a, b in zip(a_points, a_points[1:]):
                for c, d in zip(b_points, b_points[1:]):
                    horizontal_a, horizontal_b = abs(a[1]-b[1]) < 1e-6, abs(c[1]-d[1]) < 1e-6
                    if horizontal_a == horizontal_b:
                        axis = 0 if horizontal_a else 1
                        if abs(a[1-axis]-c[1-axis]) < 1e-6:
                            length = min(max(a[axis], b[axis]), max(c[axis], d[axis])) - max(min(a[axis], b[axis]), min(c[axis], d[axis]))
                            if length > 1e-6:
                                codes.add("route-overlap")
                    else:
                        h1, h2, v1, v2 = (a, b, c, d) if horizontal_a else (c, d, a, b)
                        if (min(h1[0], h2[0])+1e-6 < v1[0] < max(h1[0], h2[0])-1e-6
                                and min(v1[1], v2[1])+1e-6 < h1[1] < max(v1[1], v2[1])-1e-6
                                and not any(s.get("jumpStyle") in {"arc", "gap"} for s in (a_style, b_style))):
                            codes.add("ambiguous-crossing")
            for code in sorted(codes):
                issue("warning", code, f"{a_id} / {b_id}: review shared lanes or mark a no-junction crossing")


def check(source, *, contract=None, preview=None, mode=None, clarity=False):
    issues = []

    def issue(level, code, message):
        issues.append({"level": level, "code": code, "message": message})

    def result():
        return {"errors": sum(i["level"] == "error" for i in issues),
                "warnings": sum(i["level"] == "warning" for i in issues), "issues": issues}

    try:
        doc = ET.parse(source)
        models = list(doc.iter("mxGraphModel"))
        if len(models) != 1 or len(list(doc.iter("diagram"))) > 1:
            raise ValueError("Use one uncompressed draw.io page; compressed/multipage input is not checked")
        model = models[0]
        root = model.find("root")
        if root is None:
            raise ValueError("Missing mxGraphModel/root")
        # Object wrappers carry IDs outside mxCell; refusing is safer than omitting them.
        if any(c.tag != "mxCell" for c in root):
            raise ValueError("Object-wrapped cells are not supported; use plain uncompressed mxCell input")
        cells = list(root)
        ids = {c.get("id"): c for c in cells}
        if None in ids or len(ids) != len(cells):
            raise ValueError("Missing or duplicate mxCell IDs")
        if not {"0", "1"} <= ids.keys():
            raise ValueError("Missing draw.io root/layer IDs")
        if not any(c.get("vertex") == "1" and c.get("csaRole") != "canvas" for c in cells):
            raise ValueError("Diagram contains no visible content beyond its canvas")
        for id, cell in ids.items():
            for attr in ("parent", "source", "target"):
                if cell.get(attr) is not None and cell.get(attr) not in ids:
                    issue("error", "missing-reference", f"{id}: {attr}={cell.get(attr)}")
            if cell.get("edge") == "1":
                for attr in ("source", "target"):
                    endpoint = ids.get(cell.get(attr))
                    if endpoint is None or endpoint.get("vertex") != "1":
                        issue("error", "invalid-endpoint", f"{id}: {attr} must reference a vertex")
            if id != "0" and cell.get("parent") is None:
                issue("error", "missing-parent", id)
        if result()["errors"]:
            return result()

        ancestors = {}
        for id in ids:
            chain = []
            p = ids[id].get("parent")
            while p is not None:
                if p == id or p in chain:
                    raise ValueError(f"Cyclic parent references: {id}")
                chain.append(p)
                p = ids[p].get("parent")
            ancestors[id] = chain

        edges = [c for c in cells if c.get("edge") == "1"]
        nodes = {id for id, c in ids.items() if c.get("csaRole") == "component"}
        spec = None
        if contract is not None:
            spec = load_json(contract)
            if not isinstance(spec, dict) or not isinstance(spec.get("nodes"), dict) or not isinstance(spec.get("edges"), list):
                raise ValueError("Contract needs a nodes object and edges array")
            wanted = set(spec["nodes"])
            if nodes and nodes != wanted:
                issue("error", "component-inventory", f"Missing/extra marked components: {sorted(nodes ^ wanted)}")
            nodes = wanted
            for id, node in spec["nodes"].items():
                if not id.strip() or not isinstance(node, dict):
                    raise ValueError("Contract nodes need nonempty IDs and ownership objects")
                ownership = [key for key in ("workspace", "scope") if key in node]
                if len(ownership) != 1 or not isinstance(node[ownership[0]], str) or not node[ownership[0]].strip():
                    raise ValueError("Contract nodes need exactly one nonempty workspace or scope")
                owner_key = ownership[0]
                if id not in ids or ids[id].get("vertex") != "1":
                    issue("error", "missing-component", id)
                elif ids[id].get(owner_key) != node[owner_key]:
                    issue("error", owner_key, f"{id}: differs from contract")
                elif ids[id].get("scope" if owner_key == "workspace" else "workspace") is not None:
                    issue("error", "ownership", f"{id}: cannot be both a workspace and a scope")
            expected = []
            for e in spec["edges"]:
                if (e["source"] not in wanted or e["target"] not in wanted
                        or not isinstance(e["kind"], str) or not e["kind"].strip()):
                    raise ValueError("Invalid contract edge")
                expected.append((e["source"], e["target"], e["kind"]))
            intentions = [e for e in spec["edges"] if "intent" in e]
            if intentions:
                kinds = {"runtime": "data", "association": "association", "control": "control", "telemetry": "telemetry"}
                for e in intentions:
                    if e["intent"] not in kinds or kinds[e["intent"]] != e["kind"]:
                        raise ValueError("Contract intent disagrees with relationship kind")
                wanted_intents = Counter((e["source"], e["target"], e["kind"], e["intent"]) for e in intentions)
                actual_intents = Counter((c.get("source"), c.get("target"), c.get("kind"), c.get("intent"))
                                         for c in edges if c.get("intent") is not None)
                if actual_intents != wanted_intents:
                    issue("error", "relationship-intent", "Explicit relationship intents differ from contract")
                for c in edges:
                    style = style_of(c)
                    if c.get("intent") == "association" and (style.get("dashed") != "1" or style.get("endArrow") != "none"):
                        issue("warning", "association-style", f"{c.get('id')}: association should be dashed and arrowless")
            actual = Counter((c.get("source"), c.get("target"), c.get("kind")) for c in edges)
            if actual != Counter(expected):
                issue("error", "topology", "Directed relationship inventory/types differ from contract")

        chosen_mode = mode or model.get("csaMode")
        if chosen_mode not in MODES:
            issue("warning", "output-mode", "Specify reference, presentation or recreate to check font floors")
        width, height = number(model.get("pageWidth", "0")), number(model.get("pageHeight", "0"))
        if width <= 0 or height <= 0:
            raise ValueError("Set positive pageWidth/pageHeight")
        bounds = {}

        def rectangle(id):
            if id in bounds:
                return bounds[id]
            if id in {"0", "1"}:
                return (0, 0, 0, 0)
            cell = ids[id]
            geo = cell.find("mxGeometry")
            if geo is None:
                raise ValueError(f"Missing vertex geometry: {id}")
            transform = style_of(cell)
            if geo.get("relative") == "1" or any(transform.get(k, "0") != "0" for k in ("rotation", "flipH", "flipV")):
                raise ValueError(f"Relative/rotated/flipped vertex geometry is not supported: {id}")
            parent = rectangle(cell.get("parent"))
            x, y, w, h = (number(geo.get(key, "0")) for key in ("x", "y", "width", "height"))
            if w <= 0 or h <= 0:
                raise ValueError(f"Nonpositive vertex dimensions: {id}")
            bounds[id] = (parent[0]+x, parent[1]+y, w, h)
            return bounds[id]

        protected = {}
        labels = set()
        symbols = set()
        for id, cell in ids.items():
            if cell.get("vertex") != "1":
                continue
            rect = rectangle(id)
            style = style_of(cell)
            if rect[0] < 0 or rect[1] < 0 or rect[0]+rect[2] > width+1e-6 or rect[1]+rect[3] > height+1e-6:
                issue("warning", "outside-page", id)
            image = style.get("image")
            if image is not None:
                if not image.startswith("data:image/svg+xml,"):
                    issue("error", "image-format", f"{id}: only self-contained embedded SVG images are checked")
                else:
                    safe_svg(base64.b64decode(image.split(",", 1)[1], validate=True))
            role = cell.get("csaRole")
            if cell.get("value"):
                labels.add(id)
                if chosen_mode in MODES and number(style.get("fontSize", "12")) < MODES[chosen_mode]:
                    issue("warning", "small-text", f"{id}: below {MODES[chosen_mode]} units for {chosen_mode}")
            if role in {"canvas", "boundary", "header", "component"} or "group;" in cell.get("style", ""):
                continue
            protected[id] = rect
            if role == "symbol":
                symbols.add(id)
        if spec is not None and "scopes" in spec:
            check_scopes(spec, ids, bounds, issue)
        for i, a in enumerate(protected):
            for b in list(protected)[i+1:]:
                if a in ancestors[b] or b in ancestors[a]:
                    continue
                if (a in labels or b in labels) and overlap(protected[a], protected[b]):
                    issue("warning", "label-overlap", f"{a} / {b}: bounding rectangles overlap")
        for i, a in enumerate(sorted(nodes & bounds.keys())):
            for b in sorted(nodes & bounds.keys())[i+1:]:
                if a not in ancestors[b] and b not in ancestors[a] and overlap(bounds[a], bounds[b]):
                    issue("warning", "component-overlap", f"{a} / {b}")
        routes = []
        for cell in edges:
            id, style = cell.get("id"), style_of(cell)
            if cell.get("value"):
                issue("warning", "edge-label-unchecked", f"{id}: automatic edge-label placement needs visual inspection")
            if (style.get("noEdgeStyle") != "1"
                    or any(style.get(k) != "0" for k in ("exitPerimeter", "entryPerimeter"))
                    or any(style.get(k, "0") != "0" for k in ("curved", "rounded"))):
                issue("warning", "route-unchecked", f"{id}: renderer routing/perimeters cannot be predicted")
                continue
            endpoint_points = []
            for attr, prefix in (("source", "exit"), ("target", "entry")):
                endpoint = cell.get(attr)
                x, y, w, h = rectangle(endpoint)
                px, py = number(style[prefix+"X"]), number(style[prefix+"Y"])
                if not 0 <= px <= 1 or not 0 <= py <= 1:
                    raise ValueError(f"Port outside endpoint: {id}")
                point = (x+px*w, y+py*h)
                endpoint_points.append(point)
                visible = [s for s in symbols if s == endpoint or endpoint in ancestors[s]]
                if visible and not any(on_border(point, bounds[s]) for s in visible):
                    issue("warning", "floating-port", f"{id}: {attr} is not on its visible symbol")
            geo = cell.find("mxGeometry")
            if geo is None:
                raise ValueError(f"Missing edge geometry: {id}")
            origin = rectangle(cell.get("parent"))
            waypoints = [(number(p.get("x"))+origin[0], number(p.get("y"))+origin[1])
                         for p in geo.findall("./Array[@as='points']/mxPoint")]
            points = [endpoint_points[0], *waypoints, endpoint_points[1]]
            if any(not (abs(a[0]-b[0]) < 1e-6 or abs(a[1]-b[1]) < 1e-6)
                   for a, b in zip(points, points[1:])):
                issue("warning", "route-unchecked", f"{id}: diagonal/curved routing is not checked")
                continue
            if any(x < 0 or y < 0 or x > width or y > height for x, y in points):
                issue("warning", "route-outside-page", id)
            routes.append((id, points, style))
            for other, rect in protected.items():
                if any(through(a, b, rect) for a, b in zip(points, points[1:])):
                    issue("warning", "route-collision", f"{id} crosses {other}'s bounding rectangle")
        if clarity:
            route_clarity(routes, issue)

        if preview is not None:
            png_size(preview)
            stamp = load_json(Path(preview).with_suffix(".render.json"))
            if not isinstance(stamp, dict):
                raise ValueError("Render record must be an object")
            if stamp.get("source_sha256") != digest(source) or stamp.get("png_sha256") != digest(preview):
                issue("error", "stale-preview", "Source/PNG hashes do not match the render record")
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError) as error:
        issue("error", "invalid-input", str(error))
    return result()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--contract", type=Path)
    parser.add_argument("--preview", type=Path)
    parser.add_argument("--mode", choices=MODES)
    parser.add_argument("--strict", action="store_true", help="Fail on warnings as well as errors")
    parser.add_argument("--clarity", action="store_true", help="Also flag shared connector lanes and unmarked crossings")
    args = parser.parse_args()
    report = check(args.source, contract=args.contract, preview=args.preview, mode=args.mode, clarity=args.clarity)
    print(json.dumps(report, indent=2))
    return int(bool(report["errors"] or (args.strict and report["warnings"])))


if __name__ == "__main__":
    sys.exit(main())
