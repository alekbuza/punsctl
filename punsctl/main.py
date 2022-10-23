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

USAGE = """
punsctl <options>

options:
    -h                  Help menu
    -p                  Root path
    -l                  List namespaces
    -c <namespace>      Create namespace
    -r <namespace>      Remove namespace
    -a <namespace>      Activate namespace
    -d                  Deactivate namespaces
"""

MSG_LIST_NS = "{name} ({path}) {active}"


def usage():
    sys.exit(USAGE)


@sgetopt(args=sys.argv[1:], optstring="hplc:r:a:d")
def main(opts: List[Tuple], argv: List[str]) -> None:
    if len(opts) == 0:
        usage()

    opt_root_path = None
    opt_list = False
    opt_create = None
    opt_remove = None
    opt_activate = None
    opt_deactivate = False

    for opt, arg in opts:
        if opt == "-h":
            usage()

        elif opt == "-p":
            opt_root_path = arg

        elif opt == "-l":
            opt_list = True

        elif opt == "-c":
            opt_create = arg if arg is not None else usage()

        elif opt == "-r":
            opt_remove = arg if arg is not None else usage()

        elif opt == "-a":
            opt_activate = arg if arg is not None else usage()

        elif opt == "-d":
            opt_deactivate = True

        else:
            usage()

    if opt_root_path is not None:
        try:
            root_space = RootSpace(path=Path(opt_root_path))

        except RootSpaceException as exc:
            print(exc.message)
            sys.exit()

    else:
        root_space = RootSpace(path=Path(f"{Path.home()}/.ns"))

    if opt_list:
        for namespace in root_space.get_namespace_paths():
            ns = Namespace(root_space=root_space, name=namespace.name)

            print(
                MSG_LIST_NS.format(
                    name=namespace.name,
                    path=namespace.absolute(),
                    active="active" if ns.active() else "",
                )
            )

    elif opt_deactivate:
        for namespace in root_space.get_namespace_paths():
            ns = Namespace(root_space=root_space, name=namespace.name)
            ns.deactivate()

        print("namespaces are deactivated successfully")

    elif opt_create is not None:
        ns = Namespace(root_space=root_space, name=opt_create)

        try:
            ns.create()
            print(f"{opt_create} created")

        except NamespaceException as exc:
            print(f"error: {exc.message}")

    elif opt_remove is not None:
        ns = Namespace(root_space=root_space, name=opt_remove)

        try:
            ns.remove()

        except NamespaceException as exc:
            print(f"error: {exc.message}")

    elif opt_activate is not None:
        ns = Namespace(root_space=root_space, name=opt_activate)

        try:
            ns.activate()
            print(f"{opt_activate} activated")

        except NamespaceException as exc:
            print(f"error: {exc.message}")

    else:
        usage()