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

import argparse
import re
import os
import shutil
import textwrap

from subprocess import check_call, CalledProcessError


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
    replacement_var_marker = re.compile('##INIT_VAR:([^#]+)##$')
    with open('external-runner', 'r') as sfobj,\
         open('/target/devops-utils', 'w') as dfobj:
        for line in sfobj:
            replacement_var = replacement_var_marker.search(line.rstrip())
            if replacement_var:
                var = replacement_var.group(1)
                line = '{} = {!r}\n'.format(var, replacements[var])
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
