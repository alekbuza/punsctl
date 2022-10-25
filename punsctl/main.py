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

import sys
from pathlib import Path
from typing import List, Tuple

from punsctl.namespace import Namespace, NamespaceException
from punsctl.rootspace import RootSpace, RootSpaceException
from punsctl.sgetopt import sgetopt
from punsctl.static import DEFAULT_ROOT_PATH, DEFAULT_SYMLINK_PATH, USAGE


@sgetopt(args=sys.argv[1:], optstring="hlxr:s:n:d:a:")
def main(opts: List[Tuple], argv: List[str]) -> None:
    if len(opts) == 0:
        sys.exit(USAGE)

    opt_list = False
    opt_root_path = DEFAULT_ROOT_PATH
    opt_symlink_path = DEFAULT_SYMLINK_PATH
    opt_create = None
    opt_delete = None
    opt_activate = None
    opt_deactivate = False

    for opt, arg in opts:
        if opt == "-h":
            sys.exit(USAGE)

        elif opt == "-l":
            opt_list = True

        elif opt == "-x":
            opt_deactivate = True

        elif opt == "-r":
            opt_root_path = arg if arg is not None else sys.exit(USAGE)

        elif opt == "-s":
            opt_symlink_path = arg if arg is not None else sys.exit(USAGE)

        elif opt == "-n":
            opt_create = arg if arg is not None else sys.exit(USAGE)

        elif opt == "-d":
            opt_delete = arg if arg is not None else sys.exit(USAGE)

        elif opt == "-a":
            opt_activate = arg if arg is not None else sys.exit(USAGE)

        else:
            sys.exit(USAGE)

    try:
        root_space = RootSpace(
            path=Path(opt_root_path), symlink_path=Path(opt_symlink_path)
        )

    except RootSpaceException as exc:
        sys.exit(f"root error: {exc.message}")

    if opt_list:
        for namespace in root_space.get_all_ns_paths():
            try:
                ns = Namespace(
                    name=namespace.name,
                    root_space=root_space,
                )

                sys.stdout.write(
                    f"{namespace.name} ({namespace.absolute()}) "
                    f"{'active' if ns.active() else ''}\n"
                )
            except NamespaceException as exc:
                sys.exit(f"namespace error: {exc.message}")

    elif opt_create is not None:
        ns = Namespace(name=opt_create, root_space=root_space)

        try:
            ns.create()
            sys.stdout.write(f"info: {opt_create} created\n")

        except NamespaceException as exc:
            sys.exit(f"namespace error: {exc.message}")

    elif opt_delete is not None:
        ns = Namespace(name=opt_delete, root_space=root_space)

        try:
            ns.remove()
            sys.stdout.write(f"info: {opt_delete} removed\n")

        except NamespaceException as exc:
            sys.exit(f"namespace error: {exc.message}")

    elif opt_activate is not None:
        ns = Namespace(name=opt_activate, root_space=root_space)

        try:
            ns.activate()
            sys.stdout.write(f"info: {opt_activate} activated\n")

        except NamespaceException as exc:
            sys.exit(f"namespace error: {exc.message}")

    elif opt_deactivate:
        for namespace in root_space.get_all_ns_paths():
            ns = Namespace(name=namespace.name, root_space=root_space)
            ns.deactivate()

        sys.stdout.write("info: namespaces are deactivated successfully\n")

    else:
        sys.stdout.write(USAGE)
