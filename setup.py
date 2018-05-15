#!/usr/bin/env python3
""" file:   setup.py (earthchem)
    author: Jess Robertson
            CSIRO Mineral Resources
    date:   October 2016

    description: Setuptools installer script for earthchem.
"""

from setuptools import setup, find_packages
import versioneer

## PACKAGE INFORMATION
setup(
    name='earthchem',
    version=versioneer.get_version(),
    description='Data slurper for getting stuff from Earthchem services',
    long_description='making something good here',
    author='Jess Robertson',
    author_email='jesse.robertson@csiro.au',
    url='ssh://git@bitbucket.csiro.au:7999/rose/earthchem.git',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    # Dependencies
    install_requires=[
        'geopandas',
        'requests',
        'cartopy'
    ],
    setup_requires=[
        'versioneer',
        'nbstripout',
        'nbdime'
    ],
    tests_require=[
        'pytest',
        'pytest-runner',
        'pytest-cov',
        'coverage'
    ],

    # Contents
    packages=find_packages(exclude=['test*']),
    test_suite="tests",
    package_data={},

    # other stuff
    cmdclass=versioneer.get_cmdclass(),

    # Some entry points for running rosedb
    entry_points={
        'console_scripts': [
            'echem = cli:cli',
        ],
    }
)
