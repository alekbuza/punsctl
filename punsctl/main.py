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
import os
import sys
from pathlib import Path
from typing import List, Tuple

from punsctl.exceptions import main_exception_handler
from punsctl.namespace import Namespace
from punsctl.rootspace import RootSpace
from punsctl.sgetopt import sgetopt
from punsctl.static import (
    DEFAULT_ROOTSPACE_PATH,
    DEFAULT_SYMLINK_PATH,
    SGETOPT_STRING,
    USAGE,
)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(message)s"))

logger = logging.getLogger()
logger.addHandler(handler)


@main_exception_handler
@sgetopt(args=sys.argv[1:], optstring=SGETOPT_STRING)
def main(opts: List[Tuple], argv: List[str]) -> None:
    if len(opts) == 0:
        sys.exit(USAGE)

    opt_list = False

    opt_root_path = os.environ.get("NS_ROOT", DEFAULT_ROOTSPACE_PATH)
    opt_symlink_path = os.environ.get("NS_SYMLINK", DEFAULT_SYMLINK_PATH)
    opt_activate = None
    opt_create = None
    opt_delete = None
    opt_deactivate = False
    opt_verbose = False

    verbose_level = 0

    for opt, arg in opts:
        if opt == "-h":
            sys.exit(USAGE)

        elif opt == "-v":
            opt_verbose = True
            verbose_level += 1

        elif opt == "-l":
            opt_list = True

        elif opt == "-d":
            opt_deactivate = True

        elif opt == "-r":
            opt_root_path = arg if arg is not None else sys.exit(USAGE)

        elif opt == "-s":
            opt_symlink_path = arg if arg is not None else sys.exit(USAGE)

        elif opt == "-n":
            opt_create = arg if arg is not None else sys.exit(USAGE)

        elif opt == "-x":
            opt_delete = arg if arg is not None else sys.exit(USAGE)

        elif opt == "-a":
            opt_activate = arg if arg is not None else sys.exit(USAGE)

        else:
            sys.exit(USAGE)

    if opt_verbose:
        if verbose_level >= 1:
            logger.setLevel(logging.DEBUG)
            logging.debug(f"debug: sgetopt opts: {opts}")
            logging.debug(f"debug: sgetopt argv: {argv}")

    root_space = RootSpace(
        path=Path(opt_root_path), symlink_path=Path(opt_symlink_path)
    )

    root_space.check()

    if opt_list:
        for namespace in root_space.get_all_ns_paths():
            ns = Namespace(
                name=namespace.name,
                root_space=root_space,
            )

            sys.stdout.write(
                f"{namespace.name} ({namespace.absolute()}) "
                f"{'active' if ns.active() else ''}\n"
            )

    elif opt_create is not None:
        ns = Namespace(name=opt_create, root_space=root_space)

        ns.create()
        sys.stdout.write(f"info: {opt_create} created\n")

    elif opt_delete is not None:
        ns = Namespace(name=opt_delete, root_space=root_space)

        ns.remove()
        sys.stdout.write(f"info: {opt_delete} removed\n")

    elif opt_activate is not None:
        ns = Namespace(name=opt_activate, root_space=root_space)

        ns.activate()
        sys.stdout.write(f"info: {opt_activate} activated\n")

    elif opt_deactivate:
        for namespace in root_space.get_all_ns_paths():
            ns = Namespace(name=namespace.name, root_space=root_space)
            ns.deactivate()

        sys.stdout.write("info: namespaces are deactivated successfully\n")

    else:
        sys.exit(USAGE)
