# standard library
from setuptools import setup


# package configs
requires = ['astropy >= 3.0',
            'numpy >= 1.13',
            'xarray >= 0.10']

packages = ['radico']


# package setup
setup(name = 'radico',
      version = '0.0.1',
      description = 'Radiative transfer code',
      author = 'astropenguin',
      author_email = 'taniguchi@a.phys.nagoya-u.ac.jp',
      url = 'https://github.com/astropenguin/radico',
      install_requires = requires,
      packages = packages)