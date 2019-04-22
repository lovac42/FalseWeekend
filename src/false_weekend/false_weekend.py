# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/FalseWeekend
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Version: 0.0.1 (Prototype version)

# This is to be used for testing the due dates without changing the system time.
# Use this only on test databases, not actual productions.


from aqt import mw
from aqt.qt import *
from anki.hooks import addHook
from aqt.utils import getText, showInfo
from .utils import *


# ADDON_NAME='falseweekend'

class FalseWeekend:
    loaded=False
    dayOffset=0

    def __init__(self):
        self._setupMenu()
        addHook('unloadProfile', self.reset)


    def reset(self):
        self.dayOffset=0
        self.state.setChecked(False)

        mw.col.reset()
        #TODO: What happends when DB crashes before reset?


    def _setupMenu(self):
        if self.loaded: return #profile switch

        menu=None
        for a in mw.form.menubar.actions():
            if '&Debug' == a.text():
                menu=a.menu()
                menu.addSeparator()
                break
        if not menu:
            menu=mw.form.menubar.addMenu('&Debug')

        self.state=QAction("False Weekend", mw)
        self.state.setCheckable(True)
        self.state.setChecked(False)
        self.state.triggered.connect(self._exec)
        menu.addAction(self.state)
        self.loaded=True


    def _exec(self):
        n=0
        d,ok=getText("Change today of db: 0=today, 1=tomm, -1=yest. or m/d/y",
            default=str(self.dayOffset))
        if ok:
            self.state.setChecked(not d=='0')
            try:
                n=int(parseDate(d))
            except ValueError: n=0;
        self.dayOffset=n
        mw.reset()
