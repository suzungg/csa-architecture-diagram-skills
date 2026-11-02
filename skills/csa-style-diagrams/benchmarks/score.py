"""Recompute local pilot measurements; does not launch agents or claim a winner."""
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "scripts"))
from check_diagram import check, digest, load_json

COVERAGE = {"route-unchecked", "edge-label-unchecked", "text-unmeasured", "output-mode"}


def score(root=ROOT):
    briefs = load_json(root / "briefs.json")
    rows = []
    for case in briefs["cases"]:
        for condition in ("baseline", "csa"):
            directory = root / "runs" / f"{case}-{condition}"
            contract = directory / "contract.json"
            for stage in ("first", "final", "edit"):
                source = directory / f"{stage}.drawio"
                report = check(source, contract=contract, preview=directory / f"{stage}.png", clarity=True)
                measured = load_json(directory / f"{stage}.text.json")
                if measured["source_sha256"] != digest(source):
                    raise ValueError(f"Stale browser measurements: {case}/{condition}/{stage}")
                models = list(ET.parse(source).iter("mxGraphModel"))
                if len(models) != 1:
                    raise ValueError("Pilot requires one uncompressed model")
                model = models[0]
                if float(model.get("pageWidth")) != 1600 or float(model.get("pageHeight")) != 1000:
                    raise ValueError("Pilot canvas differs from the frozen brief")
                text_issues = [i for i in measured["issues"] if i["code"].startswith(("text-", "rendered-text-"))]
                rows.append({
                    "case": case, "condition": condition, "stage": stage,
                    "source_sha256": digest(source),
                    "contract_errors": report["errors"],
                    "measurement_errors": measured["errors"],
                    "text_cells_measured": len(measured.get("measured", [])),
                    "geometry_findings": sum(i["level"] == "warning" and i["code"] not in COVERAGE for i in report["issues"]),
                    "text_findings": sum(i["code"] != "text-unmeasured" for i in text_issues),
                    "coverage_warnings": sum(i["code"] in COVERAGE for i in report["issues"]+text_issues),
                    "issue_codes": [i["code"] for i in report["issues"]+text_issues],
                })
    return rows


if __name__ == "__main__":
    try:
        print(json.dumps(score(), indent=2))
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError) as error:
        print(f"Pilot scoring failed: {error}", file=sys.stderr)
        sys.exit(1)
