#!/usr/bin/python
import codecs

from setuptools import setup, find_packages


with codecs.open('README.rst', encoding='utf-8') as fd:
    long_description = fd.read()

tests_require = [
    'pytest==2.7.0',
    'pytest-cache==1.0',
    'mysqlclient==1.3.6',
    'pytest-services==1.0.5'
]

setup(
    name = "sqlalchemygrate",
    version = "0.2",
    packages = find_packages(exclude=["migrate.tests*"]),
    include_package_data = True,
    description = "Silly (but effective) database schema and data migration framework using SQLAlchemy.",
    long_description = long_description,
    install_requires = ['SQLAlchemy >= 0.5'],
    author = "Andrey Petrov",
    author_email = "andrey.petrov@shazow.net",
    url = "http://github.com/shazow/sqlalchemygrate",
    license = "MIT",
    entry_points="""
    # -*- Entry points: -*-
    """,
    scripts=['bin/grate'],
    tests_require=tests_require,
    extras_require={'test': tests_require}
)
