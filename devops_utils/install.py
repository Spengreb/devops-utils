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

"""Implements installation process for the devops-utils image.

The main function here is :py:func:`install` which implements the
installation process.

The :py:class:`Replacer`, used from within :py:func:`install`,
implements a lightweight preprocessing/templating process, thanks to
which the external runner can be used as-is when installed as well as
directly from source.
"""

from __future__ import print_function

import argparse
import re
import os
import shutil
import sys
import textwrap

from pkgutil import find_loader
from subprocess import check_call, CalledProcessError

from devops_utils import PROGS, plugin

string_types = str
if sys.version_info[0] == 2:
    string_types = basestring


__all__ = ('install', 'Replacer')


class InvalidOperator(Exception):
    """Invalid operation passed through Replacer."""


class Replacer(object):
    """Used to insert/replace chunks of code in a stream of lines.

    This is used to embed some values into the runner script (as it
    doesn't have access to them from outside a container) when
    installing it on the host system.

    Iterating through the object will yield lines from the input with
    lines containing a special marker replaced.  The marker format is
    ``##INIT:OPERATOR[:PARAM]##`` and should be followed by a newline.

    The ``OPERATOR`` can be:
     - ``MODULE``: then ``PARAM`` specifies a python module whose
       contents should be inserted instead of the original line
     - ``PLUGINS``: then ``PARAM`` specifies type of plugins to be
       included instead of the original line
     - ``SUPPRESS``: supresses the line from output (no parameter)
     - ``VAR``: then ``PARAM`` specifies name of variable to look up
       and place it's definition in output instead of the original
       line

    Typical usage::

        src = StringIO('FOO = 1  ##INIT:VAR:FOO##\\n')
        for line in Replacer(src, {'FOO': 2}):
            assert line == 'FOO = 2\\n'

    :param iter input: iterator for input lines
    :param dict context: look up variables to be replaced in this dict
    """
    RE_MARKER = re.compile('##INIT:([^#]+)##$')
    "Regex for matching the marker."

    def __init__(self, input, context):
        self.input = input
        self.context = context

    def handle_module(self, mod):
        l = find_loader(mod)
        n = getattr(l, 'fullname', getattr(l, 'name', None))
        return l.get_source(n)

    def handle_plugins(self, type_):
        for fn in plugin.get_plugins('runner'):
            with open(fn) as fobj:
                for line in fobj:
                    yield line
        else:
            yield ''

    def handle_suppress(self):
        return ''

    def handle_var(self, var):
        return '{} = {!r}\n'.format(var, self.context[var])

    def __iter__(self):
        for line in self.input:
            match = self.RE_MARKER.search(line.rstrip())
            if match:
                op, _, param = match.group(1).partition(':')
                try:
                    func = getattr(self, 'handle_{}'.format(op.lower()))
                except AttributeError:
                    raise InvalidOperator(op)
                param = (param,) if param else ()  # for parameterless handlers
                line = func(*param)
            if isinstance(line, string_types):
                yield line
            else:
                for generated in line:
                    yield generated


def install(args):
    """Install a runner and shortcuts to all supported programs.

    The runner will be installed as ``devops-utils`` script in a
    directory from host mounted at ``/target``.  The links to all
    included programs will be created in the same directory, pointing
    to ``devops-utils``.

    The runner will execute the command it's run as (or passed as
    first parameter if executed as ``devops-utils``) via docker run.

    :param list args: command line arguments
    """
    parser = argparse.ArgumentParser(prog='install',
                                     description=install.__doc__)
    parser.add_argument(
        '--image-name', help=('name of docker image to use when running '
                              'commands via runner (def: %(default)s)'))
    parser.add_argument('--no-links', action='store_true',
                        help='only install the runner, skip the symlinks')
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
    with open('external_runner.py', 'r') as sfobj,\
            open('/target/devops-utils', 'w') as dfobj:
        for line in Replacer(sfobj, replacements):
            dfobj.write(line)
    shutil.copystat('external_runner.py', '/target/devops-utils')

    if args.no_links:
        print('skipping links')
        return

    print('installing links ... ', end='')
    for prog in PROGS:
        link = os.path.join('/target', prog)
        print(' {}'.format(prog), end='')
        if os.path.exists(link):
            print(' (skip)', end='')
        else:
            os.symlink('devops-utils', link)
    print('')
