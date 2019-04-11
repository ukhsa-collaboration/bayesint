import os
import io
import unittest

from setuptools import setup

root = os.path.dirname(__file__)

with io.open(os.path.join(root, 'README.md'), encoding='utf8') as f:
    readme = f.read()

with io.open(os.path.join(root, 'LICENSE'), encoding='utf8') as f:
    license = f.read()

setup_requires=[
    'setuptools-scm>=3.2.0',
    ]

setup(name='bayesint',
      use_scm_version=True,
      python_requires='>=2.7.14, !=3.0.*, !=3.1.*, !=3.3.*, !=3.4.*, >=3.5.5, >=3.6.6',
      packages=['bayesint'],
      description='Bayesian credible intervals for ratios',
      long_description=readme,
      long_description_content_type="text/markdown",
      author='Public Health England',
      author_email='thomas.finnie@phe.gov.uk',
      maintainer='Public Health England',
      url='https://github.com/PublicHealthEngland/bayesint',
      license='Open Government Licence 3.0',
      classifiers=['Programming Language :: Python',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'License :: Other/Proprietary License',
                   'Natural Language :: English',
                   'Topic :: Scientific/Engineering :: Information Analysis',
                   'Intended Audience :: Science/Research',
                   'Operating System :: OS Independent'],
      install_requires=[
          #'future',
          'scipy>=0.19.1',
          'sympy>=1.1.1',
          'numpy>=1.13.3'],
      test_suite='tests.test_suite_loader',
      setup_requires=setup_requires,
)
