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


import sys
import argparse

from .version import __version__


def check_negative(value):
    ivalue = int(value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError(
            "Invalid value (%s) : it must be a positive integer" % value)
    return ivalue


def check_dow(value):
    ivalue = int(value)
    if ivalue < 1 or ivalue > 7:
        raise argparse.ArgumentTypeError(
            "Invalid value for argument --day-of-week. You must provide an integer between 1 (monday) and 7 (sunday) ")
    return ivalue


def check_dom(value):
    ivalue = int(value)
    if ivalue < 1 or ivalue > 28:
        raise argparse.ArgumentTypeError(
            "Invalid value for argument --day-of-month. You must provide an integer between 1 and 28 (yup, monthly backups at the end of the month are EVIL) ")
    return ivalue


def parse():
    version = __version__
    description = "Delete files in a backup directory according to specified retention rules"
    parser = argparse.ArgumentParser(
        description=description, version=__version__)
    parser.add_argument("-d", action="store", type=check_negative,
                        dest="days_retention", help="Number of daily backups to keep",
                        default=0)
    parser.add_argument("-w", action="store", type=check_negative,
                        dest="weeks_retention", help="Number of weekly backups to keep",
                        default=0)
    parser.add_argument("-m", action="store", type=check_negative,
                        dest="months_retention", help="Number of monthly backups to keep",
                        default=0)
    parser.add_argument("--day-of-week", action="store", type=check_dow,
                        dest="dow", help="Day of the week to consider for weekly backups. Default is 7 (sunday)", default=7)
    parser.add_argument("--day-of-month", action="store", type=check_dom,
                        dest="dom", help="Day of the month to consider for monthly backups. Default is 1", default=1)
    parser.add_argument("--noop", action="store_true",
                        help="Perform a trial run without any deletions")
    parser.add_argument("--force", "--yolo", action="store_true",
                        help="Allow to remove all files in the backup_dir if no file match your retention rules")
    parser.add_argument("backup_dir",
                        help="Directory containing backup files (subdirectories are ignored)")
    args = parser.parse_args()
    if args.days_retention == 0 and args.weeks_retention == 0 and args.months_retention == 0:
        sys.stderr.write("""You must specify at least one of the following options : -d | -y | -m.
If you don't, that means you want to delete everything. Please use rm for that !
""")
    return args
