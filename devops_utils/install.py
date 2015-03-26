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

import re


class Replacer(object):
    """Used to insert/replace chunks of code in a stream of lines.

    This is used to embed some values into the runner script (as it
    doesn't have access to them from outside a container) when
    installing it on the host system.
    """
    RE_VAR_MARKER = re.compile('##INIT_VAR:([^#]+)##$')

    def __init__(self, input, context):
        """
        :param input: iterator for input lines
        :param context: look up variables to be replaced in this dict
        """
        self.input = input
        self.context = context

    def __iter__(self):
        for line in self.input:
            replacement_var = self.RE_VAR_MARKER.search(line.rstrip())
            if replacement_var:
                var = replacement_var.group(1)
                line = '{} = {!r}\n'.format(var, self.context[var])
            yield line
