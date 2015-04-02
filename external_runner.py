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

"""The external runner for the devops-utils image.

Essentially wraps ``docker run -it --rm devops-utils``, providing
options to make the usage more convenient.

The :py:func:`main` here is the entrypoint of the devops-utils image
runner program.  It parses the arguments and executes ``docker run``
with appropriate arguments.

:py:func:`argparse_builder` is a decorator that registers a function to
be executed before argument parsing and can be used to add/modify
options, change default values, etc.

:py:func:`docker_run_builder` is a decorator that registers a function
to be executed after argument parsing to modify the final command that
will be run.

:py:class:`DockerRunCommand` is a helper object encapsulating various
arguments which can be modified by the functions decorated with
:py:func:`docker_run_builder`.
"""

from __future__ import print_function

import argparse
import logging
import os
import sys
import subprocess


PROGS = ()  ##INIT:VAR:PROGS##
DOCKER_IMAGE = 'gimoh/devops-utils'  ##INIT:VAR:DOCKER_IMAGE##


class DockerRunCommand(object):
    """Encapsulates components of a docker run command.

    The components (exposed as corresponding instance attributes) are:

    .. py:attribute:: docker_args
       (list) arguments for ``docker run``

    .. py:attribute:: prog
       (str) program to run inside the container

    .. py:attribute:: prog_args
       (list) arguments to the above program

    All of the above are also accepted as constructor parameters.  All
    of them can also be modified directly to affect the final command.

    Exposes a property :py:meth:`cmd` which returns a fully assembled
    list of docker command and arguments.
    """
    def __init__(self, prog, prog_args, docker_args=None):
        self.docker_args = docker_args if docker_args else []
        self.prog = prog
        self.prog_args = list(prog_args)

    def __repr__(self):
        return '{}(docker_args={!r}, prog={!r}, prog_args={!r})'.format(
            self.__class__.__name__,
            self.docker_args, self.prog, self.prog_args)

    def __str__(self):
        return '{}<cmd: "{}">'.format(
            self.__class__.__name__, ' '.join(self.cmd))

    @property
    def cmd(self):
        """Return a fully assembled list of docker run command and arguments.

        :returns: docker run command and arguments; list suitable for
                  passing to :py:class:`subprocess.Popen`
        :rtype: list
        """
        cmd = ['docker', 'run']
        cmd.extend(self.docker_args)
        cmd.extend([DOCKER_IMAGE, self.prog])
        cmd.extend(self.prog_args)
        return cmd

from devops_utils.builders import *  ##INIT:MODULE:devops_utils.builders##
argparse_builders = Builders()
docker_run_builders = Builders()

argparse_builder = argparse_builders.append
"""Register decorated function as :py:class:`ArgumentParser` instance builder.

These builders are executed before argument parsing and can be used to
add/modify options, change default values, etc.

The function signature should be:

.. py:function:: func(parser : argparse.ArgumentParser) -> None

   :param argparse.ArgumentParser parser: parser to modify
"""

docker_run_builder = docker_run_builders.append
"""Register decorated function as ``docker run`` command builder.

These builders are executed after argument parsing to modify the final
command that will be run (either ``docker run`` or the program inside
the container).

The function signature should be:

.. py:function:: func(args : argparse.Namespace, docker_run : DockerRunCommand) -> None

   The function can modify ``docker_run`` object directly to affect the
   final command that will be executed.

   :param argparse.Namespace args:
       arguments and options passed to the runner itself
   :param DockerRunCommand docker_run:
       object encapsulating arguments to ``docker_run`` and the command
       to run inside the container
"""

@argparse_builder
def argparse_base(parser):
    self_name = os.path.basename(sys.argv[0])
    if self_name in ('external-runner', 'devops-utils'):
        parser.add_argument('prog', help='program to run (e.g.: install, {})'.
                                        format(', '.join(PROGS)))
    else:
        parser.set_defaults(prog=self_name)

    parser.add_argument('++debug', action='store_true',
                        help='enable debugging output')
    parser.add_argument('+O', '++docker-opt', action='append',
                        help='pass specified long-style option to docker run')
    parser.add_argument('++help', action='store_true',
                        help='show this help message and exit')
    parser.set_defaults(docker_opt=[])

@docker_run_builder
def docker_run_base(args, docker_run):
    docker_run.docker_args.extend('-i -t --rm'.split())
    if args.debug:
        docker_run.docker_args.extend(('-e', 'DEVOPS_UTILS_DEBUG=true'))

@docker_run_builder
def docker_run_opts(args, docker_run):
    docker_run.docker_args.extend(['--%s' % opt for opt in args.docker_opt])

from devops_utils.plugin import load_plugins  ##INIT:SUPPRESS##
BASEDIR=os.path.dirname(__file__)  ##INIT:SUPPRESS##
load_plugins('runner', globals(), basedir=BASEDIR)  ##INIT:PLUGINS:runner##

def main(args=sys.argv[1:]):
    """Run a program in a devops-utils container."""
    logging.basicConfig(
        format='(%(module)s:%(funcName)s:%(lineno)s) %(message)s',
        level=logging.INFO)

    parser = argparse.ArgumentParser(description=main.__doc__, add_help=False,
                                     prefix_chars='+')
    argparse_builders(parser)
    args, prog_args = parser.parse_known_args(args)

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug('%r', {'args': args, 'prog_args': prog_args})

    if args.help:
        parser.print_help()
        parser.exit()

    docker_run = DockerRunCommand(args.prog, prog_args)
    docker_run_builders(args, docker_run)
    logging.debug('%r', {'docker_run': docker_run})
    logging.debug('%s', docker_run)

    subprocess.check_call(docker_run.cmd)


if __name__ == '__main__':
    main()
