import os
import io
import unittest

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

root = os.path.dirname(__file__)

with open(os.path.join(root, 'bayesint', 'version.py')) as f:
    exec(f.read())

with io.open(os.path.join(root, 'README.md'), encoding='utf8') as f:
    readme = f.read()

with io.open(os.path.join(root, 'LICENSE'), encoding='utf8') as f:
    license = f.read()

setup(name='bayesint',
      version=__version__,
      python_requires='~=2.7.14',
      packages=['bayesint'],
      description='Bayesian credible intervals for ratios',
      long_description=readme,
      author='Public Health England',
      author_email='maria.dunbar@phe.gov.uk',
      license=license,
      classifiers=['Programming Language :: Python :: 2.7.14',
                   'License :: Other/Proprietary License',
                   'Natural Language :: English',
                   'Topic :: Scientific/Engineering :: Information Analysis',
                   'Intended Audience :: Science/Research',
                   'Operating System :: Microsoft :: Windows'],
      install_requires=[
          #'future',
          'scipy>=0.19.1',
          'sympy>=1.1.1',
          'numpy>=1.13.3'],
      test_suite='tests.test_suite_loader'
)
