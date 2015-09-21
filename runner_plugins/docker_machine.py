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
def argparse_dm(parser):
    parser.add_argument('++dm', help=('docker machine to activate before '
                                      'running the program'))

@docker_run_builder
def docker_run_dm(args, docker_run):
    if not args.dm:
        return
    docker_run.docker_args.extend([
        '-e', 'ACTIVE_DM={}'.format(args.dm),
    ])
