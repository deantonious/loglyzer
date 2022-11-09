from setuptools import setup, find_packages
from loglyzer import __app_name__, __version__

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(name=__app_name__,
        version=__version__,
        description='Python log analysis tool',
        author='deantonious',
        author_email='contact@deantonious.es',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url='https://www.python.org/sigs/distutils-sig/',
        packages=find_packages(include=['loglyzer']),
    )