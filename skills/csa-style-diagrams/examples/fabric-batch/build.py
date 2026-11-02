"""Original synthetic Fabric composition; no official icons or cloud access."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from csa_drawio import Diagram, icon_path

NODES = {
    "source": ("Enterprise\nsources", "external", "cylinder", 25, 270, 150, "Data + outcomes"),
    "copy": ("Copy activity", "W1", "note", 230, 270, 150, "Data Factory / W1"),
    "bronze": ("Bronze\nlakehouse", "W1", "cylinder", 420, 270, 150, "Raw data / W1"),
    "clean": ("Quality\nnotebook", "W2", "note", 610, 270, 150, "Validate / W2"),
    "silver": ("Silver\nlakehouse", "W2", "cylinder", 800, 270, 150, "Curated Delta / W2"),
    "prep": ("EDA + features", "W2", "note", 990, 270, 150, "Datasets / W2"),
    "train": ("Train +\nevaluate", "W2", "note", 1180, 270, 150, "Notebook / W2"),
    "exp": ("MLflow\nexperiment", "W2", "ellipse", 1370, 270, 150, "Runs + artifacts / W2"),
    "model": ("Fabric ML\nmodel", "W2", "document", 1560, 270, 150, "Versioned model / W2"),
    "review": ("Human review", "W2", "process", 1515, 630, 220, "Approve + pin version / W2"),
    "score": ("Batch scoring", "W2", "note", 1190, 630, 210, "PREDICT / W2"),
    "gold": ("Gold lakehouse", "W3", "cylinder", 860, 630, 150, "Predictions / W3"),
    "sem": ("Semantic model", "W3", "document", 610, 630, 150, "Direct Lake / W3"),
    "report": ("Power BI report", "W3", "document", 310, 630, 150, "Insights / W3"),
    "quality": ("Quality / drift notebook", "W2", "note", 940, 900, 260, "Custom checks / W2"),
}
EDGES = [
    ("source", "copy", "data", "Source data and outcomes"),
    ("copy", "bronze", "data", "Land raw data"),
    ("bronze", "clean", "data", "Read raw batches"),
    ("clean", "silver", "data", "Validated Delta tables"),
    ("silver", "prep", "data", "Curated data"),
    ("prep", "train", "data", "Training and validation data"),
    ("train", "exp", "data", "Log runs and artifacts"),
    ("exp", "model", "data", "Register selected run"),
    ("model", "review", "control", "Review candidate version"),
    ("review", "score", "control", "Approve and pin version"),
    ("prep", "score", "data", "New scoring batches"),
    ("score", "gold", "data", "Write predictions"),
    ("gold", "sem", "data", "Direct Lake"),
    ("sem", "report", "data", "BI consumption"),
    ("gold", "quality", "data", "Predictions and provenance"),
    ("silver", "quality", "data", "Actuals when available"),
    ("quality", "train", "control", "Human-reviewed retraining decision"),
]


def build(output, overwrite=False, *, official_icons=False):
    output = Path(output)
    if not overwrite and any((output / name).exists() for name in ("architecture.drawio", "contract.json")):
        raise ValueError("Generated source/contract exists; choose a new output directory or --overwrite")
    d = Diagram("Fabric batch data science - annotated layout example", 1850, 1190)
    d.text("title", "Microsoft Fabric - batch data science", (28, 16, 1790, 36), size=30, bold=True)
    subtitle = ("Original layout example | One deployment stage | Official Fabric item icons; generic sources, activity and human review"
                if official_icons else "Original layout example | One deployment stage | Neutral symbols, not official product icons")
    d.text("subtitle", subtitle,
           (30, 55, 1780, 24), size=18)
    d.shape("fabric-scope", "", (205, 125, 1620, 990),
            "fillColor=#FFFFFF;strokeColor=#A2BBD0;", role="boundary").set("boundaryKind", "logical")
    d.text("scope-title", "Microsoft Fabric - logical solution scope", (230, 140, 600, 30), bold=True)
    phases = [
        ("ingest", "Ingest", (225, 190, 365, 260)),
        ("prepare", "Prepare data", (605, 190, 555, 260)),
        ("experiment", "Experiment + register", (1175, 190, 555, 260)),
        ("select", "Review", (1500, 540, 250, 250)),
        ("scoring", "Batch score", (1175, 540, 300, 250)),
        ("consume", "Consume predictions", (225, 540, 885, 250)),
        ("monitor", "Monitor", (900, 840, 575, 220)),
    ]
    for i, (id, title, rect) in enumerate(phases, 1):
        d.boundary(id, title, rect, kind="logical", number=i, title_width=110 if id == "monitor" else None)
    for id, (title, workspace, symbol, x, y, width, caption) in NODES.items():
        icons = {"bronze": "lakehouse", "silver": "lakehouse", "gold": "lakehouse",
                 "clean": "notebook", "prep": "notebook", "train": "notebook", "score": "notebook",
                 "quality": "notebook", "exp": "experiment", "model": "model",
                 "sem": "semantic-model", "report": "report"}
        d.component(id, title, x, y, workspace=workspace, symbol=symbol, width=width, caption=caption,
                    svg=icon_path(icons[id], family="fabric") if official_icons and id in icons else None)

    routing = {
        ("model", "review"): dict(end="top", via=((1750, 298), (1750, 610), (1625, 610))),
        ("review", "score"): dict(start="left", end="right",
                                 via=((1455, 675), (1455, 658)),
                                 label="Pin version", label_rect=(1355, 632, 140, 22)),
        ("prep", "score"): dict(start="right-low", end="top",
                               via=((1145, 312), (1145, 521), (1445, 521), (1445, 610), (1295, 610)),
                               label="Scoring batches", label_rect=(1175, 494, 230, 22)),
        ("score", "gold"): dict(start="left", end="right",
                               label="Predictions", label_rect=(1055, 630, 155, 22)),
        ("gold", "sem"): dict(start="left", end="right",
                             label="Direct Lake", label_rect=(770, 630, 130, 22)),
        ("sem", "report"): dict(start="left", end="right",
                               label="BI queries", label_rect=(490, 630, 130, 22)),
        ("gold", "quality"): dict(start="right-low", end="top",
                                 via=((1050, 672), (1050, 810), (1070, 810)),
                                 label="Predictions + provenance", label_rect=(1080, 802, 290, 22)),
        ("silver", "quality"): dict(start="right-low", end="right",
                                   via=((953, 312), (953, 487), (1800, 487), (1800, 928)),
                                   label="Actuals when available", label_rect=(1500, 460, 240, 22)),
        ("quality", "train"): dict(start="left", end="top",
                                  via=((215, 928), (215, 105), (1165, 105), (1165, 250), (1255, 250)),
                                  label="Human-reviewed retraining decision (custom)",
                                  label_rect=(450, 82, 650, 22)),
    }
    for i, (a, b, kind, meaning) in enumerate(EDGES):
        d.connect(f"flow-{i:02}", a, b, kind=kind, meaning=meaning, **routing.get((a, b), {}))
    d.text("monitor-note", "Compare predictions\nwith eligible actuals.\nA person decides to retrain.",
           (1220, 970, 240, 76), size=16)
    d.text("legend", "Blue bands = logical phases, not workspaces. Solid = data / artifacts. Dashed = human control. Crossings are not junctions.",
           (230, 1082, 1575, 24), size=16)
    d.text("ownership", "Workspace ownership: W1 Bronze ingestion | W2 Silver + data science | W3 Gold + analytics. Authorize cross-workspace access.",
           (28, 1132, 1780, 26), size=17)
    d.text("limitations", "No native feature store, online endpoint, automatic promotion or automatic drift-triggered retraining is implied. See the example notes.",
           (28, 1164, 1790, 22), size=14)
    output.mkdir(parents=True, exist_ok=True)
    d.save(output / "architecture.drawio")
    contract = {
        "title": "Synthetic Fabric batch data science",
        "nodes": {id: {"title": n[0].replace("\n", " "), "workspace": n[1]} for id, n in NODES.items()},
        "edges": [{"source": a, "target": b, "kind": kind, "label": meaning} for a, b, kind, meaning in EDGES],
    }
    (output / "contract.json").write_text(json.dumps(contract, indent=2) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    try:
        build(args.output_dir, args.overwrite)
    except (OSError, ValueError) as error:
        parser.error(str(error))
