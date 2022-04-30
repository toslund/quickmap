from io import open
from setuptools import setup, find_packages

# with open('README.rst', 'rb') as f:
#     readme = f.read().decode('utf-8')

setup(
    name='quickMap',
    version='0.1.0',
    description='Python package to make simple maps',
    author='Tim Oslund',
    author_email='quickmap@timoslund.com',
    url='https://github.com/toslund/quickmap',
    package_dir={"": "src"},
    packages=find_packages(where="src")
)
