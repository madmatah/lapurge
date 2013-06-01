from datetime import datetime, date
from nose.tools import with_setup
from tempfile import mkstemp, mkdtemp
from lapurge import purge
from argparse import Namespace
import shutil
import os
import sys
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


@with_setup(setup_tempdir, teardown_tempdir)
def test_purge_scenario1():
    global tempdir
    # Generate 2 backup file per day from Tue 1st January 2013,
    # to Tue 26th March 2013
    backup_files = {}
    start_date = int(datetime(2013, 1, 1, 2, 0, 0).strftime("%s"))
    for day_count in range(85):
        tstamp = start_date + (day_count * 86400)
        (fh1, path1) = mkstemp(dir=tempdir)
        os.utime(path1, (tstamp, tstamp))
        (fh2, path2) = mkstemp(dir=tempdir)
        os.utime(path2, (tstamp, tstamp))
        backup_files[date.fromtimestamp(tstamp)] = [path1, path2]

    args = Namespace(backup_dir=tempdir,
                     days_retention=4,
                     weeks_retention=3,
                     months_retention=2,
                     dom=5,
                     dow=3,
                     force=False,
                     noop=False)
    assert(purge.run(args) == 0)

    expected_existing = set([
        # daily backups
        date(2013, 3, 26), date(2013, 3, 25),
        date(2013, 3, 24), date(2013, 3, 23),
        # weekly
        date(2013, 3, 20), date(2013, 3, 13), date(2013, 3, 6),
        # monthly bacups
        date(2013, 3, 5), date(2013, 2, 5)
    ])

    expected_absent = sorted(set(backup_files.keys()) - expected_existing)

    for day in expected_existing:
        for path in backup_files[day]:
            assert(os.path.exists(path))

    for day in expected_absent:
        for path in backup_files[day]:
            assert(not os.path.exists(path))


@with_setup(setup_capture_stderr, teardown_capture_stderr)
@with_setup(setup_tempdir, teardown_tempdir)
def test_purge_force():
    global tempdir
    # Generate 1 backup file per day from Thu. 10th January 2013,
    # to Tue 15th January 2013
    backup_files = []
    start_date = int(datetime(2013, 1, 10, 2, 0, 0).strftime("%s"))
    for day_count in range(6):
        tstamp = start_date + (day_count * 86400)
        (fh1, path) = mkstemp(dir=tempdir)
        os.utime(path, (tstamp, tstamp))
        backup_files.append(path)
    # No file in the backup_dir will match these rules
    args = Namespace(backup_dir=tempdir,
                     days_retention=0,
                     weeks_retention=3,
                     months_retention=2,
                     dom=5,
                     dow=3,
                     force=False,
                     noop=False)
    # Will it blend ?
    assert(purge.run(args) != 0)
    for backup_file in backup_files:
        assert(os.path.exists(backup_file))

    # Now, lets try with force=True
    args.force = True
    assert(purge.run(args) == 0)
    for backup_file in backup_files:
        assert(not os.path.exists(backup_file))
