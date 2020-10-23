# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='flaskapp',
    packages=['flaskapp'],
    include_package_data=True,
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
