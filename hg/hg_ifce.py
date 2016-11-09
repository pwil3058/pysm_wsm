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

"""Provide an interface for the CLI to access Mercurial (hg) source control"""

__all__ = []
__author__ = "Peter Williams <pwil3058@gmail.com>"

import re

from ..bab import runext

from ..patch_diff import patchlib

NOSUCH_RE = re.compile(_("^.*: No such file or directory$\n?"), re.M)

class Interface:
    name = "hg"
    @staticmethod
    def __getattr__(attr_name):
        if attr_name == "is_available":
            try:
                return runext.run_cmd(["hg", "version"]).is_ok
            except OSError as edata:
                if edata.errno == errno.ENOENT:
                    return False
                else:
                    raise
        if attr_name == "in_valid_wspce": return runext.run_cmd(["hg", "root"]).is_ok
        raise AttributeError(attr_name)
    @staticmethod
    def dir_is_in_valid_pgnd(dir_path=None):
        if dir_path:
            orig_dir_path = os.getcwd()
            os.chdir(dir_path)
        result = runext.run_cmd(["hg", "root"])
        if dir_path:
            os.chdir(orig_dir_path)
        return result.is_ok
    @classmethod
    def do_import_patch(cls, patch_file_path):
        ok_to_import, msg = cls.is_ready_for_import()
        if not ok_to_import:
            return CmdResult.error(stderr=msg)
        return runext.run_cmd(["hg", "import", "-q", patch_file_path])
    @staticmethod
    def get_clean_contents(file_path):
        return runext.run_get_cmd(["hg", "cat", file_path], do_rstrip=False, default=None, decode_stdout=False)
    @staticmethod
    def get_files_with_uncommitted_changes(files=None):
        cmd = ["hg", "status", "-mardn"] + (list(files) if files else ["."])
        return runext.run_get_cmd(cmd, sanitize_stderr=lambda x: NOSUCH_RE.sub("", x)).splitlines()
    @staticmethod
    def is_ready_for_import():
        if runext.run_cmd(["hg", "qtop"]).is_ok:
            return (False, _("There are \"mq\" patches applied."))
        result = runext.run_cmd(["hg", "parents", "--template", "{rev}\\n"])
        if not result.is_ok:
            return (False, result.stdout + result.stderr)
        elif len(result.stdout.splitlines()) > 1:
            return (False, _("There is an incomplete merge in progress."))
        return (True, "")

SCM = Interface()
from ..scm import scm_ifce
scm_ifce.add_back_end(SCM)
