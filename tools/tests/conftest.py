from pathlib import Path

import pytest

from .rawfiles import classifiers_dir, collections_dir


@pytest.fixture(scope="session")
def classifiers_folder() -> Path:
    assert classifiers_dir.exists()
    return classifiers_dir


@pytest.fixture(scope="session")
def collections_folder() -> Path:
    assert collections_dir.exists()
    return collections_dir


@pytest.fixture(scope="session", params=[str(classifiers_dir), str(collections_dir),])
def top_data_folder(request) -> Path:
    # NOTE: params are passed as strings so they can be printed in tests log
    data_dir = Path(request.param)
    assert data_dir.exists()
    return data_dir
