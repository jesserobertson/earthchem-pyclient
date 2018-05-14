#!/usr/bin/env python3
""" file:   setup.py (earthchem)
    author: Jess Robertson
            CSIRO Mineral Resources
    date:   October 2016

    description: Setuptools installer script for earthchem.
"""

from setuptools import setup, find_packages
import yaml
import versioneer

def get_conda_dependencies(env_yaml=None):
    """
    Load dependencies from a conda environment.yml file

    Parameters:
        env_yaml - the path to the environment.yml file. Optional,
            will look for one in the current working directory if
            not specified.

    Returns:
        a list of dependencies which can be included in the setup.py
    """
    # Load up environment yaml
    env_yaml = env_yaml or 'environment.yml'
    with open(env_yaml, 'r') as src:
        pkginfo = yaml.load(src)

    # First pull out simple string dependencies (these are conda installs)
    # The pip packages are in a seperate dict
    dependencies = list()
    for dep in pkginfo['dependencies']:
        if isinstance(dep, str):  # we have a conda dependencies
            dependencies.append(dep.split('=')[0])
        elif isinstance(dep, dict):  # We have a pip dependency
            try:
                # We need to filter out things like -e because setuptools
                # doesn't know how to handle these
                pipdeps = [d.split('=')[0] 
                           for d in dep['pip'] 
                           if not d.lstrip().startswith('-')]
                dependencies.extend(pipdeps)
            except KeyError:
                raise IOError("Can't parse - environment.yaml is malformed")

    return dependencies

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
    install_requires=get_conda_dependencies(),
    setup_requires=[
        'versioneer'
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
