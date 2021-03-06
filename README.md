# Lapurge

**lapurge** is a command line utility which helps you to purge your backup directories according to your retention rules, regardless of the backup tool you use.


[![Build Status](https://secure.travis-ci.org/madmatah/lapurge.png)](http://travis-ci.org/madmatah/lapurge)

## Why this tool ?

**Short answer :** [Unix Philosophy : «Write programs that do one thing and do it well»](http://en.wikipedia.org/wiki/Unix_philosophy)

**The long story :**

Usually, backup retention management is handled by the backup solution we use. But :
- some backup tools do not have this feature
- sometimes, we have to make our own backup script for particular cases.

In these cases, we have to manage the retention of the backup files on our own.
And honestly, I've seen too many ugly and untested shell scripts in production to do this job !


So I decided to create this tool. I hope it will follow the [Unix Philosophy (Write programs that do one thing and do it well)](http://en.wikipedia.org/wiki/Unix_philosophy).


## Requirements

- Python >= 2.7 and >= 3.2
- Works on Linux (not tested on other platforms, feedback appreciated)


## Installation

```
sudo pip install lapurge
```


## Usage

```
usage: lapurge [-h] [-v] [-d DAYS_RETENTION] [-w WEEKS_RETENTION]
               [-m MONTHS_RETENTION] [--day-of-week DOW]
               [--day-of-month DOM] [--noop] [--force]
               backup_dir


  backup_dir           Directory containing backup files (subdirectories
                       are ignored)

optional arguments:
  -h, --help           show this help message and exit
  -v, --version        show program's version number and exit
  -d DAYS_RETENTION    Number of daily backups to keep
  -w WEEKS_RETENTION   Number of weekly backups to keep
  -m MONTHS_RETENTION  Number of monthly backups to keep
  --day-of-week DOW    Day of the week to consider for weekly backups.
                       Default is 7 (sunday)
  --day-of-month DOM   Day of the month to consider for monthly backups.
                       Default is 1
  --noop               Perform a trial run without any deletions
  --force, --yolo      Allow to remove all files in the backup_dir if no
                       file match your retention rules

```


## Examples:

To keep 3 daily backups, 2 weekly backups (sunday's backup) and 2 monthly backups (the 1st of the month) :

```
lapurge -d 3 -w 2 --day-of-week 7 -m 2 --day-of-month 1 /my/backupdir
```


To keep 7 daily backups :

```
lapurge -d 7 /my/backupdir
```


## FAQ

#### Do I have to use a specific naming convention for my backup files ?

Nope ! lapurge use the **modification time** of your backup files to detect the backup date.

 *(I may add an option in the future to choose between ctime and mtime.)*

#### Each of my backups consists of several files. Is it a problem ?

Nope ! All the files modified the same day are considered as a single backup.

#### My backup tool did not run for 10 days but a cronjob was still running `lapurge -d 7` every days ... will I lose all my backups ?

Nope ! lapurge will keep the 7 most recent backups it will find.

#### Did that rhino just ordered a drink ?

Nope ! [Chuck Testa](http://www.youtube.com/watch?v=35CkYtcaJzI).
