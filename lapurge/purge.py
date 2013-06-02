# Copyright (c) 2013 Matthieu Huguet

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import sys
from .types import BackupCollection, Backup


def run(config):
    backups = get_backup_collection(config.backup_dir)
    days = backups.days()
    if not days:
        return 0
    days_to_keep = get_days_to_keep(days, config)
    if days_to_keep or config.force:
        backups_to_remove = backups.except_days(set(days_to_keep))
        backups_to_remove.remove_all(config.noop)
        return 0
    else:
        sys.stderr.write("""
WARNING : With the specified retention rules, all the files in the specified
directory will be deleted. If you only specified -m and / or -w, it means that
there is no file in the directory that match your retention rules. Please look
at --day-of-week or --day-of-month options.

If you really know what you are doing, you can use option --force to
remove all your backup files according to your retention rules.
""")
        return 1


def get_backup_collection(backup_dir):
    daily_backups = BackupCollection()
    for file in os.listdir(backup_dir):
        fpath = os.path.join(backup_dir, file)
        if not os.path.islink(fpath) and os.path.isfile(fpath):
            backup = Backup.from_path(fpath)
            daily_backups.add(backup)
    return daily_backups


def get_days_to_keep(days, config):
    days_to_keep = daily_backup_days(days, config.days_retention)
    days_to_keep += weekly_backup_days(
        days, config.dow, config.weeks_retention)
    days_to_keep += monthly_backup_days(
        days, config.dom, config.months_retention)
    return days_to_keep


def daily_backup_days(days, retention):
    return days[:retention]


def weekly_backup_days(days, dow, retention):
    weekly_days = [day for day in days if day.isoweekday() == dow]
    return weekly_days[:retention]


def monthly_backup_days(days, dom, retention):
    monthly_days = [day for day in days if day.day == dom]
    return monthly_days[:retention]
