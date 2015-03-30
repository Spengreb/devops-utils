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

import pytest

import devops_utils

from conftest import create_plugin


class TestLoadPlugins(object):
    def test_get_plugins(self, plugin_dir):
        create_plugin('init', 'test1', 'FOO = 1\n')
        create_plugin('init', 'test2', 'BAR = 2\n')

        from devops_utils import plugin
        lst = plugin.get_plugins('init')

        assert lst == ('./init_plugins/test1.py', './init_plugins/test2.py')

    def test_load(self, plugin_dir):
        create_plugin('init', 'test', 'BAR = FOO\nFOO = 2\n')

        from devops_utils import plugin
        ctx = {'FOO': 1}
        plugin.load_plugins('init', ctx)

        assert ctx['FOO'] == 2
        assert 'BAR' in ctx and ctx['BAR'] == 1
