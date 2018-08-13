#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""Table tests.

Allows for the calculation of a chi squared statistic (chi_sq_stat) and the
corresponding test (chi_sq_test) for a 2x2 contingency table.

"""

#from builtins import *
from scipy.stats.distributions import chi2
from sympy.abc import P, C, M, N

## Tests
### Chi squared statistic
def chi_sq_stat(p_val, c_val, m_val, n_val):
    """Calculates the Chi squared test statistic for the between groups one and\
    two in a 2x2 contingency table.

    Parameters
    ==========

    p_val : Number of exposed in group one
    c_val : Number of exposed in group two
    m_val : Total number in group one
    n_val : Total number in group two

    Returns
    =======

    The Chi square statistic

    Raises
    ======

    TypeError
        Count inputs must be integers
    ValueError
        Chi squared statistic is negative

    See Also
    =======

    chi_sq_stat : Chi squared statistic

    Examples
    ========

    >>> chi_sq_stat(56, 126, 366, 354).evalf()
    39.232115997016614
    >>> chi_sq_stat(25, 108, 123, 313).evalf()
    8.374694230627874

    """
    if not (isinstance(p_val, int) and isinstance(c_val, int) and
            isinstance(m_val, int) and isinstance(n_val, int)):
        raise TypeError('Count inputs must be integers')
    tot = M + N
    val_1 = P + C
    val_2 = (N - C) + (M - P)
    stat = (tot * (P * (N - C) - (M - P) * C)**2) / (val_1 * val_2 * M * N)
    stat = stat.subs({P: p_val, C: c_val, M: m_val, N: n_val})
    if stat < 0:
        raise ValueError('Chi sqaured statistic is negative')
    else:
        return stat


### Chi squared test
def chi_sq_test(p_val, c_val, m_val, n_val, signif):
    """Gives the Chi squared test results between groups one and two in a 2x2\
    contingency table.

    Parameters
    ==========

    p_val : Number of exposed in group one
    c_val : Number of exposed in group two
    m_val : Total number in group one
    n_val : Total number in group two
    signif : Significance cut off desired

    Returns
    =======

    The Chi square statistic

    Raises
    ======

    ValueError
        Significance level must be between 0 and 1

    See Also
    =======

    chi_sq_stat : Chi squared statistic

    Examples
    ========

    >>> chi_sq_test(56, 126, 366, 354, 0.05)
    (3.762993555770853e-10, True)
    >>> chi_sq_test(25, 108, 123, 313, 0.05)
    (0.0038048156707230687, True)

    """
    if not (isinstance(p_val, int) and isinstance(c_val, int) and
            isinstance(m_val, int) and isinstance(n_val, int)):
        raise TypeError('Count inputs must be integers')
    if not 0 <= signif <= 1:
        raise ValueError('Significance level must be between 0 and 1')
    stat = chi_sq_stat(p_val, c_val, m_val, n_val)
    prob = chi2.sf(stat, 1)
    return prob, prob < signif
