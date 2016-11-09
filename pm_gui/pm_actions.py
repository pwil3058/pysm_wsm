### Copyright (C) 2011-2015 Peter Williams <pwil3058@gmail.com>
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

'''
Workspace status action groups
'''

from .. import pm
from ..pm_gui import pm_gui_ifce
from .. import scm

from ..bab import enotify

from ..gtx import actions

AC_NOT_IN_PM_PGND, AC_IN_PM_PGND, AC_IN_PM_PGND_MUTABLE, AC_IN_PM_PGND_MASK = actions.ActionCondns.new_flags_and_mask(3)
AC_NOT_PMIC, AC_PMIC, AC_PMIC_MASK = actions.ActionCondns.new_flags_and_mask(2)
AC_POP_POSSIBLE = AC_PMIC
AC_PUSH_POSSIBLE, AC_PUSH_POSSIBLE_MASK = actions.ActionCondns.new_flags_and_mask(1)
AC_ALL_APPLIED_REFRESHED, AC_ALL_APPLIED_REFRESHED_MASK = actions.ActionCondns.new_flags_and_mask(1)

def get_pushable_condns():
    return actions.MaskedCondns(AC_PUSH_POSSIBLE if pm_gui_ifce.PM.is_pushable else 0, AC_PUSH_POSSIBLE)

def _update_class_indep_pushable_cb(**kwargs):
    condns = get_pushable_condns()
    actions.CLASS_INDEP_AGS.update_condns(condns)
    actions.CLASS_INDEP_BGS.update_condns(condns)

enotify.add_notification_cb(enotify.E_CHANGE_WD|pm.E_PATCH_LIST_CHANGES, _update_class_indep_pushable_cb)

def get_absorbable_condns():
    return actions.MaskedCondns(AC_ALL_APPLIED_REFRESHED if pm_gui_ifce.PM.all_applied_patches_refreshed else 0, AC_ALL_APPLIED_REFRESHED)

def _update_class_indep_absorbable_cb(**kwargs):
    condns = get_absorbable_condns()
    actions.CLASS_INDEP_AGS.update_condns(condns)
    actions.CLASS_INDEP_BGS.update_condns(condns)

enotify.add_notification_cb(enotify.E_CHANGE_WD|scm.E_FILE_CHANGES|pm.E_FILE_CHANGES|pm.E_PATCH_LIST_CHANGES, _update_class_indep_absorbable_cb)

def get_in_pm_pgnd_condns():
    if pm_gui_ifce.PM.in_valid_pgnd:
        if pm_gui_ifce.PM.pgnd_is_mutable:
            conds = AC_IN_PM_PGND | AC_IN_PM_PGND_MUTABLE
        else:
            conds = AC_IN_PM_PGND
    else:
        conds = AC_NOT_IN_PM_PGND
    return actions.MaskedCondns(conds, AC_IN_PM_PGND_MASK)

def get_pmic_condns():
    return actions.MaskedCondns(AC_PMIC if pm_gui_ifce.PM.is_poppable else AC_NOT_PMIC, AC_PMIC_MASK)

def _update_class_indep_pm_pgnd_cb(**kwargs):
    condns = get_in_pm_pgnd_condns()
    actions.CLASS_INDEP_AGS.update_condns(condns)
    actions.CLASS_INDEP_BGS.update_condns(condns)

def _update_class_indep_pmic_cb(**kwargs):
    condns = get_pmic_condns()
    actions.CLASS_INDEP_AGS.update_condns(condns)
    actions.CLASS_INDEP_BGS.update_condns(condns)

enotify.add_notification_cb(enotify.E_CHANGE_WD|pm.E_NEW_PM, _update_class_indep_pm_pgnd_cb)
enotify.add_notification_cb(pm.E_PATCH_STACK_CHANGES|pm.E_NEW_PM|enotify.E_CHANGE_WD, _update_class_indep_pmic_cb)

class WDListenerMixin:
    def __init__(self):
        self.add_notification_cb(enotify.E_CHANGE_WD|pm.E_NEW_PM, self.pm_pgnd_condns_change_cb)
        self.add_notification_cb(pm.E_PATCH_STACK_CHANGES|pm.E_NEW_PM|enotify.E_CHANGE_WD, self.pmic_condns_change_cb)
        self.add_notification_cb(enotify.E_CHANGE_WD|pm.E_PATCH_LIST_CHANGES, self._pm_pushable_condns_change_cb)
        self.add_notification_cb(enotify.E_CHANGE_WD|scm.E_FILE_CHANGES|pm.E_FILE_CHANGES|pm.E_PATCH_LIST_CHANGES, self._pm_absorbable_condns_change_cb)
        condn_set = get_in_pm_pgnd_condns() | get_pmic_condns() | get_absorbable_condns() | get_pushable_condns()
        self.action_groups.update_condns(condn_set)
        try:
            self.button_groups.update_condns(condn_set)
        except AttributeError:
            pass
    def pm_pgnd_condns_change_cb(self, **kwargs):
        condns = get_in_pm_pgnd_condns()
        self.action_groups.update_condns(condns)
        try:
            self.button_groups.update_condns(condns)
        except AttributeError:
            pass
    def pmic_condns_change_cb(self, **kwargs):
        condns = get_pmic_condns()
        self.action_groups.update_condns(condns)
        try:
            self.button_groups.update_condns(condns)
        except AttributeError:
            pass
    def _pm_pushable_condns_change_cb(self, **kwargs):
        condns = get_pushable_condns()
        self.action_groups.update_condns(condns)
        try:
            self.button_groups.update_condns(condns)
        except AttributeError:
            pass
    def _pm_absorbable_condns_change_cb(self, **kwargs):
        condns = get_absorbable_condns()
        self.action_groups.update_condns(condns)
        try:
            self.button_groups.update_condns(condns)
        except AttributeError:
            pass

condns = get_in_pm_pgnd_condns() | get_pmic_condns() | get_absorbable_condns() | get_pushable_condns()
actions.CLASS_INDEP_AGS.update_condns(condns)
actions.CLASS_INDEP_BGS.update_condns(condns)
