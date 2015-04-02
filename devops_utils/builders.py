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

"""Implements an extension mechanism for devops-utils image.

Basically a list of callables (functions defined by plugins), with a
simple interface to execute them with given parameters.

.. sidebar:: NOTE

   this module should be kept minimal, specifically without importing
   anything else from the devops_utils or any other external package;
   this is because this module is included in the runner, which doesn't
   have access to the package when installed.
"""


class Builders(list):
    """A list of callables."""
    def __call__(self, *args):
        for builder in self:
            builder(*args)
