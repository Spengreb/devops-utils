#!/usr/bin/env python
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


import logging
import shlex

from subprocess import check_output


def dm_env(script):
    """Yield (var, value) pairs for environment variables for docker machine.

    :param str script: output of ``docker-machine env`` (sh script
                       snippet exporting environment variables)
    """
    for line in script.splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        var, value = shlex.split(line)[1].split('=', 1)
        logging.debug('dm out line: %r, var: %s, value: %r', line, var, value)
        yield var, value

@initfunc
def init_dm(prog, args):
    if not 'ACTIVE_DM' in os.environ:
        return
    # parse ``docker-machine env`` output and inject variables into own
    # environment; this avoids the need for wrapping prog+args in
    # additional shell invocation
    cmd = ['docker-machine', 'env', os.environ['ACTIVE_DM']]
    logging.debug('run: %s', ' '.join(cmd))
    for var, value in dm_env(check_output(cmd)):
        os.environ[var] = value
