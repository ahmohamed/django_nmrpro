from distutils.core import setup
from os.path import exists
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
  name = 'django_nmrpro',
  packages = find_packages(), # this must be the same as the name above
  include_package_data=True,
  platforms='any',
  version = '0.2.4',
  description = 'Django app companion for nmrpro package',
  author = 'Ahmed Mohamed',
  author_email = 'mohamed@kuicr.kyoto-u.ac.jp',
  install_requires=['django >= 1.8','nmrpro', 'dill', 'Pillow'],
  url = 'https://github.com/ahmohamed/django_nmrpro', # use the URL to the github repo
  license='MIT',
  keywords = ['nmr', 'spectra', 'multi-dimensional'],
  classifiers = [],
)