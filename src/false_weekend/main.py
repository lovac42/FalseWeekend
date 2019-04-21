# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/FalseWeekend
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Version: 0.0.1 (Prototype version)

# This is to be used for testing the due dates without changing the system time.
# Use this only on test databases, not actual productions.

# The function in this file is copies from anki_src_v2.0.52
# Other Author: Damien Elmes <anki@ichi2.net>


from aqt import mw
from anki.sched import Scheduler
import time
from .false_weekend import *



fw=FalseWeekend()



# * MODIFIED VERSION * from anki_src_v2.0.52 *

def patch_updateCutoff(sched):
    oldToday = sched.today

    try: # V2
        sched.today = sched._daysSinceCreation() + fw.dayOffset
        sched.dayCutoff = sched._dayCutoff()
    except AttributeError: # V1
        # days since col created
        sched.today = int((time.time() - sched.col.crt) // 86400) + fw.dayOffset
        # end of day cutoff
        sched.dayCutoff = sched.col.crt + (sched.today+1)*86400


    #Prints out debug log
    if oldToday != sched.today:
        sched.col.log(sched.today, sched.dayCutoff)


    # update all daily counts, but don't save decks to prevent needless
    # conflicts. we'll save on card answer instead
    def update(g):
        for t in "new", "rev", "lrn", "time":
            key = t+"Today"
            if g[key][0] != sched.today:
                g[key] = [sched.today, 0]

    for deck in sched.col.decks.all():
        update(deck)


    # unbury if the day has rolled over
    unburied = sched.col.conf.get("lastUnburied", 0)
    # if unburied < sched.today:
    if unburied != sched.today:
        sched.unburyCards()


Scheduler._updateCutoff = patch_updateCutoff



from anki import version
ANKI21=version.startswith("2.1.")
if ANKI21:
    import anki.schedv2
    anki.schedv2.Scheduler._updateCutoff = patch_updateCutoff
