""" Read/write raw files and repo folder skeleton
"""

import json
import sys
from pathlib import Path
from typing import Dict, Tuple

import yaml

# paths
current_dir = Path(sys.argv[0] if __name__ == "__main__" else __file__).resolve().parent
data_dir = current_dir.parent.parent / "data"
classifiers_dir = data_dir / "classifiers"
collections_dir = data_dir / "collections"
schemas_dir = current_dir.parent / "schemas"

assert classifiers_dir.exists()
assert collections_dir.exists()
assert schemas_dir.exists()

INDEX_FILENAME = "index.md"


def load_index_md_file(index_path: Path) -> Tuple[Dict, str]:
    content = index_path.read_text()
    _, meta, markdown = content.split("---\n")
    return yaml.safe_load(meta), markdown


def create_index_json(index_path: Path) -> Path:
    meta, markdown = load_index_md_file(index_path)
    # appends markdown as meta
    meta["markdown"] = markdown
    # dumps into
    json_path = index_path.with_suffix(".json")
    json_path.write_text(json.dumps(meta, indent=2))
    return json_path
