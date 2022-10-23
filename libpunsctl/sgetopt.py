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

from typing import Any, List

__all__ = ["sgetopt"]


def sgetopt(args: List[str], optstring: str) -> Any:
    """
    Parses command line options and parameter list.
    args is the argument list to be parsed, without the leading reference
    to the running program. Typically, this means "sys.argv[1:]".
    optstring is the string of option letters that the script wants to
    recognize, with options that require an argument followed by a
    colon (i.e., the same format that Unix getopt() uses).
    """

    def func(f):
        def wrapper():
            def is_opt(opt: str) -> bool:
                """
                Check if the argument is an option
                """
                if len(opt) == 2 and opt.startswith("-"):
                    return True
                return False

            def req_arg(opt: str) -> bool:
                """
                Check if the option requires an argument
                """
                if opt.isalpha():
                    return optstring[optstring.find(opt) + 1] == ":"
                return False

            opts, argv = [], []

            for _ in range(len(args)):
                arg, arg_ix = args[_], _

                if is_opt(arg):
                    n_arg = arg_ix + 1

                    if len(args) <= n_arg:
                        opts.append((arg, None))

                    elif req_arg(arg[1]) and not is_opt(args[n_arg]):
                        opts.append((arg, args[n_arg]))

                    else:
                        opts.append((arg, ""))

                else:
                    p_arg = arg_ix - 1

                    if is_opt(args[p_arg]):
                        if not req_arg(args[p_arg][1]):
                            argv.append(arg)

                    else:
                        argv.append(arg)

            f(opts, argv)

        return wrapper

    return func
