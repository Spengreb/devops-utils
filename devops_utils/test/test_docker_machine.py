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

"""Tests for `docker_machine` plugin."""

import textwrap

import pytest

from devops_utils import init, plugin


@pytest.fixture
def dm_env():
    ctx = {'initfunc': init.initfunc}
    plugin.load_plugins('init', ctx, pattern='docker_machine')
    return ctx['dm_env']


class TestDockerMachinePlugin(object):
    def test_dm_env_comment(self, dm_env):
        dm_out = '# this is = a comment'

        assert list(dm_env(dm_out)) == []

    def test_dm_env_vars(self, dm_env):
        dm_out = textwrap.dedent('''
            export DOCKER_TLS_VERIFY="1"
            export DOCKER_CERT_PATH="/app=dm/machines/foo"
            ''')

        assert list(dm_env(dm_out)) == [
            ('DOCKER_TLS_VERIFY', '1'),
            ('DOCKER_CERT_PATH', '/app=dm/machines/foo'),
            ]
