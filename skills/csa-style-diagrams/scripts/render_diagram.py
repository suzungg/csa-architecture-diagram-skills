"""Export through an explicitly selected local draw.io Desktop executable."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from check_diagram import check, digest, png_size


def render(source, executable, output, *, width=2400, timeout=120, overwrite=False):
    source, executable, output = (Path(p).resolve() for p in (source, executable, output))
    if not source.is_file() or not executable.is_file():
        raise ValueError("Source and explicitly selected draw.io executable must exist")
    if output.suffix.lower() != ".png" or output == source or width <= 0 or timeout <= 0:
        raise ValueError("Use a distinct .png output and positive width/timeout")
    record = output.with_suffix(".render.json")
    if not overwrite and (output.exists() or record.exists()):
        raise ValueError("Output/render record exists; use --overwrite only for an intentional replacement")
    report = check(source)
    if report["errors"]:
        raise ValueError("Source check failed: " + json.dumps(report["issues"]))
    source_hash = digest(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".csa-render-", dir=output.parent) as temp:
        png = Path(temp) / "preview.png"
        subprocess.run(
            [str(executable), "--disable-update", "--force-device-scale-factor=1",
             "--export", "--format", "png", "--width", str(width), "--border", "0",
             "--theme", "light", "--output", str(png), str(source)],
            check=True, timeout=timeout, capture_output=True, text=True,
        )
        dimensions = png_size(png)
        if source_hash != digest(source):
            raise ValueError("Source changed during export; previous output was not replaced")
        stamp = {"source_sha256": source_hash, "png_sha256": digest(png),
                 "png_dimensions": list(dimensions),
                 "visual_review": "not established by rendering; inspect the actual PNG"}
        temporary_record = Path(temp) / "render.json"
        temporary_record.write_text(json.dumps(stamp, indent=2) + "\n", encoding="utf-8", newline="\n")
        png.replace(output)
        temporary_record.replace(record)
    return {"output": str(output), "warnings": report["warnings"], **stamp}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--drawio", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--width", type=int, default=2400)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    try:
        result = render(args.source, args.drawio, args.output, width=args.width,
                        timeout=args.timeout, overwrite=args.overwrite)
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(f"Export failed: {error}", file=sys.stderr)
        if isinstance(error, subprocess.CalledProcessError):
            print(error.stderr or error.stdout or "Renderer supplied no diagnostic output", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
