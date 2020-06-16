import sys

from setuptools import setup, find_packages

VERSION = '0.0.1'

with open('requirements.txt') as f:
    requirements = f.read().splitlines()[1:]

with open('requirements-dev.txt') as f:
    dev_requirements = f.read().splitlines()

# https://github.com/pytest-dev/pytest-runner#conditional-requirement
needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

setup(
    name='Owenscrape',
    version=VERSION,
    description=
    """
    Owenscrape:
    A Python application for scraping RO.eu, interpreting Rick item codes 
    """,
    url='https://github.com/0x6362/owenscrape',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    scripts=[],
    platforms='any',
    python_requires='>=3.5',
    setup_requires=pytest_runner,
    tests_require=dev_requirements,
    install_requires=requirements,
    entry_points={}
)
