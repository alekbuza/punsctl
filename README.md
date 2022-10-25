### `The project is currently under development and is not ready for use in production.`

# punsctl - POSIX User's Namespace Control

[![codecov](https://codecov.io/github/alekbuza/punsctl/branch/main/graph/badge.svg?token=OMHOSME5ZB)](https://codecov.io/github/alekbuza/punsctl)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/punsctl)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/punsctl)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/punsctl)

The `punsctl` utility manages multiple namespaces (user environments) for the current POSIX user.
That means the user can have multiple "_profiles_" for the same or different tool configurations in the same user account
(`~/.ssh`, `~/.gitconfig`, `~/.gnupg`, `~/.config`, `~/.config/nvim`, ...).
The user can create, delete, activate and deactivate namespaces without additional permissions.

## Installation

```sh
pip install punsctl
```

## Usage

### Create a new namespace
```sh
punsctl -c <namespace>
```

### List all namespaces
```sh
punsctl -l
```

### Activate a namespace
```sh
punsctl -a <namespace>
```

### Deactivate namespaces
```sh
punsctl -d
```

### List all namespaces for the non-default root path (`~/.ns`)
```sh
punsctl -p <root_path> -l
```
