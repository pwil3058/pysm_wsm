### Copyright (C) 2016 Peter Williams <pwil3058@gmail.com>
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

"""Create icons for WSM applications"""

from gi.repository import Gtk

from .gtx import icons

_PREFIX = icons.APP_NAME + "_"

STOCK_AMEND_COMMIT = _PREFIX + "stock_amend_commit"
STOCK_APPLIED = _PREFIX + "stock_applied"
STOCK_BRANCH = _PREFIX + "stock_branch"
STOCK_COMMIT = _PREFIX + "stock_commit"
STOCK_CURRENT_BRANCH = _PREFIX + "stock_current_branch"
STOCK_DIFF = _PREFIX + "stock_diff"
STOCK_FILE_REFRESHED = _PREFIX + "stock_file_refreshed"
STOCK_FILE_NEEDS_REFRESH = _PREFIX + "stock_file_needs_refresh"
STOCK_FILE_UNREFRESHABLE = _PREFIX + "stock_file_unrefreshable"
STOCK_FILE_PROBLEM = STOCK_FILE_UNREFRESHABLE
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
    (STOCK_BRANCH, _("Branch"), 0, 0, None),
    (STOCK_COMMIT, _("Commit"), 0, 0, None),
    (STOCK_CURRENT_BRANCH, _("Current Branch"), 0, 0, None),
    (STOCK_DIFF, _("Diff"), 0, 0, None),
    (STOCK_FILE_REFRESHED, _("Refreshed"), 0, 0, None),
    (STOCK_FILE_NEEDS_REFRESH, _("Needs Refresh"), 0, 0, None),
    (STOCK_FILE_UNREFRESHABLE, _("Unrefreshable"), 0, 0, None),
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
STOCK_CHECKOUT = Gtk.STOCK_EXECUTE
STOCK_CLONE = Gtk.STOCK_COPY
STOCK_FETCH = Gtk.STOCK_GO_FORWARD
STOCK_INIT = STOCK_APPLIED
STOCK_INSERT= Gtk.STOCK_ADD
STOCK_NEW_WORKSPACE = Gtk.STOCK_NEW
STOCK_PULL = Gtk.STOCK_GO_FORWARD
STOCK_PUSH = Gtk.STOCK_GO_BACK
STOCK_RENAME = Gtk.STOCK_PASTE
