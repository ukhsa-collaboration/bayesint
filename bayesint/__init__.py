from __future__ import absolute_import, division, print_function

from .table_measures import *
from .table_tests import *
from .random_variables import *
from .intervals import *

from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    __version__ = 'unknown'
