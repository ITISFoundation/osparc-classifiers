"""
    Data models
"""
import os
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, HttpUrl, constr, validator

from .rawfiles import load_index_md_file, INDEX_FILENAME

current_dir = Path(sys.argv[0] if __name__ == "__main__" else __file__).resolve().parent


GITHUB_URL = "https://github.com/"

ItemsSequence = Union[str, List]


def comma_separated_to_list(values: ItemsSequence) -> List:
    return [v.strip() for v in values.split(",")] if isinstance(values, str) else values


ClassifierName = constr(regex=r"[\w:]+")


class Classifier(BaseModel):
    classifier: str
    display_name: str
    short_description: Optional[str]
    logo: Optional[Path] = None
    aliases: ItemsSequence = []
    created_by: str
    released: Optional[date] = None
    related: ItemsSequence = []
    url: Optional[HttpUrl] = None
    github_url: Optional[HttpUrl] = None
    wikipedia_url: Optional[HttpUrl] = None
    markdown: Optional[str] = ""
    rrid: Optional[str] = ""

    # pylint: disable=no-self-argument

    @classmethod
    def create_from_index_md(cls, index_path: Path) -> "Classifier":
        meta, md = load_index_md_file(index_path)
        return cls(markdown=md, **meta)

    @validator("github_url")
    def check_github_domain(cls, v):
        if v.startswith("gh:"):
            return v.replace("gh:", GITHUB_URL)
        if not v.startswith(GITHUB_URL):
            raise ValueError("expected github url or gh: prefix")

    _normalize_related = validator("related", allow_reuse=True)(comma_separated_to_list)
    _normalize_alias = validator("aliases", allow_reuse=True)(comma_separated_to_list)


class Collection(BaseModel):
    items: List[str] = Field(
        ..., description="List of studies repos associated to this collection"
    )
    display_name: str
    created_by: str
    markdown: Optional[str] = ""

    @classmethod
    def create_from_index_md(cls, index_path: Path) -> "Collection":
        meta, md = load_index_md_file(index_path)
        return cls(markdown=md, **meta)


class DataBundleFile(BaseModel):
    # meta
    build_date: str = os.environ.get("BUILD_DATE", str(datetime.now()))
    vcs_url: str = os.environ.get("VCS_URL")
    vcs_ref: str = os.environ.get("VCS_REF")

    # data
    classifiers: Dict[ClassifierName, Classifier]
    collections: Dict[str, Collection]

    @classmethod
    def create_from_data_folder(cls, data_path: Path) -> "DataBundleFile":
        classifiers_dir = data_path / "classifiers"

        clsf = [
            Classifier.create_from_index_md(index_path)
            for index_path in classifiers_dir.rglob(INDEX_FILENAME)
        ]

        collections_dir = data_path / "collections"

        colls = [
            Collection.create_from_index_md(index_path)
            for index_path in collections_dir.rglob(INDEX_FILENAME)
        ]

        return cls(classifiers={c.classifier:c for c in clsf}, collections={c.display_name:c for c in colls})

