### Copyright (C) 2015 Peter Williams <peter_ono@users.sourceforge.net>
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
import hashlib
import collections

from gi.repository import Pango

from .. import git_utils

from ...bab import runext

from ...gtx import fsdb

from ...bab import utils

class FileStatus:
    UNMODIFIED = '  '
    WD_ONLY_MODIFIED = ' M'
    WD_ONLY_DELETED = ' D'
    MODIFIED = 'M '
    MODIFIED_MODIFIED = 'MM'
    MODIFIED_DELETED = 'MD'
    ADDED = 'A '
    ADDED_MODIFIED = 'AM'
    ADDED_DELETED = 'AD'
    DELETED = 'D '
    DELETED_MODIFIED = 'DM'
    RENAMED = 'R '
    RENAMED_MODIFIED = 'RM'
    RENAMED_DELETED = 'RD'
    COPIED = 'C '
    COPIED_MODIFIED = 'CM'
    COPIED_DELETED = 'CD'
    UNMERGED = 'UU'
    UNMERGED_ADDED = 'AA'
    UNMERGED_ADDED_US = 'AU'
    UNMERGED_ADDED_THEM = 'UA'
    UNMERGED_DELETED = 'DD'
    UNMERGED_DELETED_US = 'DU'
    UNMERGED_DELETED_THEM = 'DA'
    NOT_TRACKED = '??'
    IGNORED = '!!'
    MODIFIED_LIST = [
            # TODO: review order of modified set re directory decoration
            # order is preference order for directory decoration based on contents' states
            WD_ONLY_MODIFIED, WD_ONLY_DELETED,
            MODIFIED_MODIFIED, MODIFIED_DELETED,
            ADDED_MODIFIED, ADDED_DELETED,
            DELETED_MODIFIED,
            RENAMED_MODIFIED, RENAMED_DELETED,
            COPIED_MODIFIED, COPIED_DELETED,
            UNMERGED,
            UNMERGED_ADDED, UNMERGED_ADDED_US, UNMERGED_ADDED_THEM,
            UNMERGED_DELETED, UNMERGED_DELETED_US, UNMERGED_DELETED_THEM,
            MODIFIED, ADDED, DELETED, RENAMED, COPIED,
         ]
    MODIFIED_SET = frozenset(MODIFIED_LIST)
    CLEAN_SET = set([UNMODIFIED, MODIFIED, ADDED, DELETED, RENAMED, COPIED, IGNORED, None])
    SIGNIFICANT_SET = frozenset(MODIFIED_LIST + [NOT_TRACKED])

_WD_DECO_MAP = {
        None: fsdb.Deco(Pango.Style.NORMAL, "black"),
        FileStatus.UNMODIFIED: fsdb.Deco(Pango.Style.NORMAL, "black"),
        FileStatus.WD_ONLY_MODIFIED: fsdb.Deco(Pango.Style.NORMAL, "blue"),
        FileStatus.WD_ONLY_DELETED: fsdb.Deco(Pango.Style.NORMAL, "red"),
        FileStatus.MODIFIED: fsdb.Deco(Pango.Style.NORMAL, "blue"),
        FileStatus.MODIFIED_MODIFIED: fsdb.Deco(Pango.Style.NORMAL, "blue"),
        FileStatus.MODIFIED_DELETED: fsdb.Deco(Pango.Style.NORMAL, "red"),
        FileStatus.ADDED: fsdb.Deco(Pango.Style.NORMAL, "darkgreen"),
        FileStatus.ADDED_MODIFIED: fsdb.Deco(Pango.Style.NORMAL, "blue"),
        FileStatus.ADDED_DELETED: fsdb.Deco(Pango.Style.NORMAL, "red"),
        FileStatus.DELETED: fsdb.Deco(Pango.Style.NORMAL, "red"),
        FileStatus.DELETED_MODIFIED: fsdb.Deco(Pango.Style.NORMAL, "blue"),
        FileStatus.RENAMED: fsdb.Deco(Pango.Style.ITALIC, "pink"),
        FileStatus.RENAMED_MODIFIED: fsdb.Deco(Pango.Style.ITALIC, "blue"),
        FileStatus.RENAMED_DELETED: fsdb.Deco(Pango.Style.ITALIC, "red"),
        FileStatus.COPIED: fsdb.Deco(Pango.Style.ITALIC, "green"),
        FileStatus.COPIED_MODIFIED: fsdb.Deco(Pango.Style.ITALIC, "blue"),
        FileStatus.COPIED_DELETED: fsdb.Deco(Pango.Style.ITALIC, "red"),
        FileStatus.UNMERGED: fsdb.Deco(Pango.Style.NORMAL, "magenta"),
        FileStatus.UNMERGED_ADDED: fsdb.Deco(Pango.Style.NORMAL, "magenta"),
        FileStatus.UNMERGED_ADDED_US: fsdb.Deco(Pango.Style.NORMAL, "magenta"),
        FileStatus.UNMERGED_ADDED_THEM: fsdb.Deco(Pango.Style.NORMAL, "magenta"),
        FileStatus.UNMERGED_DELETED: fsdb.Deco(Pango.Style.NORMAL, "magenta"),
        FileStatus.UNMERGED_DELETED_US: fsdb.Deco(Pango.Style.NORMAL, "magenta"),
        FileStatus.UNMERGED_DELETED_THEM: fsdb.Deco(Pango.Style.NORMAL, "magenta"),
        FileStatus.NOT_TRACKED: fsdb.Deco(Pango.Style.ITALIC, "cyan"),
        FileStatus.IGNORED: fsdb.Deco(Pango.Style.ITALIC, "grey"),
    }

