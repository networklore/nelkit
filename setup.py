"""setup.py."""
import re

from codecs import open
from setuptools import setup, find_packages

version = ''
with open('lib/nelkit/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

with open('HISTORY.rst', 'r', 'utf-8') as f:
    history = f.read()

long_description = readme + '\n\n' + history

console_scripts = [
    'nk-compare-configs=nelkit.cli.compare_configs:main',
    'nk-snmp-deviceinfo=nelkit.cli.snmp_deviceinfo:main'
]

config = {
    'name': 'nelkit',
    'package_dir': {'': 'lib'},
    'packages': find_packages('lib'),
    'entry_points': {'console_scripts': console_scripts},
    'version': version,
    'description': 'A Toolkit for network engineers',
    'long_description': long_description,
    'author': 'Patrick Ogenstad',
    'author_email': 'patrick@ogenstad.com',
    'license': 'Apache',
    'url': 'https://networklore.com/nelkit/',
    'install_requires': ['argparse', 'nelsnmp >= 0.2.0', 'PyYAML'],
    'classifiers': ['Development Status :: 4 - Beta',
                    'Intended Audience :: Developers',
                    'Intended Audience :: System Administrators']
}

setup(**config)
