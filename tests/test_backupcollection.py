from nose.tools import *
from lapurge.types import *
from datetime import datetime, date
from nose.tools import with_setup
from tempfile import mkstemp, mkdtemp
import shutil
import os
# To support python 2.7 and 3.x
try:
    from StringIO import StringIO
except:
    from io import StringIO


tempdir = None
saved_stderr = None


def setup_tempdir():
    global tempdir
    tempdir = mkdtemp()


def teardown_tempdir():
    global tempdir
    if tempdir is not None:
        shutil.rmtree(tempdir, ignore_errors=True)


def setup_capture_stderr():
    global saved_stderr
    saved_stderr = sys.stderr
    sys.stderr = StringIO()


def teardown_capture_stderr():
    global saved_stderr
    sys.stderr = saved_stderr


def test_add():
    b1 = Backup(datetime(2013, 1, 10, 2, 20), "b1")
    b2 = Backup(datetime(2013, 1, 11, 2, 20), "b2")
    b3 = Backup(datetime(2013, 1, 11, 2, 30), "b3")
    b4 = Backup(datetime(2013, 1, 12, 2, 20), "b4")
    bc = BackupCollection()
    assert(len(bc.backups) == 0)
    bc.add(b1)
    bc.add(b2)
    bc.add(b3)
    bc.add(b2)
    bc.add(b4)
    assert(len(bc.backups) == 3)
    assert(bc.backups[date(2013, 1, 10)] == set([b1]))
    assert(bc.backups[date(2013, 1, 11)] == set([b2, b3]))
    assert(bc.backups[date(2013, 1, 12)] == set([b4]))


def test_days():
    b1 = Backup(datetime(2013, 1, 10, 2, 20), "b1")
    b2 = Backup(datetime(2013, 1, 15, 2, 20), "b2")
    b3 = Backup(datetime(2012, 2, 5, 2, 20), "b3")
    b4 = Backup(datetime(2014, 1, 5, 2, 20), "b4")
    bc = BackupCollection()
    bc.add(b1)
    bc.add(b2)
    bc.add(b3)
    bc.add(b4)
    days = bc.days()
    expected = [b4.mtime.date(), b2.mtime.date(),
                b1.mtime.date(), b3.mtime.date()]
    assert(days == expected)


def test_except_days():
    b1 = Backup(datetime(2013, 1, 10, 2, 20), "b1")
    b2 = Backup(datetime(2013, 1, 10, 5, 30), "b2")
    b3 = Backup(datetime(2013, 1, 11, 2, 20), "b3")
    b4 = Backup(datetime(2014, 1, 12, 5, 30), "b4")
    bc = BackupCollection()
    bc.add(b1)
    bc.add(b2)
    bc.add(b3)
    bc.add(b4)
    result = bc.except_days(set([b1.mtime.date()]))
    assert(result.days() == [b4.mtime.date(), b3.mtime.date()])


@with_setup(setup_tempdir, teardown_tempdir)
def test_remove_all():
    global tempdir
    (fh1, path1) = mkstemp(dir=tempdir)
    b1 = Backup.from_path(path1)
    (fh2, path2) = mkstemp(dir=tempdir)
    b2 = Backup.from_path(path2)
    bc = BackupCollection()
    bc.add(b1)
    bc.add(b2)
    bc.remove_all()
    assert(os.path.exists(path1))
    assert(os.path.exists(path2))
    bc.remove_all(simulate=True)
    assert(os.path.exists(path1))
    assert(os.path.exists(path2))
    assert(bc.remove_all(simulate=False))
    assert(not os.path.exists(path1))
    assert(not os.path.exists(path2))


@with_setup(setup_capture_stderr, teardown_capture_stderr)
@with_setup(setup_tempdir, teardown_tempdir)
def test_remove_all_with_errors():
    global tempdir
    (fh1, path1) = mkstemp(dir=tempdir)
    b1 = Backup.from_path(path1)
    (fh2, path2) = mkstemp(dir=tempdir)
    b2 = Backup.from_path(path2)
    b2.remove(False)
    bc = BackupCollection()
    bc.add(b1)
    bc.add(b2)
    assert(os.path.exists(path1))
    assert(not os.path.exists(path2))
    assert(bc.remove_all())
    assert(os.path.exists(path1))
    assert(not os.path.exists(path2))
    assert(not bc.remove_all(False))
    assert(not os.path.exists(path1))
    assert(not os.path.exists(path2))
