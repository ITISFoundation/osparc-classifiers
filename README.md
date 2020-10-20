# osparc-classifiers

A curated list of classifiers defined and used by the osparc-community

![](https://i.imgur.com/snpGa2V.png)

### Concept

- A classifier is a label with a hierarchical format (e.g. ``programming-language::python``) and its associated metadata (e.g. description, maintainer, ...) that is curated by the community
- Classifiers are used to annotate osparc entities (e.g. services, studies, data) in a particular subject area,
- Our approach to classifiers combines two existing implementations: the python distribution metadata standard [PEP 301](https://www.python.org/dev/peps/pep-0301/#distutils-trove-classification) for the hierarchical-names and a curation workflow very similar to [Github Explore](https://github.com/github/explore#github-explore).

#### Examples of Classifiers Labeling

For some inspiration, check:
- python packages are annotated using [these classifiers](https://pypi.org/classifiers/)
- Github explore [topics](https://github.com/github/explore/tree/master/topics)


### Curation Workflow

The basic idea is to reuse well known versioning, testing,review and integration techniques in software development to continuously curate classifiers

- Every classifier is defined as a directory under [data/classifiers](data/classifiers) that contains files with metadata and resources:
  - the classifier name is given by the folder path
  - ``index.md`` is a [markdown](https://guides.github.com/features/mastering-markdown/) format file with a [Jekyll front-matter](https://jekyllrb.com/docs/front-matter/) block for the classifier metadata
  - other resources (e.g. figures, images) refered in the ``index.md`` file
- Any changes or new classifiers are **pull requested** (PR) to this repository.
- Any PR is subject to the community review and triggers automatic validation of the changes/classifiers
  - Validation is based on data schemas or agreed conventions
  - The PR is only accepted when a minimum number of reviewers accept it and the automatic validation passes
- When PR is accepted, it is merge into the main branch AND the continuous integration transforms the classifiers into a **bundled artifact** that can be consumed by osparc.io

This workflows guarantees continues versioning, validation and community review of the classifiers in addition to produce a osparc.io-compatible bundle artifact with any version of the classifiers.


### Organization of the Repository


- [``.github``](.github) : all github and [github actions](https://github.com/features/actions) configuration to trigger the automatic validation and artifacts generation.
- [``.vscode``](.vscode)  : some template configs for one of the coolest open IDEs in the world ;-)
- [``data/classifiers``](data/classifiers): where classifiers names and metadata is hierarchicaly stored
- [``tools``](tools) : some python code to test ``data`` based on some json-schemas and layout conventions.



### References

- A gentle intro to github [workflows](https://guides.github.com/activities/hello-world/) used here for data curation