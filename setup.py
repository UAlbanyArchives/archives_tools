#!/usr/bin/env python

from setuptools import setup

__version__ = '0.1'


if __name__ == "__main__":
	setup(name='archives_tools',
	      version='0.1',
	      description='Some Python scripts for working with archives metadata and digital archives',
	      author='Gregory Wiedeman',
	      author_email='gwiedeman@albany.edu',
	      url='https://www.github.com/UAlbanyArchives/archives_tools',
	      install_requires=[
			"requests",
			"ConfigParser",
	      ],
	      packages=['archives_tools'],
	     )