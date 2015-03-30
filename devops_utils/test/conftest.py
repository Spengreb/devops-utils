#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2015 gimoh
#
# This file is part of devops-utils.
#
# devops-utils is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# devops-utils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with devops-utils.  If not, see <http://www.gnu.org/licenses/>.

"""Common fixtures and settings for `devops_utils` tests."""

import os

import pytest

import devops_utils


@pytest.fixture
def plugin_dir(monkeypatch, tmpdir):
    monkeypatch.setattr(devops_utils, 'PLUGIN_DIR', '.')
    monkeypatch.chdir(tmpdir)
    return tmpdir

def create_plugin(type_, name, contents):
    """Create a plugin for tests.

    The plugins are created relative to the current directory.

    :param str type_: type of plugins, i.e. init or runner
    :param str name: name of the plugin (without extension)
    :param str contents: contents of the plugin file
    """
    dir = '{}_plugins'.format(type_)
    if not os.path.isdir(dir):
        os.mkdir(dir)
    with open(os.path.join(dir, '{}.py'.format(name)), 'w') as fobj:
        fobj.write(contents)
