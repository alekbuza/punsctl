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

from pathlib import Path

import pytest

from punsctl.namespace import Namespace


@pytest.mark.usefixtures("root_space")
def test_create_namespace(root_space, tmp_path):
    ns = Namespace(root_space=root_space, name="test")

    ns.create()

    assert ns.get_path() == Path(f"{tmp_path}/{ns.get_name()}")


@pytest.mark.usefixtures("root_space")
def test_delete_namespace(root_space, tmp_path):
    ns = Namespace(root_space=root_space, name="test")

    ns.create()
    assert ns.exists() is True

    ns.remove()
    assert ns.exists() is False
