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

"""Tests for `devops_utils.install` module."""

import os

import pytest

import devops_utils

from .conftest import create_plugin
from devops_utils import install

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


contents = [
    # (input, expected)
    (
        '''\
#!/usr/bin/python
import os
PROGS = ()  ##INIT:VAR:PROGS##
DOCKER_IMAGE = 'gimoh/devops-utils'  ##INIT:VAR:DOCKER_IMAGE##
FOO = 0
''',
        '''\
#!/usr/bin/python
import os
PROGS = ('foo', 'bar')
DOCKER_IMAGE = 'test/devops-utils'
FOO = 0
'''
    ),
    (
        '''FOO ##INIT:MODULE:devops_utils.test.init_module_test##''',
        '''BAR = 1\n'''
    ),
    (
        'FOO  ##INIT:SUPPRESS##\n',
        ''
    ),
]

class TestReplacer(object):
    @pytest.mark.parametrize('input,expected', contents)
    def test_replace(self, input, expected):
        input = StringIO(input)
        context = {'PROGS': ('foo', 'bar'), 'DOCKER_IMAGE': 'test/devops-utils'}
        output = ''.join(list(install.Replacer(input, context)))
        assert output == expected

    def test_replace_plugins(self, plugin_dir):
        create_plugin('runner', 'test1', 'FOO = 2\n')
        create_plugin('runner', 'test2', 'BAR = 1\n')

        input = StringIO('_src_load_plugins()  ##INIT:PLUGINS:runner##\n')
        expected = 'FOO = 2\nBAR = 1\n'
        output = ''.join(list(install.Replacer(input, {})))
        assert output == expected
