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
import grp
import logging
import os
import pwd
import shutil
import sys

from devops_utils import PROGS
from devops_utils.builders import Builders
from devops_utils.install import install
from devops_utils.plugin import load_plugins


def install_file(src, dst, owner, group, mode):
    shutil.copy(src, dst)
    uid = pwd.getpwnam(owner).pw_uid
    gid = grp.getgrnam(group).gr_gid
    os.chown(dst, uid, gid)
    os.chmod(dst, mode)


def install_file_if_exists(src, dst, owner, group, mode):
    if not os.path.exists(src):
        return
    install_file(src, dst, owner, group, mode)


initializers = Builders()
initfunc = initializers.append
"""Register function as initializer.

An initializer is executed on startup and can contribute to environment
setup within the container.  The function will be executed with two
arguments: ``prog`` and ``args``.  ``prog`` is the name/path to the
program that will be executed by init.  ``args`` is a list of arguments
it will be executed with.  The ``args`` list may be mutated to affect
the final arguments.
"""


def run(prog, args):
    """Run the specified program."""
    load_plugins('init', globals())
    args = list(args)
    initializers(prog, args)
    logging.debug('%r', {'prog': prog, 'args': args})
    logging.debug('cmd: %s', ' '.join([prog] + args))
    os.execvp(prog, (prog,) + tuple(args))


def main(args=sys.argv[1:]):
    """Run a program in devops-utils container."""
    logging.basicConfig(
        format='(%(module)s:%(funcName)s:%(lineno)s) %(message)s',
        level=logging.INFO if 'DEVOPS_UTILS_DEBUG' not in os.environ else
        logging.DEBUG)

    parser = argparse.ArgumentParser(description=main.__doc__, add_help=False)
    parser.add_argument('prog', help='program to run (e.g.: install, {})'.
                                     format(', '.join(PROGS)))

    args, prog_args = parser.parse_known_args(args)
    logging.debug('%r', {'args': args, 'prog_args': prog_args})

    if args.prog == 'install':
        sys.exit(install(prog_args))

    run(args.prog, prog_args)


if __name__ == '__main__':
    main()
