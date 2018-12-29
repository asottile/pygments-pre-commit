[![Build Status](https://travis-ci.org/asottile/pygments-pre-commit.svg?branch=master)](https://travis-ci.org/asottile/pygments-pre-commit)
[![Coverage Status](https://coveralls.io/repos/github/asottile/pygments-pre-commit/badge.svg?branch=master)](https://coveralls.io/github/asottile/pygments-pre-commit?branch=master)

pygments-pre-commit
===================

A pygments lexer for pre-commit output

See [some demos](https://asottile.github.io/pygments-pre-commit)!

## Installation

`pip install pygments-pre-commit`

## Usage

This library provides a pygments lexer called `pre-commit`.

```rst
.. code-block:: pre-commit

    $ pre-commit run
    passing..................................................................Passed
    failing..................................................................Failed
    hookid: failing

    ['.pre-commit-config.yaml', 'a']

    skipped (no files)...................................(no files to check)Skipped
    skip me.................................................................Skipped
```

This library also provides a sphinx extension.  It can be enabled by adding
`'pygments_pre_commit'` to the `extensions` setting in your `conf.py`.

The colors can be tweaked using the sphinx setting (in `conf.py`)
`pygments_pre_commit_ansi_colors`:

```python
pygments_pytest_ansi_colors = {
    'Black': '#2e3436',
    'Cyan': '#06989a',
    'Green': '#4e9a06',
    'Red': '#c00',
    'Yellow': '#c4A000',
}
```
