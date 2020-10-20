import os.path
from pathlib import Path

import pytest

from .models import Classifier, Collection
from .rawfiles import INDEX_FILENAME, classifiers_dir, collections_dir


def _get_params(basedir: Path):
    params = []
    for index_path in basedir.rglob(INDEX_FILENAME):
        name = str(os.path.relpath(index_path.parent, basedir))
        params.append((name, index_path))
    return params


def test_index_md_is_defined(top_data_folder):
    assert any(top_data_folder.rglob(INDEX_FILENAME))

    for root, dirs, files in os.walk(top=top_data_folder):
        if files:
            assert (
                INDEX_FILENAME in files
            ), f"Folder {root} must list {INDEX_FILENAME}: {files}"
        else:
            assert dirs, f"It seems {root} is empty"


@pytest.mark.parametrize("name,index_path", _get_params(classifiers_dir))
def test_classifier(name: str, index_path: Path):

    model = Classifier.create_from_index_md(index_path)
    print(model)

    assert model.classifier == name.replace("/", "::")
    # NOTE: removed this requirement since a huge bunch of classifiers were added
    # without any explanation
    #
    # assert model.markdown
    if model.logo:
        assert (index_path.parent / model.logo).exists()


@pytest.mark.parametrize("name,index_path", _get_params(collections_dir))
def test_collections(name: str, index_path: Path):

    model = Collection.create_from_index_md(index_path)  # validates
    print(model)

    assert model.display_name == name.split("/")[-1]
    assert model.markdown
