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

from __future__ import print_function

import argparse
import re
import os
import shutil
import textwrap

from pkgutil import find_loader
from subprocess import check_call, CalledProcessError

from devops_utils import PROGS


class InvalidOperator(Exception):
    """Invalid operation passed through Replacer."""

class Replacer(object):
    """Used to insert/replace chunks of code in a stream of lines.

    This is used to embed some values into the runner script (as it
    doesn't have access to them from outside a container) when
    installing it on the host system.

    Iterating through the object will yield lines from the input with
    lines containing a special marker replaced.  The marker format is
    `##INIT:OPERATOR[:PARAM]##` and should be followed by a newline.

    The `OPERATOR` can be:
     - `MODULE`: `PARAM` specifies a python module whose contents
       should be inserted instead of the original line
     - `VAR`: `PARAM` specifies name of variable to look up and place
       it's definition in output instead of the original line
    """
    RE_MARKER = re.compile('##INIT:([^#]+)##$')

    def __init__(self, input, context):
        """
        :param input: iterator for input lines
        :param context: look up variables to be replaced in this dict
        """
        self.input = input
        self.context = context

    def handle_module(self, mod):
        l = find_loader(mod)
        return l.get_source()

    def handle_var(self, var):
        return '{} = {!r}\n'.format(var, self.context[var])

    def __iter__(self):
        for line in self.input:
            match = self.RE_MARKER.search(line.rstrip())
            if match:
                op, _, param = match.group(1).partition(':')
                try:
                    func = getattr(self, 'handle_{}'.format(op.lower()))
                except AttributeError as e:
                    raise InvalidOperator(op)
                line = func(param)
            yield line

def install(args):
    """Install a runner and shortcuts to all supported programs.

    The runner will execute the command it's run as via docker run.
    """
    parser = argparse.ArgumentParser(prog='install',
                                     description=install.__doc__)
    parser.add_argument(
        '--image-name', help=('name of docker image to use when running '
                              'commands via runner (def: %(default)s)'))
    parser.set_defaults(image_name='gimoh/devops-utils')
    args = parser.parse_args(args)

    try:
        check_call(('mountpoint', '-q', '/target'))
    except CalledProcessError:
        print(textwrap.dedent('''\
            /target is not a mountpoint

            Re-run this image with -v $HOME/.local/bin:/target
            '''))
        return 2

    print('installing runner')
    replacements = {'PROGS': PROGS, 'DOCKER_IMAGE': args.image_name}
    with open('external-runner', 'r') as sfobj,\
         open('/target/devops-utils', 'w') as dfobj:
        for line in Replacer(sfobj, replacements):
            dfobj.write(line)
    shutil.copystat('external-runner', '/target/devops-utils')

    print('installing links ... ', end='')
    for prog in PROGS:
        link = os.path.join('/target', prog)
        print(' {}'.format(prog), end='')
        if os.path.exists(link):
            print(' (skip)', end='')
        else:
            os.symlink('devops-utils', link)
    print('')
