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

from pathlib import Path

import pytest

from punsctl.namespace import Namespace
from punsctl.rootspace import RootSpace


@pytest.fixture
def root_tmpdir(tmpdir):
    path = Path(f"{tmpdir}/.ns")
    path.mkdir(parents=True, exist_ok=True)

    return path


@pytest.fixture
def symlink_tmpdir(tmpdir):
    path = Path(f"{tmpdir}/workspace")
    path.mkdir(parents=True, exist_ok=True)

    return path


@pytest.mark.usefixtures()
def test_single_namespace(root_tmpdir, symlink_tmpdir):
    rs = RootSpace(path=root_tmpdir, symlink_path=symlink_tmpdir)
    ns = Namespace(root_space=rs, name="single_namespace_test")

    assert ns.exists() is False

    ns.create()
    ns.activate()

    assert ns.active() is True
    assert ns.get_path() == Path(f"{root_tmpdir}/{ns.get_name()}")

    assert Path(f"{rs.get_symlink_path()}/.current_ns").is_dir() is True
    assert Path(f"{rs.get_symlink_path()}/.current_ns").is_symlink() is True

    ns.deactivate()
    ns.remove()

    assert ns.exists() is False
