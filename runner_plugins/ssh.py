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

@argparse_builder
def argparse_ssh_key(parser):
    parser.add_argument('++key', help='SSH key to use')

@docker_run_builder
def docker_run_ssh_agent(args, docker_run):
    if 'SSH_AUTH_SOCK' not in os.environ:
        return
    docker_run.docker_args.extend([
        '-v', '{}:/tmp/ssh_agent'.format(os.environ['SSH_AUTH_SOCK']),
        ])

@docker_run_builder
def docker_run_ssh_key(args, docker_run):
    if not args.key:
        return
    key = os.path.join(os.path.expanduser('~/.ssh'), args.key)
    # can't mount it directly as ~/.ssh/id_rsa as ssh won't accept it without
    # correct permissions; docker-init will do the rest
    docker_run.docker_args.extend([
        '-v', '{}:/var/local/ssh.key'.format(key),
        ])

@docker_run_builder
def docker_run_ssh_config(args, docker_run):
    src = os.path.join(os.path.expanduser('~/.ssh'), 'config')
    if not os.path.exists(src):
        return
    docker_run.docker_args.extend([
        '-v', '{}:/var/local/ssh_config'.format(src),
        ])
