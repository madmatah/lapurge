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

from collections import OrderedDict
from datetime import datetime
import os
import sys


class Backup:

    """ A Backup represents a file in the backup directory """

    def __init__(self, mtime, filepath):
        self.mtime = mtime
        self.filepath = filepath

    def remove(self, simulate=True):
        if (simulate):
            print ("REMOVE " + str(self))
            return True
        else:
            try:
                os.remove(self.filepath)
                return True
            except OSError as info:
                sys.stderr.write("ERROR : %s\n" % info)
                return False

    def __key(self):
        return (self.mtime, self.filepath)

    def __eq__(x, y):
        return x.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())

    def __str__(self):
        return self.filepath + " (" + str(self.mtime.date().isoformat()) + ")"

    @classmethod
    def from_path(cls, filepath):
        stats = os.lstat(filepath)
        mtime = datetime.utcfromtimestamp(stats.st_mtime)
        return cls(mtime, filepath)


class BackupCollection:

    """ Collection of Backup elements grouped by date """

    def __init__(self, backups={}):
        self.backups = dict(backups)

    def add(self, backup):
        """ add a backup to the collection """
        date = backup.mtime.date()
        if date not in self.backups:
            s = set()
            s.add(backup)
            self.backups[date] = s
        else:
            self.backups[date].add(backup)

    def days(self, recent_first=True):
        """ returns the list of days having backups, ordered by modification
        date (most recent backups first by default) """
        return sorted(self.backups.keys(), reverse=recent_first)

    def except_days(self, days):
        """ returns a copy of the BackupCollection without the specified days """
        filtered_backups = {day: self.backups[day] for day in self.days() if day not in days}
        return BackupCollection(filtered_backups)

    def remove_all(self, simulate=True):
        """ remove every backups of this collection """
        errors = False
        for days in self.days(recent_first=False):
            for backup in self.backups[days]:
                if not backup.remove(simulate):
                    errors = True
        return not errors
