#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""Table measures.

Allows for the calculation of relative risks (rel_risk) and odds ratios (odds_rat)
for a 2x2 contingency table. Both can be evaluated (ratios).

"""

#from builtins import *
from sympy.abc import P, C, M, N

## Comparative measures
### Relative risk
def rel_risk(p_val, c_val, m_val, n_val):
    """Calculates the relative risk between groups one and two in a 2x2\
        contingency table.

    Parameters
    ==========

    p_val : Number of exposed in group one
    c_val : Number of exposed in group two
    m_val : Total number in group one
    n_val : Total number in group two

    Returns
    =======

    The relative risk estimate between groups one and two in a 2x2\
        contingency table

    Raises
    ======

    TypeError
        Count inputs must be integers
    ValueError
        Relative risk is negative

    See Also
    =======

    odds_rat: Odds ratio

    Examples
    ========

    >>> rel_risk(56, 126, 366, 354)
    236/549
    >>> rel_risk(25, 108, 123, 313)
    7825/13284

    """
    #args = (p_val, c_val, m_val, n_val)
    #if any(type(a) == 'int' for a in args):
    if not (isinstance(p_val, int) and isinstance(c_val, int) and
            isinstance(m_val, int) and isinstance(n_val, int)):
        raise TypeError('Count inputs must be integers')
    frac = (P * N) / (C * M)
    frac = frac.subs({P: p_val, C: c_val, M: m_val, N: n_val})
    if frac < 0:
        raise ValueError('Relative risk is negative')
    else:
        return frac


### Odds ratio
def odds_rat(p_val, c_val, m_val, n_val):
    """Calculates the odds ratio between groups one and two in a 2x2\
        contingency table.

    Parameters
    ==========

    p_val : Number of exposed in group one
    c_val : Number of exposed in group two
    m_val : Total number in group one
    n_val : Total number in group two

    Returns
    =======

    The odds ratio estimate between groups one and two in a 2x2\
        contingency table

    Raises
    ======

    TypeError
        Count inputs must be integers
    ValueError
        Odds ratio is negative

    See Also
    =======

    rel_risk: Relative risk

    Examples
    ========

    >>> odds_rat(56, 126, 366, 354)
    152/465
    >>> odds_rat(25, 108, 123, 313)
    5125/10584

    """
    if not (isinstance(p_val, int) and isinstance(c_val, int) and
            isinstance(m_val, int) and isinstance(n_val, int)):
        raise TypeError('Count inputs must be integers')
    frac = (P * (N - C)) / (C * (M - P))
    frac = frac.subs({P: p_val, C: c_val, M: m_val, N: n_val})
    if frac < 0:
        raise ValueError('Odds ratio is negative')
    else:
        return frac

### Wrapper giving both ratios
def ratios(p_val, c_val, m_val, n_val):
    """Provides the relative risk and odds ratio for a 2x2 contingency table.

    Parameters
    ==========

    p_val : Number of exposed in group one
    c_val : Number of exposed in group two
    m_val : Total number in group one
    n_val : Total number in group two

    Returns
    =======

    A tuple with the relative risk and the odds ratio

    Raises
    ======

    TypeError
        Count inputs must be integers
    ValueError
        Relative risk is negative
        Odds ratio is negative

    See Also
    =======

    rel_risk: Relative risk
    odds_rat: Odds ratio

    Examples
    =======
    >>> ratios(56, 126, 366, 354)
    (236/549, 152/465)

    """
    if not (isinstance(p_val, int) and isinstance(c_val, int) and
            isinstance(m_val, int) and isinstance(n_val, int)):
        raise TypeError('Count inputs must be integers')
    args = (p_val, c_val, m_val, n_val)
    return rel_risk(*args), odds_rat(*args)
