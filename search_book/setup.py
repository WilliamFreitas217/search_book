import re
from pathlib import Path
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

__package_name__ = 'search_book'

_script_local = Path(__file__).parent
with (_script_local / __package_name__ / '__init__.py').open() as version_handle:
    __version__ = re.search(r"(?<='|\").*(?='|\")", version_handle.readline()).group()

__author__ = 'williamdov.c.f@gmail.com'

setup(
    name=__package_name__,  # The name of your package and how it'll be imported.
    version=__version__,
    packages=find_packages(),  # NOTE - If you have a submodule, you have to include it as 'package_name.submodule_name'
    entry_points={  # Only if you have a script to use as an entry point
        'console_scripts': ['run_server=search_book.app:main']
    },
    include_package_data=True,
    author=__author__,
    author_email=__author__,
    description='',
    keywords='search book',
    install_requires=[
    ],
)
