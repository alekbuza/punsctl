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
import sys
from functools import wraps


class NamespaceException(Exception):
    def __init__(self, message):
        self.message = message


class RootSpaceException(Exception):
    def __init__(self, message):
        self.message = message


def main_exception_handler(func):
    @wraps(func)
    def inner_func(*args, **kwargs):
        try:
            func(*args, **kwargs)

        except RootSpaceException as exc:
            sys.exit(f"rootspace error: {exc.message}")

        except NamespaceException as exc:
            sys.exit(f"namespace error: {exc.message}")

        except Exception as exc:
            sys.exit(f"unexpected error: {exc}")

    return inner_func


def fs_ops_exception_handler(func):
    @wraps(func)
    def inner_func(*args, **kwargs):
        try:
            func(*args, **kwargs)

        except PermissionError as exc:
            logging.warning(
                f"warning: {exc.strerror}: {exc.filename} -> {exc.filename2}"
            )

        except FileExistsError as exc:
            logging.warning(
                f"warning: {exc.strerror}: {exc.filename} -> {exc.filename2}"
            )

        except Exception as exc:
            logging.critical(f"unexpected error: {exc}")

    return inner_func
