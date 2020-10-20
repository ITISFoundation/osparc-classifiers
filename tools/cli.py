from tests.models import Classifier, Collection, DataBundleFile
from tests.rawfiles import schemas_dir, data_dir
import sys
from pathlib import Path
import os


def create_schemas():
    (schemas_dir / "classifier-meta.json").write_text(Classifier.schema_json(indent=2))
    (schemas_dir / "collection-meta.json").write_text(Collection.schema_json(indent=2))


def dump_bundle():
    output_dir = Path(sys.argv[1]).resolve()
    os.makedirs(output_dir, exist_ok=True)
    bundle_path = output_dir / "bundle.json"

    bundle = DataBundleFile.create_from_data_folder(data_dir)

    bundle_path.write_text(bundle.json(indent=2))


if __name__ == "__main__":
    dump_bundle()
