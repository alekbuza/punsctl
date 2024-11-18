# punsctl - POSIX User's Namespace Control

[![PyPI Version](https://img.shields.io/pypi/v/punsctl)](https://pypi.python.org/pypi/punsctl)
![PyPI - Downloads](https://img.shields.io/pypi/dm/punsctl?style=flat-square)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/punsctl)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/punsctl)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/punsctl)

[![codecov](https://codecov.io/github/alekbuza/punsctl/graph/badge.svg?token=OMHOSME5ZB)](https://codecov.io/github/alekbuza/punsctl)
[![License: ISC](https://img.shields.io/badge/License-ISC-blue.svg)](https://opensource.org/licenses/ISC)

The `punsctl` utility allows users to manage multiple namespaces (or profiles) for various tool configurations within a single POSIX user account.
This enables users to maintain separate configurations for tools like `~/.ssh`, `~/.gitconfig`, `~/.gnupg`, `~/.config`, `~/.config/nvim`, and others, all under the same user account.
With punsctl, users can easily create, delete, activate, or deactivate namespaces without requiring additional system permissions, providing a flexible way to manage different environments or workflows.

## Installation

```sh
pipx install punsctl
```

## Usage

```txt
punsctl <options>

options:
    -h                  Help menu
    -r                  Root path                 (Default: ~/.ns)
    -s                  Symlink path              (Default: ~/)
    -l                  List namespaces
    -n <namespace>      Create namespace
    -x <namespace>      Delete namespace
    -a <namespace>      Activate namespace
    -d                  Deactivate namespaces
```

### List all namespaces
```sh
punsctl -l
```

### List all namespaces from the `non-default` root path
```sh
punsctl -p <root_path> -l
```

### Create new namespace
```sh
punsctl -n <namespace>
```

### Create a new namespace in the `non-default` root path
```sh
punsctl -p <root_path> -n <namespace>
```

### Delete namespace
```sh
punsctl -x <namespace>
```

### Delete namespace in `non-default` root path
```sh
punsctl -p <root_path> -x <namespace>
```

### Activate namespace
```sh
punsctl -a <namespace>
```

### Activate the namespace from the `non-default` root path
```sh
punsctl -p <root_path> -a <namespace>
```

### Activate the namespace from the `non-default` root path and change the symlink path

```sh
punsctl -p <root_path> -s <symlink_path> -a <namespace>
```

### Deactivate namespaces
```sh
punsctl -d
```

