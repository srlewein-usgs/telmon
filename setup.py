from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import os

import telmon

here = os.path.abspath(os.path.dirname(__file__))

setup(name='usgs_telmon',
      version='0.1.0dev',
      description='Telemetry Monitoring',
      author='Scott Lewein',
      author_email='srlewein@usgs.gov',
      packages=find_packages(),
      include_package_data=True,
      long_description=read('README.md'),
      install_requires=read_requirements()['install_requires'],
      platforms='any',
      test_suite='unittest:TestLoader',
      zip_safe=False,
      # include the tier agnostic configuration file in the distributable
      # the file gets placed in site-packages upon dist installation
      py_modules=['config'],
      # include static files in the distributable
      # they will appear in the root of the virtualenv upon dist installation
data_files=identify_data_files(['assets/dist', 'data']))