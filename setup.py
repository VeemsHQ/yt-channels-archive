#!/usr/bin/env python
# -*- coding: utf-8 -*

import os
from codecs import open

from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

with open('README.md', 'r', encoding='utf-8') as rm_file:
    readme = rm_file.read()

with open('HISTORY.md', 'r', encoding='utf-8') as hist_file:
    history = hist_file.read()

setup(
    name='yt-channels-archive',
    version='0.2.0',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    zip_safe=False,
    description=(
        'A CLI tool to backup multiple YouTube channels along with their '
        'associated metadata and thumbnails. In the highest available quality.'
    ),
    author="O'Dwyer Software",
    author_email='hello@odwyer.software',
    url='https://github.com/project-49476/yt-channels-archive',
    license='Apache 2.0',
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    install_requires=install_requires,
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
    ],
    entry_points={'console_scripts': [
        'yt_archive = yt_archive.cli:main',
    ]},
)
