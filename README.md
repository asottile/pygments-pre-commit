[![build status](https://github.com/asottile/pygments-pre-commit/actions/workflows/main.yml/badge.svg)](https://github.com/asottile/pygments-pre-commit/actions/workflows/main.yml)
[![Build Status](https://github.com/asottile/pygments-pre-commit/workflows/deploy/badge.svg)](https://github.com/asottile/pygments-pre-commit/actions)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/asottile/pygments-pre-commit/main.svg)](https://results.pre-commit.ci/latest/github/asottile/pygments-pre-commit/main)

pygments-pre-commit
===================

A pygments lexer for pre-commit output

See [some demos](https://asottile.github.io/pygments-pre-commit)!
Or [see it in action on pre-commit.com](https://pre-commit.com/#usage).

## Installation

```bash
pip install pygments-pre-commit
```

## Usage

This library provides a pygments lexer called `pre-commit`.

```rst
.. code-block:: pre-commit

    $ pre-commit run
    passing..................................................................Passed
    failing..................................................................Failed
    - hook id: failing
    - exit code: 1

    ['.pre-commit-config.yaml', 'a']

    skipped (no files)...................................(no files to check)Skipped
    skip me.................................................................Skipped
```

This library also provides a sphinx extension.  It can be enabled by adding
`'pygments_pre_commit'` to the `extensions` setting in your `conf.py`.

The colors can be tweaked using the sphinx setting (in `conf.py`)
`pygments_pre_commit_ansi_colors`:

```python
pygments_pre_commit_ansi_colors = {
    'Black': '#2e3436',
    'Cyan': '#06989a',
    'Green': '#4e9a06',
    'Red': '#c00',
    'Yellow': '#c4A000',
    'Faint': '#ccc',
}
```
