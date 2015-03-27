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

import glob
import grp
import os
import pwd
import shutil

from devops_utils import PLUGIN_DIR


def load_plugins(type_, globals):
    """Load plugins of given type.

    The plugin files are looked up in ${type}_plugins directory under
    PLUGIN_DIR.  They are execfile()d in the global namespace of the
    module.

    The reason the plugins are exec'ed and not imported is so that it
    is easier for derived images to add plugins, as they can just drop
    files into a known directory.

    :param str type_: type of plugins, i.e. init or runner
    :param dict globals: as for execfile()
    """
    dir = os.path.join(PLUGIN_DIR, type_ + '_plugins')
    if not os.path.isdir(dir):
        return
    for fn in glob.glob(os.path.join(dir, '*.py')):
        execfile(fn, globals)

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

def run(prog, args):
    """Run the specified program."""
    load_plugins('init', globals())
    init_ssh_agent()
    init_ssh_key()
    init_ssh_config()
    os.execvp(prog, (prog,) + tuple(args))
