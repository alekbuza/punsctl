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

SHELL = /bin/sh
BASE_PATH = $(shell pwd)

.PHONY = help build install

.DEFAULT_GOAL = help

help:
	@echo "---------------HELP-----------------"
	@echo "build      - Build punsctl locally"
	@echo "install    - Install punsctl inside a Poetry virtual environment"
	@echo "test       - Run all tests"
	@echo "lint       - Linter"
	@echo "bump_patch - Bump patch version"
	@echo "bump_minor - Bump minor version"
	@echo "bump_major - Bump major version"
	@echo "------------------------------------"

build:
	poetry build

install:
	poetry install

test:
	poetry run pytest

lint:
	isort . --profile black
	black .
	flake8 .
	bandit -r punsctl/

bump_patch:
	poetry version patch

bump_minor:
	poetry version minor

bump_major:
	poetry version major
