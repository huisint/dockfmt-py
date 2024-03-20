# dockfmt-py

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A python package that provides a pip-installable
[dockfmt](https://github.com/jessfraz/dockfmt) binary.

The mechanism by which the binary is downloaded is basically copied from
[hadolint-py](https://github.com/AleksaC/hadolint-py).

## Getting started

### Installation

The package hasn't been published to PyPI yet, and may never be, as its primary
purpose doesn't require it. However you can install it through git:

```shell script
pip install git+https://github.com/huisint/dockfmt-py
```

### With pre-commit

Example `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/huisint/dockfmt-py
    rev: v0.3.3
    hooks:
      - id: dockfmt
        args:
          - fmt
```
