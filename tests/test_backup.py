from lapurge.types import Backup
from datetime import datetime, date
from nose.tools import with_setup
from tempfile import mkstemp, mkdtemp
from StringIO import StringIO
import shutil
import os
import sys

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


@with_setup(setup_tempdir, teardown_tempdir)
def test_frompath():
    global tempdir
    tstamp = int(datetime(2013, 3, 12, 2, 0, 0).strftime("%s"))
    (fh1, path1) = mkstemp(dir=tempdir)
    os.utime(path1, (tstamp, tstamp))
    b1 = Backup.from_path(path1)
    assert(b1.mtime.date() == date(2013, 3, 12))
    assert(b1.filepath == path1)


@with_setup(setup_capture_stderr, teardown_capture_stderr)
@with_setup(setup_tempdir, teardown_tempdir)
def test_remove():
    global tempdir
    (fh, filepath) = mkstemp(dir=tempdir)
    backup = Backup.from_path(filepath)
    assert(os.path.exists(filepath))
    assert(backup.remove())
    assert(os.path.exists(filepath))
    assert(backup.remove(simulate=True))
    assert(os.path.exists(filepath))
    assert(backup.remove(simulate=False))
    assert(not os.path.exists(filepath))
    assert(not backup.remove(simulate=False))


def test_eq():
    b1 = Backup(datetime(2013, 1, 10, 2, 20), "b")
    b2 = Backup(datetime(2013, 1, 10, 2, 20), "b")
    c = Backup(datetime(2013, 1, 10, 2, 20), "c")
    d = Backup(datetime(2013, 1, 10, 2, 21), "b")
    assert(b1 == b2)
    assert(b1 != c)
    assert(b1 != d)


def test_str():
    str(Backup(datetime(2013, 1, 10, 2, 20), "b1"))
