# -*- coding: utf-8 -*-
# Copyright (c) 2022, 2024 Aleksandar Buza <tech@aleksandarbuza.com>
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

import logging
from os import R_OK, W_OK, access, mkdir, readlink
from pathlib import Path
from typing import List, Optional

from punsctl.exceptions import RootSpaceException
from punsctl.static import (
    CURRENT_NS_SYMLINK_NAME,
    DEFAULT_ROOTSPACE_MKDIR_MODE,
    DEFAULT_ROOTSPACE_PATH,
    DEFAULT_SYMLINK_PATH,
)

__all__ = ["RootSpace"]


class RootSpace(object):
    def __init__(
        self,
        path: Path = Path(DEFAULT_ROOTSPACE_PATH),
        symlink_path: Path = Path(DEFAULT_SYMLINK_PATH),
    ):
        self.path = path
        self.symlink_path = symlink_path
        self.current_ns_path = Path(f"{symlink_path}/{CURRENT_NS_SYMLINK_NAME}")

        logging.debug(f"debug: rootspace: path: {self.path}")
        logging.debug(f"debug: rootspace: symlink path: {self.symlink_path}")
        logging.debug(
            f"debug: rootspace: current namespace path: {self.current_ns_path}"
        )

    def check(self) -> None:
        # Root path checks
        logging.debug(
            f"debug: rootspace: checking {self.path.parent} write permissions"
        )
        if not self.path.exists():
            if access(self.path.parent, W_OK) is not True:
                raise RootSpaceException(message=f"path {self.path} is not writable")

            try:
                mkdir(self.path, mode=DEFAULT_ROOTSPACE_MKDIR_MODE)

            except OSError as exc:
                raise RootSpaceException(message=exc.strerror)

        logging.debug(f"debug: rootspace: checking {self.path} is a directory")
        if not self.path.is_dir():
            raise RootSpaceException(message=f"path {self.path} is not a directory")

        logging.debug(f"debug: rootspace: checking {self.path} read permissions")
        if access(self.path, R_OK) is not True:
            raise RootSpaceException(message=f"path {self.path} is not readable")

        # Symlink path checks
        logging.debug(f"debug: rootspace: checking {self.symlink_path} exists")
        if not self.symlink_path.exists():
            raise RootSpaceException(message=f"path {self.symlink_path} doesn't exists")

        logging.debug(f"debug: rootspace: checking {self.symlink_path} is a directory")
        if not self.symlink_path.is_dir():
            raise RootSpaceException(
                message=f"path {self.symlink_path} is not a directory"
            )

        logging.debug(
            f"debug: rootspace: checking {self.symlink_path} write permissions"
        )
        if access(self.symlink_path, W_OK) is not True:
            raise RootSpaceException(
                message=f"path {self.symlink_path} is not writable"
            )

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
