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


@initfunc
def init_ssh_agent(prog, args):
    if not os.path.exists('/tmp/ssh_agent'):
        return
    os.environ['SSH_AUTH_SOCK'] = '/tmp/ssh_agent'


@initfunc
def init_ssh_key(prog, args):
    install_file_if_exists('/var/local/ssh.key', '/root/.ssh/id_rsa',
                           'root', 'root', 0o600)


@initfunc
def init_ssh_config(prog, args):
    install_file_if_exists('/var/local/ssh_config', '/root/.ssh/config',
                           'root', 'root', 0o600)
