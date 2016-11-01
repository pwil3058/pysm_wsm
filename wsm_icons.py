# Copyright (C) 2005-2016 Peter Williams <pwil3058@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License only.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

"""Create icons for WSM applications"""

from gi.repository import Gtk

from .gtx import icons

_PREFIX = icons.APP_NAME + "_"

STOCK_AMEND_COMMIT = _PREFIX + "stock_amend_commit"
STOCK_APPLIED_NEEDS_REFRESH = _PREFIX + "stock_applied_needs_refresh"
STOCK_APPLIED_UNREFRESHABLE = _PREFIX + "stock_applied_unrefreshable"
STOCK_APPLIED = _PREFIX + "stock_applied"
STOCK_BRANCH = _PREFIX + "stock_branch"
STOCK_COMMIT = _PREFIX + "stock_commit"
STOCK_CURRENT_BRANCH = _PREFIX + "stock_current_branch"
STOCK_DIFF = _PREFIX + "stock_diff"
STOCK_FILE_REFRESHED = _PREFIX + "stock_file_refreshed"
STOCK_FILE_NEEDS_REFRESH = _PREFIX + "stock_file_needs_refresh"
STOCK_FILE_UNREFRESHABLE = _PREFIX + "stock_file_unrefreshable"
STOCK_FILE_PROBLEM = STOCK_FILE_UNREFRESHABLE
STOCK_FINISH_PATCH = _PREFIX + "stock_finish_patch"
STOCK_FOLD_PATCH = _PREFIX + "stock_fold_patch"
STOCK_IMPORT_PATCH = _PREFIX + "stock_import_patch"
STOCK_MERGE = _PREFIX + "stock_merge"
STOCK_NEW_PATCH = _PREFIX + "stock_new_patch"
STOCK_PATCH_GUARD = _PREFIX + "stock_patch_guard"
STOCK_PATCH_GUARD_SELECT = _PREFIX + "stock_patch_guard_select"
STOCK_POP_PATCH = _PREFIX + "stock_pop_patch"
STOCK_PUSH_PATCH = _PREFIX + "stock_push_patch"
STOCK_REFRESH_PATCH = _PREFIX + "stock_refresh_patch"
STOCK_STASH_APPLY = _PREFIX + "stock_stash_apply"
STOCK_STASH_BRANCH = _PREFIX + "stock_stash_branch"
STOCK_STASH_DROP = _PREFIX + "stock_stash_drop"
STOCK_STASH_POP = _PREFIX + "stock_stash_pop"
STOCK_STASH_SAVE = _PREFIX + "stock_stash_save"
STOCK_STASH_SHOW = _PREFIX + "stock_stash_show"
STOCK_TAG = _PREFIX + "stock_tag"

_STOCK_ITEMS_OWN_PNG = [
    (STOCK_AMEND_COMMIT, _("Amend"), 0, 0, None),
    (STOCK_APPLIED, _("Applied"), 0, 0, None),
    (STOCK_APPLIED_NEEDS_REFRESH, _("Applied (needs refresh)"), 0, 0, None),
    (STOCK_APPLIED_UNREFRESHABLE, _("Applied (unrefreshable)"), 0, 0, None),
    (STOCK_BRANCH, _("Branch"), 0, 0, None),
    (STOCK_COMMIT, _("Commit"), 0, 0, None),
    (STOCK_CURRENT_BRANCH, _("Current Branch"), 0, 0, None),
    (STOCK_DIFF, _("Diff"), 0, 0, None),
    (STOCK_FILE_REFRESHED, _("Refreshed"), 0, 0, None),
    (STOCK_FILE_NEEDS_REFRESH, _("Needs Refresh"), 0, 0, None),
    (STOCK_FILE_UNREFRESHABLE, _("Unrefreshable"), 0, 0, None),
    (STOCK_FINISH_PATCH, _("Finish"), 0, 0, None),
    (STOCK_FOLD_PATCH, _("Fold"), 0, 0, None),
    (STOCK_IMPORT_PATCH, _("Import"), 0, 0, None),
    (STOCK_MERGE, _("Merge"), 0, 0, None),
    (STOCK_NEW_PATCH, _("New"), 0, 0, None),
    (STOCK_PATCH_GUARD, _("Guard"), 0, 0, None),
    (STOCK_PATCH_GUARD_SELECT, _("Select"), 0, 0, None),
    (STOCK_POP_PATCH, _("Pop"), 0, 0, None),
    (STOCK_PUSH_PATCH, _("Push"), 0, 0, None),
    (STOCK_REFRESH_PATCH, _("Refresh"), 0, 0, None),
    (STOCK_STASH_APPLY, _("Apply Stash"), 0, 0, None),
    (STOCK_STASH_BRANCH, _("Branch From Stash"), 0, 0, None),
    (STOCK_STASH_DROP, _("Drop From Stash"), 0, 0, None),
    (STOCK_STASH_POP, _("Pop Stash"), 0, 0, None),
    (STOCK_STASH_SAVE, _("Save To Stash"), 0, 0, None),
    (STOCK_STASH_SHOW, _("Show Stash"), 0, 0, None),
    (STOCK_TAG, _("Tag"), 0, 0, None),
]

icons.add_own_stock_icons(_STOCK_ITEMS_OWN_PNG)

# Icons that have to be designed eventually (using aliased GtK stock in the meantime)
STOCK_BACKOUT = Gtk.STOCK_MEDIA_REWIND
STOCK_CHECKOUT = Gtk.STOCK_EXECUTE
STOCK_CLONE = Gtk.STOCK_COPY
STOCK_CONFIG = Gtk.STOCK_PREFERENCES
STOCK_EDIT = Gtk.STOCK_EDIT
STOCK_FETCH = Gtk.STOCK_GO_FORWARD
STOCK_GRAPH = Gtk.STOCK_FILE
STOCK_GUESS = Gtk.STOCK_DIALOG_QUESTION
STOCK_INIT = STOCK_APPLIED
STOCK_INSERT = Gtk.STOCK_ADD
STOCK_LOG = Gtk.STOCK_FIND
STOCK_MARK_RESOLVE = Gtk.STOCK_APPLY
STOCK_MARK_UNRESOLVE = Gtk.STOCK_CANCEL
STOCK_MOVE = Gtk.STOCK_PASTE
STOCK_NEW_PLAYGROUND = Gtk.STOCK_NEW
STOCK_NEW_WORKSPACE = Gtk.STOCK_NEW
STOCK_PULL = Gtk.STOCK_GO_FORWARD
STOCK_PUSH = Gtk.STOCK_GO_BACK
STOCK_RECOVERY = Gtk.STOCK_REVERT_TO_SAVED
STOCK_REMOVE = Gtk.STOCK_REMOVE
STOCK_RENAME = Gtk.STOCK_PASTE
STOCK_RESOLVE = Gtk.STOCK_CONVERT
STOCK_REVERT = Gtk.STOCK_UNDO
STOCK_ROLLBACK = Gtk.STOCK_UNDO
STOCK_SELECT_GUARD = STOCK_APPLIED
STOCK_SERVE = Gtk.STOCK_EXECUTE
STOCK_SHELVE = Gtk.STOCK_EXECUTE
STOCK_STATUS = Gtk.STOCK_INFO
STOCK_STATUS_NOT_OK = Gtk.STOCK_CANCEL
STOCK_STATUS_OK = Gtk.STOCK_APPLY
STOCK_SYNCH = Gtk.STOCK_REFRESH
STOCK_UPDATE = Gtk.STOCK_EXECUTE
STOCK_VERIFY = STOCK_APPLIED
