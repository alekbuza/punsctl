### `The project is currently under development and is not ready for use in production.`

# punsctl - POSIX User's Namespace Control

[![PyPI Version](https://img.shields.io/pypi/v/punsctl)](https://pypi.python.org/pypi/punsctl)
![PyPI - Downloads](https://img.shields.io/pypi/dm/punsctl?style=flat-square)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/punsctl)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/punsctl)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/punsctl)

[![codecov](https://codecov.io/github/alekbuza/punsctl/branch/main/graph/badge.svg?token=OMHOSME5ZB)](https://codecov.io/github/alekbuza/punsctl)
[![License: ISC](https://img.shields.io/badge/License-ISC-blue.svg)](https://opensource.org/licenses/ISC)


The `punsctl` utility manages multiple namespaces (user environments) for the current POSIX user.
That means the user can have multiple "_profiles_" for the same or different tool configurations in the same user account
(`~/.ssh`, `~/.gitconfig`, `~/.gnupg`, `~/.config`, `~/.config/nvim`, ...).
The user can create, delete, activate and deactivate namespaces without additional permissions.

## Installation

```sh
pip install punsctl
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

