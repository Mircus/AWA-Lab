"""Execute six notebooks in isolated kernels, optionally retaining their outputs.

    python scripts/run_notebooks.py           # CI / verification
    python scripts/run_notebooks.py --write   # update visual previews for GitHub
"""
from pathlib import Path
import argparse
import nbformat
from nbclient import NotebookClient

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--write', action='store_true', help='save executed outputs for GitHub preview')
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
paths = sorted((root/'notebooks').glob('*.ipynb'))
assert len(paths) == 6, 'Expected exactly six experiment notebooks'
for path in paths:
    print('Running', path.name, flush=True)
    notebook = nbformat.read(path, as_version=4)
    client = NotebookClient(notebook, timeout=120, kernel_name='python3',
                            resources={'metadata': {'path': str(root)}})
    client.execute()
    if args.write:
        nbformat.write(notebook, path)
print(f'All {len(paths)} notebooks executed successfully')
