"""Original icon reference sheet, not a deployment topology."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from csa_drawio import ASSET_ROOT, Diagram, icon_path

ROWS = [
    ("core", "Foundry core", 120,
     ["foundry", "foundry-project", "foundry-models", "foundry-agent-service"]),
    ("data", "Application hosting and connected data services", 385,
     ["container-apps-environment", "ai-search", "cosmos-db", "storage-account"]),
    ("access", "Security, networking and observability", 650,
     ["key-vault", "firewall", "private-endpoint", "virtual-network", "application-insights"]),
]


def build(output, overwrite=False):
    output = Path(output)
    if not overwrite and any((output / name).exists() for name in ("architecture.drawio", "contract.json")):
        raise ValueError("Output exists; choose a new directory or explicitly --overwrite")
    catalog = json.loads((ASSET_ROOT / "catalog.json").read_text(encoding="utf-8"))
    d = Diagram("Foundry diagram symbols", 1600, 1030)
    d.text("title", "Foundry diagram symbols", (40, 20, 1480, 38), size=30, bold=True)
    d.text("subtitle", "Official Microsoft Azure icons | Curated local lookup keys | Reference sheet, not a deployment topology",
           (40, 65, 1500, 26), size=18)
    nodes = {}
    for id, title, top, names in ROWS:
        d.boundary(id, title, (40, top, 1520, 235), kind="logical")
        for i, name in enumerate(names):
            x, width = (110 + 380*i, 240) if len(names) == 4 else (90 + 300*i, 220)
            display = catalog["icons"][name]["display_name"]
            d.component(name, display, x, top+70, scope="icon-reference",
                        width=width, caption=name, svg=icon_path(name))
            nodes[name] = {"title": display, "scope": "icon-reference"}
    d.text("meaning", "A project is an ownership/development scope, not a subnet or an inference proxy. A private endpoint is not the hosted service.",
           (40, 918, 1510, 28), size=17)
    d.text("terms", "Use only for architecture diagrams, training or documentation under Microsoft's icon terms. Preserve colors and proportions; no endorsement implied.",
           (40, 958, 1510, 25), size=14)
    output.mkdir(parents=True, exist_ok=True)
    d.save(output / "architecture.drawio")
    (output / "contract.json").write_text(json.dumps({"nodes": nodes, "edges": []}, indent=2) + "\n",
                                        encoding="utf-8", newline="\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    try:
        build(args.output_dir, args.overwrite)
    except (OSError, ValueError) as error:
        parser.error(str(error))
