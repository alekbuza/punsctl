# -*- coding: utf-8 -*-
# Copyright (c) 2022 Aleksandar Buza <me@aleksandarbuza.com>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from os import R_OK, W_OK, access, mkdir, readlink
from pathlib import Path
from typing import List, Optional

from punsctl.static import DEFAULT_ROOT_PATH, DEFAULT_SYMLINK_PATH

__all__ = ["RootSpace", "RootSpaceException"]


class RootSpaceException(Exception):
    def __init__(self, message):
        self.message = message


class RootSpace(object):
    def __init__(
        self,
        path: Path = Path(DEFAULT_ROOT_PATH),
        symlink_path: Path = Path(DEFAULT_SYMLINK_PATH),
    ):
        # Root path checks
        if not path.exists():
            if access(path.parent, W_OK) is not True:
                raise RootSpaceException(message=f"path {path} is not writable")

            try:
                mkdir(path, mode=0o744)

            except OSError as exc:
                raise RootSpaceException(message=exc.strerror)

        if not path.is_dir():
            raise RootSpaceException(message=f"path {path} is not a directory")

        if access(path, R_OK) is not True:
            raise RootSpaceException(message=f"path {path} is not readable")

        # Symlink path checks
        if not symlink_path.exists():
            raise RootSpaceException(message=f"path {symlink_path} doesn't exists")

        if not symlink_path.is_dir():
            raise RootSpaceException(message=f"path {symlink_path} is not a directory")

        if access(symlink_path, W_OK) is not True:
            raise RootSpaceException(message=f"path {symlink_path} is not writable")

        self.path = path
        self.symlink_path = symlink_path
        self.current_ns_path = Path(f"{symlink_path}/.current_ns")

    def get_path(self) -> Path:
        return self.path

    def get_symlink_path(self) -> Path:
        return self.symlink_path

    def get_current_ns_path(self) -> Path:
        return self.current_ns_path

    def get_current_ns_name(self) -> Optional[str]:
        if self.current_ns_path.exists() and self.current_ns_path.is_symlink():
            return Path(readlink(self.current_ns_path)).name

        return None

    def get_all_ns_paths(self) -> List[Path]:
        namespaces = []

        for namespace in self.path.iterdir():
            if namespace.is_dir() and not namespace.is_symlink():
                namespaces.append(namespace)

        namespaces.sort()

        return namespaces
