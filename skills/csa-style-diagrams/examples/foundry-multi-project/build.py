"""Synthetic logical request view: two Foundry projects share model deployments."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from csa_drawio import Diagram, icon_path


def build(output, overwrite=False):
    output = Path(output)
    if not overwrite and any((output / name).exists() for name in ("architecture.drawio", "contract.json")):
        raise ValueError("Output exists; choose a new directory or explicitly --overwrite")
    d = Diagram("Foundry multi-project application", 1900, 1320)
    d.text("title", "Foundry - two use cases, shared model deployments", (40, 20, 1810, 40), size=30, bold=True)
    d.text("subtitle", "Logical ownership + request view | Public authenticated HTTPS assumed | Not a network isolation or deployment template",
           (40, 70, 1810, 30), size=18)
    boundaries = [
        ("applications", "Application-owned hosting", (40, 140, 360, 820), "logical"),
        ("foundry-resource", "Foundry resource - shared governance", (460, 140, 1100, 820), "resource"),
        ("project-a", "Project A - customer support", (500, 200, 500, 280), "project"),
        ("project-b", "Project B - research summary", (500, 620, 500, 280), "project"),
        ("search-resource", "Independent retrieval resource", (1250, 1010, 590, 240), "resource"),
        ("operations", "Application observability", (750, 1010, 460, 240), "resource"),
    ]
    for id, title, rect, kind in boundaries:
        d.boundary(id, title, rect, kind=kind)
    nodes = {
        "support-app": ("Support web app", "apps", 90, 263, 260, "Own UI + integration code", None),
        "research-app": ("Research web app", "apps", 90, 683, 260, "Own UI + integration code", None),
        "support-agent": ("Support agent", "support", 560, 280, 220, "Foundry Agent Service", "foundry-agent-service"),
        "research-agent": ("Research agent", "research", 560, 700, 220, "Foundry Agent Service", "foundry-agent-service"),
        "shared-models": ("Shared model deployments", "foundry", 1180, 480, 260, "Resource-owned inference", "foundry-models"),
        "search": ("Azure AI Search", "retrieval", 1410, 1090, 240, "Approved support content", "ai-search"),
        "telemetry": ("Application Insights", "operations", 850, 1090, 260, "App instrumentation enabled", "application-insights"),
    }
    for id, (title, owner, x, y, width, caption, icon) in nodes.items():
        d.component(id, title, x, y, scope=owner, width=width, caption=caption,
                    svg=icon_path(icon) if icon else None)
    relations = [
        ("support-app", "support-agent", "data", "runtime", "Agent API request", {}),
        ("research-app", "research-agent", "data", "runtime", "Agent API request", {}),
        ("support-agent", "shared-models", "data", "runtime", "Model inference",
         {"via": ((1100, 308), (1100, 508))}),
        ("research-agent", "shared-models", "data", "runtime", "Model inference",
         {"end": "left-low", "via": ((1140, 728), (1140, 522))}),
        ("support-agent", "search", "data", "runtime", "Configured search tool retrieves approved context",
         {"start": "right-low", "end": "right", "via": ((1860, 322), (1860, 1118))}),
        ("support-app", "telemetry", "telemetry", "telemetry", "Configured application telemetry",
         {"start": "right-low", "via": ((420, 330.5), (420, 1118))}),
        ("research-app", "telemetry", "telemetry", "telemetry", "Configured application telemetry",
         {"start": "right-low", "end": "left-low", "via": ((440, 750.5), (440, 1132))}),
    ]
    for i, (a, b, kind, intent, meaning, routing) in enumerate(relations):
        d.connect(f"flow-{i}", a, b, kind=kind, intent=intent, meaning=meaning, **routing)
    for id, text, rect in [
        ("request-a", "Agent request", (470, 272, 160, 24)),
        ("request-b", "Agent request", (470, 692, 160, 24)),
        ("model-call", "Inference", (1020, 278, 140, 24)),
        ("search-call", "Retrieve context", (1370, 337, 185, 26)),
        ("shared-note", "One deployment pool\nreused by both projects.\nProjects are not inference proxies.", (1160, 810, 350, 90)),
        ("app-note", "Applications stay outside\nFoundry Agent Service.\nResponses return on the\nsame logical request paths.", (75, 835, 300, 100)),
        ("resource-note", "Project boundaries describe ownership, not subnets. Connected services retain separate access/network controls.",
         (500, 914, 1010, 28)),
        ("footer", "Solid arrows = requests / telemetry; crossings are not junctions. No private connectivity, automatic RBAC or complete operations stack is implied.",
         (40, 1280, 1810, 26)),
    ]:
        d.text(id, text, rect, size=16)
    spec = {
        "nodes": {id: {"title": n[0], "scope": n[1]} for id, n in nodes.items()},
        "edges": [{"source": a, "target": b, "kind": k, "intent": intent} for a, b, k, intent, _, _ in relations],
        "scopes": {
            "apps": {"boundary": "applications", "kind": "logical"},
            "foundry": {"boundary": "foundry-resource", "kind": "resource"},
            "support": {"boundary": "project-a", "kind": "project", "parent": "foundry"},
            "research": {"boundary": "project-b", "kind": "project", "parent": "foundry"},
            "retrieval": {"boundary": "search-resource", "kind": "resource"},
            "operations": {"boundary": "operations", "kind": "resource"},
        },
    }
    output.mkdir(parents=True, exist_ok=True)
    d.save(output / "architecture.drawio")
    (output / "contract.json").write_text(json.dumps(spec, indent=2)+"\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    try:
        build(args.output_dir, args.overwrite)
    except (OSError, ValueError) as error:
        parser.error(str(error))
