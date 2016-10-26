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

"""Provide an interface for the CLI to access git source control"""

__all__ = []
__author__ = "Peter Williams <pwil3058@gmail.com>"

from ..bab import runext

from ..patch_diff import patchlib

def index_is_empty():
    stdout = runext.run_get_cmd(["git", "status", "--porcelain", "--untracked-files=no"])
    for line in stdout.splitlines():
        if line[0] != " ":
            return False
    return True

class Interface:
    name = "git"
    @staticmethod
    def __getattr__(attr_name):
        if attr_name == "is_available":
            try:
                return runext.run_cmd(["git", "version"]).is_ok
            except OSError as edata:
                if edata.errno == errno.ENOENT:
                    return False
                else:
                    raise
        if attr_name == "in_valid_pgnd": return runext.run_cmd(["git", "config", "--local", "-l"]).is_ok
        raise AttributeError(attr_name)
    @staticmethod
    def dir_is_in_valid_pgnd(dir_path=None):
        if dir_path:
            orig_dir_path = os.getcwd()
            os.chdir(dir_path)
        result = runext.run_cmd(["git", "config", "--local", "-l"])
        if dir_path:
            os.chdir(orig_dir_path)
        return result.is_ok
    @classmethod
    def do_import_patch(cls, patch_filepath):
        ok_to_import, msg = cls.is_ready_for_import()
        if not ok_to_import:
            return CmdResult.error(stderr=msg)
        epatch = patchlib.Patch.parse_text_file(patch_filepath)
        description = epatch.get_description()
        if not description:
            return CmdResult.error(stderr="Empty description")
        result = runext.run_cmd(["git", "apply", patch_filepath])
        if not result.is_less_than_error:
            return result
        result = runext.run_cmd(["git", "add"] + epatch.get_file_paths(1))
        if not result.is_less_than_error:
            return result
        return runext.run_cmd(["git", "commit", "-q", "-m", description])
    @staticmethod
    def get_clean_contents(file_path):
        return runext.run_get_cmd(["git", "cat-file", "blob", "HEAD:{}".format(file_path)], do_rstrip=False, default=None, decode_stdout=False)
    @staticmethod
    def get_files_with_uncommitted_changes(files=None):
        cmd = ["git", "status", "--porcelain", "--untracked-files=no",]
        if files:
            cmd += files
        return [line[3:] for line in runext.run_get_cmd(cmd).splitlines()]
    @staticmethod
    def is_ready_for_import():
        return (True, "") if index_is_empty() else (False, _("Index is NOT empty\n"))

SCM = Interface()
from ..scm import ifce as scm_ifce
scm_ifce.add_back_end(SCM)
