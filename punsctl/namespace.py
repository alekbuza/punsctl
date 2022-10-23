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

from punsctl.rootspace import RootSpace
from punsctl.static import CURRENT_NS_PATH, MSG_ANOTHER_NS_ACTIVE

__all__ = ["Namespace", "NamespaceException"]


class NamespaceException(Exception):
    def __init__(self, message):
        self.message = message


class Namespace(object):
    def __init__(
        self,
        name: str,
        root_space: RootSpace,
        symlink_path: Optional[Path] = Path.home(),
    ):
        self.name = name
        self.root_space = root_space
        self.symlink_path = symlink_path

        self.__path = Path(f"{root_space.get_path()}/{name}")

    def create(self) -> None:
        try:
            os.mkdir(self.__path, mode=0o744)

        except OSError as exc:
            raise NamespaceException(message=exc.strerror)

    def remove(self) -> None:
        try:
            if self.exists():
                os.rmdir(self.__path)

        except OSError as exc:
            raise NamespaceException(message=exc.strerror)

    def exists(self) -> bool:
        if not Path(self.__path).exists():
            return False

        return True

    def get_path(self) -> Path:
        return self.__path

    def active(self) -> bool:
        if (
            CURRENT_NS_PATH.exists()
            and Path(os.readlink(CURRENT_NS_PATH)) == self.__path
        ):
            return True

        return False

    def get_name(self) -> str:
        return self.name

    def get_namespace_path(self) -> Path:
        return self.__path

    def __get_sources(self) -> List[Path]:
        sources = []

        for source in self.__path.iterdir():
            if source.name == CURRENT_NS_PATH.name:
                continue
            sources.append(source)

        return sources

    def activate(self) -> None:
        if CURRENT_NS_PATH.exists() and CURRENT_NS_PATH.is_symlink():
            if Path(os.readlink(CURRENT_NS_PATH)) == self.__path:
                pass

            else:
                raise NamespaceException(
                    message=MSG_ANOTHER_NS_ACTIVE.format(
                        name=self.root_space.get_active_namespace()
                    )
                )
        else:
            CURRENT_NS_PATH.symlink_to(self.__path)

        for source in self.__get_sources():
            with Path(f"{self.symlink_path}/{source.name}") as target:
                if target.exists():
                    if target.is_symlink() and Path(os.readlink(target)) == source:
                        continue

                    with target.with_name(f"{target.name}.{self.name}.bak") as backup:
                        if not target.is_symlink():
                            target.rename(backup)

                if not target.is_symlink():
                    target.symlink_to(source)

    def deactivate(self) -> None:
        if CURRENT_NS_PATH.exists() and CURRENT_NS_PATH.is_symlink():
            if Path(os.readlink(CURRENT_NS_PATH)) == self.__path:
                CURRENT_NS_PATH.unlink()

        for source in self.__get_sources():
            with Path(f"{self.symlink_path}/{source.name}") as target:
                if target.exists():
                    if target.is_symlink() and Path(os.readlink(target)) == source:
                        target.unlink()

                    with target.with_name(f"{target.name}.{self.name}.bak") as backup:
                        if backup.exists():
                            backup.rename(target)
