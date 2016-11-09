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

from gi.repository import Gtk

from ..gtx import actions
from ..gtx import apath

from ... import CONFIG_DIR_PATH

class WorkspacePathView(apath.AliasPathView):
    SAVED_FILE_NAME = os.path.join(CONFIG_DIR_PATH, "workspaces")

class WorkspacePathTable(apath.AliasPathTable):
    VIEW = WorkspacePathView

class WorkspaceOpenDialog(apath.PathSelectDialog):
    PATH_TABLE = WorkspacePathTable
    def __init__(self, parent=None):
        apath.PathSelectDialog.__init__(self, label=_("Workspace/Directory"), parent=parent)

def generate_chdir_to_workspace_menu(label=_("Change Directory To")):
    return WorkspacePathView.generate_alias_path_menu(label, lambda newtgnd: chdir(newtgnd))

def add_workspace_path(path):
    return WorkspacePathView.append_saved_path(path)

def chdir(newdir):
    from ..bab import CmdResult
    events = 0
    try:
        os.chdir(newdir)
        retval = CmdResult.ok()
    except OSError as err:
        import errno
        ecode = errno.errorcode[err.errno]
        emsg = err.strerror
        retval = CmdResult.error(stderr="{0}: \"{1}\" : {2}".format(ecode, newdir, emsg))
        newdir = os.getcwd()
    # NB regardless of success of os.chdir() we need to check the interfaces
    from ..bab import enotify
    from ..bab import options
    from ..gtx.console import LOG
    from ..scm_gui import ifce as scm_ifce
    scm_ifce.reset_scm_ifce()
    if scm_ifce.SCM.in_valid_pgnd:
        # move down to the root dir
        newdir = scm_ifce.SCM.get_playground_root()
        os.chdir(newdir)
        from ..gtx import recollect
        WorkspacePathView.append_saved_path(newdir)
        recollect.set("workspace", "last_used", newdir)
    from ..pm_gui import ifce as pm_ifce
    pm_ifce.reset_pm_ifce()
    options.reload_pgnd_options()
    CURDIR = os.getcwd()
    LOG.start_cmd(_("New Working Directory: {0}\n").format(CURDIR))
    LOG.append_stdout(retval.stdout)
    LOG.append_stderr(retval.stderr)
    if scm_ifce.SCM.in_valid_pgnd:
        LOG.append_stdout('In valid repository\n')
    else:
        LOG.append_stderr('NOT in valid repository\n')
    LOG.end_cmd()
    enotify.notify_events(enotify.E_CHANGE_WD, new_wd=CURDIR)
    return retval

def change_wd_acb(_arg):
    open_dialog = WorkspaceOpenDialog()
    if open_dialog.run() == Gtk.ResponseType.OK:
        newpg = open_dialog.get_path()
        if newpg:
            with open_dialog.showing_busy():
                result = chdir(newpg)
            open_dialog.report_any_problems(result)
    open_dialog.destroy()

actions.CLASS_INDEP_AGS[actions.AC_DONT_CARE].add_actions(
    [
        ("scm_change_wd", Gtk.STOCK_OPEN, _("Open"), "",
         _("Change current working directory"),
         change_wd_acb
        ),
    ])
