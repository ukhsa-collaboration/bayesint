'''
Testing the equal-tailed interval function
'''
import unittest
from bayesint import eqt_int_frac
from sympy import Rational

EQT_INT_FRAC_INPUTS = [
    (56, 126, 366, 354, (0, 0, 0, 0), "risk", 0.05, "estim"),
    (56, 126, 366, 354, (1/2, 1/2, 1/2, 1/2), "risk", 0.05, "estim"),
    (56, 126, 366, 354, (1/3, 1/3, 1/3, 1/3), "risk", 0.05, "estim"),
    (56, 126, 366, 354, (1, 1, 1, 1), "risk", 0.05, "estim"),
    (56, 126, 366, 354, (2, 2, 2, 2), "risk", 0.05, "estim"),
    (56, 126, 366, 354, (1, 2, 3, 4), "risk", 0.05, "estim"),
    (25, 108, 123, 313, (0, 0, 0, 0), "risk", 0.05, "estim"),
    (25, 108, 123, 313, (1/2, 1/2, 1/2, 1/2), "risk", 0.05, "estim"),
    (25, 108, 123, 313, (1/3, 1/3, 1/3, 1/3), "risk", 0.05, "estim"),
    (25, 108, 123, 313, (1, 1, 1, 1), "risk", 0.05, "estim"),
    (25, 108, 123, 313, (2, 2, 2, 2), "risk", 0.05, "estim"),
    (25, 108, 123, 313, (1, 2, 3, 4), "risk", 0.05, "estim")
    ]

EQT_INT_FRAC_OUTPUTS = [
    (Rational(236, 549), 0.184135819539239, 0.667343920284484),
    (Rational(236, 549), 0.198032015761997, 0.667711545605716),
    (Rational(236, 549), 0.193495220941505, 0.667591374087769),
    (Rational(236, 549), 0.211097728892229, 0.668058545428114),
    (Rational(236, 549), 0.234963753717440, 0.668696611718380),
    (Rational(236, 549), 0.265196970835994, 0.669540972138297),
    (Rational(7825, 13284), 0.324483034763110, 0.839177981791508),
    (Rational(7825, 13284), 0.346066274486009, 0.840491455803984),
    (Rational(7825, 13284), 0.339108082569407, 0.840055782030556),
    (Rational(7825, 13284), 0.365633347322525, 0.841788907698617),
    (Rational(7825, 13284), 0.399598040663112, 0.844363004471654),
    (Rational(7825, 13284), 0.428814489493699, 0.847432790177181)
    ]

class BayesintTests(unittest.TestCase):
    '''
    Test the interval finding function
    '''
    def test_hpd_int_frac(self):
        for input_set, output_set in zip(EQT_INT_FRAC_INPUTS, EQT_INT_FRAC_OUTPUTS):
            test_result = eqt_int_frac(*input_set)
            self.assertIsInstance(test_result,
                                  tuple,
                                  'eqt_in_func must return a tuple.')
            self.assertEqual(len(test_result),
                             3,
                             'eqt_int_frac must return an object of length 3')
            for test_value, expected_value in zip(test_result, output_set):
                self.assertAlmostEqual(test_value,
                                       expected_value,
                                       places=1,
                                       msg='The result for {} gave {}, expected {}.'
                                       ''.format(input_set, test_result, output_set))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()