### -*- coding: utf-8 -*-
###
###  Copyright (C) 2016 Peter Williams <pwil3058@gmail.com>
###
### This program is free software; you can redistribute it and/or modify
### it under the terms of the GNU General Public License as published by
### the Free Software Foundation; version 2 of the License only.
###
### This program is distributed in the hope that it will be useful,
### but WITHOUT ANY WARRANTY; without even the implied warranty of
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.
###
### You should have received a copy of the GNU General Public License
### along with this program; if not, write to the Free Software
### Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import os
import re
import subprocess

from ..lib import runext

def check_ignored(paths):
    return subprocess.run(["git", "check-ignore"] + paths, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def is_ignored_path(path):
    return check_ignored([path]).returncode == 0

def get_recognized_subdirs(base_dir_path="."):
    path_iter = (os.path.join(dp, sdn) for dp, sdns, _fns in os.walk(base_dir_path) for sdn in sdns)
    return [path for path in path_iter if check_ignored([path]).returncode == 1 and not path.startswith("./.git")]

_SUBMODULE_PATH_RE = re.compile(r"[a-fA-F0-9]+\s+(\S+)(\s+\S*)?")
def get_submodule_paths():
    text = runext.run_get_cmd(["git", "submodule", "status", "--recursive"], default="")
    return [_SUBMODULE_PATH_RE.match(line[1:]).groups()[0] for line in text.splitlines()]
