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

import os
from pathlib import Path
from typing import List, Optional

from punsctl.static import CURRENT_NS_PATH

__all__ = ["RootSpace", "RootSpaceException"]


class RootSpaceException(Exception):
    def __init__(self, message):
        self.message = message


class RootSpace(object):
    def __init__(self, path: Path):
        self.path = path

        if not self.path.exists():
            raise RootSpaceException(message=f"{self.path} doesn't exists")

        if not self.path.is_dir():
            raise RootSpaceException(message=f"{self.path} is not a directory")

    def get_path(self) -> Path:
        return self.path

    @staticmethod
    def get_active_namespace() -> Optional[str]:
        if CURRENT_NS_PATH.exists() and CURRENT_NS_PATH.is_symlink():
            return Path(os.readlink(CURRENT_NS_PATH)).name

        return None

    def get_namespace_paths(self) -> List[Path]:
        namespaces = []

        for namespace in self.path.iterdir():
            if namespace.is_dir() and not namespace.is_symlink():
                namespaces.append(namespace)

        return namespaces
