"""Create a new source-only ZIP from the reviewed allowlist, never Git/build data."""
from pathlib import Path
import argparse
import hashlib
import json
import zipfile
from check_public import ROOT, check

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('output', type=Path, help='New ZIP path (existing files are never overwritten)')
args = parser.parse_args()
files = check()
args.output.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(args.output, 'x', zipfile.ZIP_DEFLATED) as archive:
    for name in files:
        archive.write(ROOT / name, 'jacky-pocket-world/' + name)
with zipfile.ZipFile(args.output) as archive:
    if archive.testzip() is not None or len(archive.infolist()) != len(files):
        raise SystemExit('ZIP verification failed')
print(json.dumps({'files': len(files), 'bytes': args.output.stat().st_size,
                  'sha256': hashlib.sha256(args.output.read_bytes()).hexdigest()}, indent=2))
