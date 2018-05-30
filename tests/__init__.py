# -*- coding: utf-8 -*-
"""
Location of test discovery function
"""

import unittest

#add the testsuite
def test_suite_loader():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite
