#!/usr/bin/env python

from distutils.core import setup
from lapurge.version import __version__

setup(name='lapurge',
      version=__version__,
      author='Matthieu Huguet',
      author_email='matthieu@huguet.eu',
      description='A tool to purge your backup directories according to your retention rules',
      url='https://github.com/madmatah/lapurge',
      keywords='backup retention purge delete remove',
      license='The MIT License: http://www.opensource.org/licenses/mit-license.php',
      scripts=['bin/lapurge'],
      packages=['lapurge'],
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Intended Audience :: System Administrators',
                   'Operating System :: POSIX',
                   'License :: OSI Approved :: MIT License',
                   'Topic :: System :: Archiving'
                   ]
      )