# TODO: think about different deco map for the index

_FILE_DATA_RE = re.compile(r'(("([^"]+)")|(\S+))( -> (("([^"]+)")|(\S+)))?')

class GitFileData(fsdb.FileData):
    STATUS_DECO_MAP = _WD_DECO_MAP

class GitDirData(fsdb.DirData):
    STATUS_DECO_MAP = _WD_DECO_MAP

def get_git_file_data(string):
    match = _FILE_DATA_RE.match(string[3:])
    path = match.group(3) if match.group(3) else match.group(4)
    if match.group(5):
        extra_data = fsdb.RFD(extradatamatch.group(8) if match.group(8) else match.group(9), '->')
    else:
        extra_data = None
    return GitFileData(path, string[:2], extra_data)

def iter_git_file_data_text(text, related_file_path_data):
    for line in text.splitlines():
        file_path, status, extra_data = get_git_file_data(line)
        if extra_data:
            related_file_path_data.append((file_path, extra_data.path))
        yield (file_path, line[:2], extra_data)

# TODO: rewrite fsdb_git.WsFileDb to better handle submodules
class WsFileDb(fsdb.GenericSnapshotWsFileDb):
    class FileDir(fsdb.GenericSnapshotWsFileDb.FileDir):
        DIR_DATA = GitDirData
        FILE_DATA = GitFileData
        IGNORED_STATUS_SET = set([FileStatus.IGNORED])
        CLEAN_STATUS_SET = FileStatus.CLEAN_SET
        SIGNIFICANT_DATA_SET = FileStatus.SIGNIFICANT_SET
        ORDERED_DIR_STATUS_LIST = FileStatus.MODIFIED_LIST + [FileStatus.NOT_TRACKED]
        ORDERED_DIR_CLEAN_STATUS_LIST = [x for x in FileStatus.MODIFIED_LIST if x not in FileStatus.CLEAN_SET] + [FileStatus.NOT_TRACKED]
        def _get_initial_status(self, dir_path):
            if self._file_status_snapshot.status_set:
                for status in self.ORDERED_DIR_STATUS_LIST:
                    if status in self._file_status_snapshot.status_set:
                        return status
            return FileStatus.IGNORED if git_utils.is_ignored_path(dir_path) else None
        def _get_initial_clean_status(self, dir_path):
            if self._file_status_snapshot.status_set:
                for status in self.ORDERED_DIR_CLEAN_STATUS_LIST:
                    if status in self._file_status_snapshot.status_set:
                        return status
            return FileStatus.IGNORED if git_utils.is_ignored_path(dir_path) else None
        def _is_hidden_dir(self, ddata):
            if ddata.name[0] == ".":
                return ddata.status not in self.SIGNIFICANT_DATA_SET and ddata.clean_status not in self.SIGNIFICANT_DATA_SET
            return ddata.status == FileStatus.IGNORED
    def _get_file_data_text(self, h):
        file_data_text = runext.run_get_cmd(["git", "status", "--porcelain", "--ignored", "--untracked=all", "--ignore-submodules=none"])
        h.update(file_data_text.encode())
        return file_data_text
    @staticmethod
    def _extract_file_status_snapshot(file_data_text):
        related_file_path_data = []
        fsd = {file_path: (status, related_file_data) for file_path, status, related_file_data in iter_git_file_data_text(file_data_text, related_file_path_data)}
        for file_path, related_file_path in related_file_path_data:
            data = fsd.get(related_file_path, None)
            if data is not None:
                # don't overwrite git's opinion on related file data if it had one
                if data[1] is not None: continue
                status = data[0]
            else:
                stdout = runext.run_get_cmd(["git", "status", "--porcelain", "--", related_file_path], default="")
                status = stdout[:2] if stdout else None
            fsd[related_file_path] = (status, fsdb.RFD(path=file_path, relation="<-"))
        return fsdb.Snapshot(fsd)

class IndexFileDb(fsdb.GenericChangeFileDb):
    class FileDir(fsdb.GenericChangeFileDb.FileDir):
        DIR_DATA = GitDirData
        FILE_DATA = GitFileData
        CLEAN_STATUS_SET = FileStatus.CLEAN_SET
        def _calculate_status(self):
            for status in FileStatus.MODIFIED_LIST + [FileStatus.NOT_TRACKED]:
                if status in self._status_set:
                    return status
            return FileStatus.UNMODIFIED
        def _calculate_clean_status(self):
            for status in FileStatus.MODIFIED_LIST + [FileStatus.NOT_TRACKED]:
                if status in self._status_set:
                    return status
            return FileStatus.UNMODIFIED
    def __init__(self):
        fsdb.GenericChangeFileDb.__init__(self)
    def _get_patch_data_text(self, h):
        patch_status_text = runext.run_get_cmd(["git", "status", "--porcelain", "--untracked-files=no"], default="")
        h.update(patch_status_text.encode())
        return (patch_status_text)
    @staticmethod
    def _iterate_file_data(pdt):
        for line in pdt.splitlines():
            if line[0] == " ": continue # not in the index
            file_path, status, extra_data = get_git_file_data(line)
            yield (file_path, line[:2], extra_data)
