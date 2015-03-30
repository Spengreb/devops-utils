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

"""Tests for `devops_utils.plugin` module."""

import os

import pytest

import devops_utils


class TestLoadPlugins(object):
    def create_plugin(self, type_, name, contents):
        dir = '{}_plugins'.format(type_)
        if not os.path.isdir(dir):
            os.mkdir(dir)
        with open(os.path.join(dir, '{}.py'.format(name)), 'w') as fobj:
            fobj.write(contents)

    def test_load(self, monkeypatch, tmpdir):
        monkeypatch.setattr(devops_utils, 'PLUGIN_DIR', '.')
        monkeypatch.chdir(tmpdir)

        self.create_plugin('init', 'test', 'BAR = FOO\nFOO = 2\n')

        from devops_utils import plugin
        ctx = {'FOO': 1}
        plugin.load_plugins('init', ctx)

        assert ctx['FOO'] == 2
        assert 'BAR' in ctx and ctx['BAR'] == 1
