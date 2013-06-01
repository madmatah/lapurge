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
            print "REMOVE " + str(self)
            return True
        else:
            try:
                os.remove(self.filepath)
                return True
            except OSError, info:
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

    def days(self):
        """ returns the list of days having backups, ordered by modification
        date (most recent backups first) """
        return sorted(self.backups.keys(), reverse=True)

    def except_days(self, days):
        """ returns a copy of the BackupCollection without the specified days """
        filtered_backups = {day: self.backups[day] for day in self.days() if day not in days}
        return BackupCollection(filtered_backups)

    def remove_all(self, simulate=True):
        """ remove every backups of this collection """
        errors = False
        for days in self.backups:
            for backup in self.backups[days]:
                if not backup.remove(simulate):
                    errors = True
        return not errors
