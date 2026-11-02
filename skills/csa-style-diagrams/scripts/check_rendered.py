"""Optional local Chromium text measurement of a fresh draw.io SVG export."""
import argparse
import base64
import html
import json
from pathlib import Path
import re
import secrets
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

from check_diagram import check, digest, style_of
from csa_drawio import safe_svg


def inspect_svg(text):
    root = ET.fromstring(text)
    if root.tag != "{http://www.w3.org/2000/svg}svg":
        raise ValueError("Renderer did not produce SVG")
    for element in root.iter():
        if element.tag.split("}")[-1].lower() in {"script", "iframe", "object", "embed", "link"}:
            raise ValueError("Active exported content is refused")
        for key, value in element.attrib.items():
            name = key.split("}")[-1].lower()
            if name.startswith("on"):
                raise ValueError("Exported event handler is refused")
            if name in {"href", "src"} and not value.startswith("#"):
                if element.tag.endswith("}a") and value == "https://www.drawio.com/doc/faq/svg-export-text-problems":
                    continue  # Inert exporter help link, not an automatically loaded resource.
                if value.startswith("data:image/svg+xml;base64,"):
                    safe_svg(base64.b64decode(value.split(",", 1)[1], validate=True))
                elif not value.startswith("data:image/png;base64,"):
                    raise ValueError("External or unsupported exported image/link is refused")
    if re.search(r"@import", text, re.I):
        raise ValueError("External stylesheet is refused")
    for value in re.findall(r"url\((.*?)\)", text, re.I | re.S):
        if not value.strip().strip("'\"").startswith("#"):
            raise ValueError("External stylesheet resource is refused")


def measure(source, executable, browser, *, timeout=120):
    source, executable, browser = (Path(p).resolve() for p in (source, executable, browser))
    if not executable.is_file() or not browser.is_file():
        raise ValueError("Supply existing approved draw.io and Chromium/Edge executables")
    report = check(source, clarity=True)
    if report["errors"]:
        raise ValueError("Source check failed: " + json.dumps(report["issues"]))
    cells = ET.parse(source).findall(".//mxCell")
    labels = [c.get("id") for c in cells if c.get("vertex") == "1" and c.get("value")]
    if any(style_of(c).get("html", "0") != "0" for c in cells if c.get("value")):
        raise ValueError("Only plain-text labels (html=0) are measured; rich HTML needs separate review")
    source_hash = digest(source)
    with tempfile.TemporaryDirectory(prefix="csa-text-") as directory:
        temp = Path(directory)
        svg = temp / "export.svg"
        subprocess.run([str(executable), "--disable-update", "--export", "--format", "svg",
                        "--theme", "light", "--output", str(svg), str(source)],
                       check=True, capture_output=True, text=True, timeout=timeout)
        text = svg.read_text(encoding="utf-8")
        inspect_svg(text)
        nonce = secrets.token_hex(16)
        script = Path(__file__).with_name("measure_text.js").read_text(encoding="utf-8")
        payload = json.dumps(labels).replace("<", "\\u003c")
        page = temp / "measure.html"
        page.write_text(
            '<!doctype html><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" '
            f'content="default-src \'none\'; img-src data:; style-src \'unsafe-inline\'; script-src \'nonce-{nonce}\'">'
            '<style>body{margin:0;color-scheme:light}svg{max-width:none}</style>'
            + re.sub(r"<\?xml.*?\?>|<!DOCTYPE[^>]*>", "", text, flags=re.S)
            + f'<pre id="csa-report"></pre><script nonce="{nonce}">window.csaLabels={payload};\n{script}</script>',
            encoding="utf-8")
        run = subprocess.run(
            [str(browser), "--headless=new", "--disable-gpu", "--no-first-run",
             "--no-default-browser-check", "--disable-background-networking", "--disable-extensions",
             "--disable-sync", f"--user-data-dir={temp / 'profile'}",
             "--dump-dom", "--virtual-time-budget=3000", page.as_uri()],
            check=True, capture_output=True, text=True, encoding="utf-8", timeout=timeout)
        match = re.search(r'<pre id="csa-report" data-ready="1">(.*?)</pre>', run.stdout, re.S)
        if match is None:
            raise ValueError("Browser did not return completed text measurements")
        measured = json.loads(html.unescape(match.group(1)))
        if source_hash != digest(source):
            raise ValueError("Source changed during measurement")
        measured["issues"] = report["issues"] + measured["issues"]
        measured["errors"] = sum(i["level"] == "error" for i in measured["issues"])
        measured["warnings"] = sum(i["level"] == "warning" for i in measured["issues"])
        measured["source_sha256"] = source_hash
        measured["coverage"] = "Browser-laid-out SVG text and explicit route clarity; not PNG OCR or cloud validation"
        return measured


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--drawio", required=True, type=Path)
    parser.add_argument("--browser", required=True, type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    try:
        report = measure(args.source, args.drawio, args.browser)
    except (OSError, ValueError, ET.ParseError, subprocess.SubprocessError) as error:
        print(f"Rendered check failed: {error}", file=sys.stderr)
        if isinstance(error, subprocess.CalledProcessError):
            print(error.stderr or error.stdout, file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2))
    return int(bool(report["errors"] or (args.strict and report["warnings"])))


if __name__ == "__main__":
    sys.exit(main())
