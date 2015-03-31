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
import os

from devops_utils import PLUGIN_DIR


# PY3 compat: execfile removed
try:
    execfile
except NameError:
    import tokenize

    def execfile(fn, globals):
        with tokenize.open(fn) as fobj:
            exec(fobj.read(), globals)


def get_plugins(type_, basedir=PLUGIN_DIR):
    """Return a tuple of filenames of plugins of a given type.

    :param str type_: type of plugins, i.e. init or runner
    :param str basedir: base directory to look up plugins in
    """
    dir = os.path.join(basedir, type_ + '_plugins')
    if not os.path.isdir(dir):
        return ()
    return tuple(sorted(glob.glob(os.path.join(dir, '*.py'))))


def load_plugins(type_, globals, basedir=PLUGIN_DIR):
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
    for fn in get_plugins(type_, basedir):
        execfile(fn, globals)
