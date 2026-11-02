"""Reuse the neutral Fabric example's topology with reviewed official item icons."""
import argparse
from pathlib import Path
import runpy


def build(output, overwrite=False):
    generator = Path(__file__).resolve().parents[1] / "fabric-batch" / "build.py"
    runpy.run_path(str(generator))["build"](output, overwrite, official_icons=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    try:
        build(args.output_dir, args.overwrite)
    except (OSError, ValueError) as error:
        parser.error(str(error))
