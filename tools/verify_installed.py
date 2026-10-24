"""Run with a clean installed environment, from the repository root.

python tools/verify_installed.py --python .venv-clean/Scripts/python.exe
This invokes the console entry point outside the repository with PYTHONPATH removed.
"""

import argparse
import json
import os
import subprocess
import tempfile
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--python", type=Path, required=True)
args = parser.parse_args()
# Keep the venv path: resolving a POSIX interpreter symlink escapes its bin/.
python = args.python.absolute()
console = python.with_name("arabic-pdf-kit.exe" if os.name == "nt" else "arabic-pdf-kit")
root = Path(__file__).resolve().parents[1]
env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
commands = [
    (["--help"], 0),
    (["fixtures", "verify"], 0),
    (["evaluate", str(root / "examples/positive-control.json"), "--output", "control.json", "--html", "control.html"], 0),
    (["run", "--engine", "pypdf", "--output", "pypdf.json", "--html", "pypdf.html"], 1),
    (["compare", "pypdf.json", "pypdf.json", "--output", "comparison.json"], 0),
    (["report", "pypdf.json", "--html", "report.html"], 0),
]
with tempfile.TemporaryDirectory() as directory:
    for command, expected in commands:
        result = subprocess.run([str(console), *command], cwd=directory, env=env,
                                capture_output=True, text=True, check=False)
        if result.returncode != expected:
            raise RuntimeError(f"Installed command {command[0]} returned {result.returncode}: {result.stderr}")
    run = json.loads((Path(directory) / "pypdf.json").read_text(encoding="utf-8"))
    assert run["summary"] == {"PASS": 0, "FAIL": 8, "ERROR": 0, "SKIPPED": 0}
print("Installed-package quickstart: 6 commands passed outside checkout")
