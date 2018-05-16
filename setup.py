#!/usr/bin/env python3
""" file:   setup.py (earthchem)
    author: Jess Robertson
            CSIRO Mineral Resources
    date:   October 2016

    description: Setuptools installer script for earthchem.
"""

from setuptools import setup, find_packages
import versioneer

with open('README.md', 'r') as src:
    LONG_DESCRIPTION = src.read()

## PACKAGE INFORMATION
setup(
    name='earthchem',
    version=versioneer.get_version(),
    description='Data slurper for getting stuff from Earthchem services',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    license='MIT',
    author='Jess Robertson',
    author_email='jesse.robertson@csiro.au',
    url='https://github.com/jesserobertson/earthchem-pyclient.git',
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
    project_urls={
        'Test coverage': 'https://coveralls.io/github/jesserobertson/earthchem-pyclient',
        'Test status': 'https://travis-ci.org/jesserobertson/earthchem-pyclient'
    },

    # Dependencies
    install_requires=[
        'geopandas',
        'requests',
        'beautifulsoup4',
        'lxml',
        'tqdm'
    ],
    extras_require={
        'dev': [
            'versioneer',
            'nbstripout',
            'nbdime'
        ]
    },
    tests_require=[
        'pytest',
        'pytest-runner',
        'pytest-cov',
        'coverage'
    ],

    # Contents
    packages=find_packages(exclude=['test*']),
    test_suite="tests",
    package_data={
        'earthchem': ['resources/*']
    },

    # other stuff
    cmdclass=versioneer.get_cmdclass(),

    # Some entry points for running rosedb
    entry_points={
        'console_scripts': [
            'echem = cli:cli',
        ],
    }
)
