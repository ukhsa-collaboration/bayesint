'''
Testing the highest posterior density interval function
'''
import unittest
from bayesint import hpd_int_frac
from sympy import Rational

HPD_INT_FRAC_INPUTS = [
    (56, 126, 366, 354, (0, 0, 0, 0), "risk", 0.05, None),
    (56, 126, 366, 354, (1/2, 1/2, 1/2, 1/2), "risk", 0.05, None),
    (56, 126, 366, 354, (1/3, 1/3, 1/3, 1/3), "risk", 0.05, None),
    (56, 126, 366, 354, (1, 1, 1, 1), "risk", 0.05, None),
    (56, 126, 366, 354, (2, 2, 2, 2), "risk", 0.05, None),
    (56, 126, 366, 354, (1, 2, 3, 4), "risk", 0.05, None),
    (25, 108, 123, 313, (0, 0, 0, 0), "risk", 0.05, (0, 7825.0/13284)),
    (25, 108, 123, 313, (0, 0, 0, 0), "risk", 0.05, (0.4, 7825.0/13284)),
    (25, 108, 123, 313, (1/2, 1/2, 1/2, 1/2), "risk", 0.05, (0.4, 7825.0/13284)),
    (25, 108, 123, 313, (1/3, 1/3, 1/3, 1/3), "risk", 0.05, (0.4, 7825.0/13284)),
    (25, 108, 123, 313, (1, 1, 1, 1), "risk", 0.05, (0.4, 7825.0/13284)),
    (25, 108, 123, 313, (2, 2, 2, 2), "risk", 0.05, (0.4, 7825.0/13284)),
    (25, 108, 123, 313, (1, 2, 3, 4), "risk", 0.05, (0.4, 7825.0/13284))
    ]

HPD_INT_FRAC_OUTPUTS = [
    (Rational(236, 549), 0.18274558146543513, 0.84884394841446875),
    (Rational(236, 549), 0.18757048159418485, 0.85244144037884517),
    (Rational(236, 549), 0.18653066052899805, 0.85330629631297295),
    (Rational(236, 549), 0.19003847555891126, 0.85204465555167919),
    (Rational(236, 549), 0.19706168934499999, 0.84444052669791325),
    (Rational(236, 549), 0.19742700634986471, 0.86654457125620166),
    (Rational(7825, 13284), 1e-12, 0.5890545016571277),
    (Rational(7825, 13284), 0.3503450323429196, 0.866347221610741),
    (Rational(7825, 13284), 0.3811218015357208, 0.8290217856675588),
    (Rational(7825, 13284), 0.35291799741948277, 0.87279116078276364),
    (Rational(7825, 13284), 0.35807308484872263, 0.8853976078998071),
    (Rational(7825, 13284), 0.40068136124448028, 0.84279306354227945),
    (Rational(7825, 13284), 0.37304196126577, 0.9223962699502721)
    ]
class BayesintTests(unittest.TestCase):
    '''
    Test the interval finding function
    '''
    def test_hpd_int_frac(self):
        for input_set, output_set in zip(HPD_INT_FRAC_INPUTS, HPD_INT_FRAC_OUTPUTS):
            test_result = hpd_int_frac(*input_set)
            self.assertIsInstance(test_result,
                                  tuple,
                                  'hpd_in_func must return a tuple.')
            self.assertEqual(len(test_result),
                             3,
                             'hpd_int_frac must return an object of length 3')
            for test_value, expected_value in zip(test_result, output_set):
                self.assertAlmostEqual(test_value,
                                       expected_value,
                                       places=1,
                                       msg='The result for {} gave {}, expected {}.'
                                       ''.format(input_set, test_result, output_set))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()