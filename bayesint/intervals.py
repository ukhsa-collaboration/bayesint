#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""Intervals.

Allows for the calculation of the equal-tailed quantile credible interval
(eqt_int_frac) and the highest posterior density interval (hpd_int_frac) of a
ratio of two independent beta distributions. Both can be evaluated (frac_ints).

"""

#from builtins import *
from sympy import solveset, symbols, S, nsolve, Abs, lambdify
from sympy.abc import alpha, b, phi, theta, z, P, C, M, N, u, l, sigma
from scipy.optimize import minimize
import numpy as np
from numpy import vectorize

from .table_measures import rel_risk, odds_rat
from .random_variables import densi_frac, distri_frac

PI_1, PI_2, PI_3, PI_4 = symbols('pi:4')

## Credible intervals for fractions
### Equal-tailed interval
def eqt_int_frac(p_val, c_val, m_val, n_val, pri_val, frac_type, signif, ans):
    """Calculates the Bayesian credible interval using the equal-tailed approach.

    Parameters
    ==========

    p_val : Number of exposed in group one
    c_val : Number of exposed in group two
    m_val : Total number in group one
    n_val : Total number in group two
    pri_val : Tuple containing belief parameters for the two beta distributions,\
                B(c_val + pi_1, n_val - c_val + pi_2) and B(p_val + pi_3, m_val - p_val + pi_4),\
                given in the order: pi_1, pi_2, pi_3, pi_4
    frac_type : Desired ratio - relative risk ("risk") or odds ratio ("odds")
    signif : Significance cut off desired
    ans : Desired results - estimated ("estim") or exact "exact")

    Returns
    =======

    A tuple with the ratio, and lower and upper values of the interval\
        of the ratio (in that order)

    Raises
    ======

    TypeError
        Count inputs must be integers
    ValueError
        Significance level must be between 0 and 1
        frac_type must be "risk" or "odds"
        ans must be "estim" or "exact"

    See Also
    =======

    hpd_int_frac : Highest posterior density interval

    Examples
    ========

    >>> eqt_int_frac(56, 126, 366, 354, (0, 0, 0, 0), "risk", 0.05, "estim")
    (236/549, 0.184135819539239, 0.667343920284484)

    """
    if not (isinstance(p_val, int) and isinstance(c_val, int) and
            isinstance(m_val, int) and isinstance(n_val, int)):
        raise TypeError('Count inputs must be integers')
    if not 0 <= signif <= 1:
        raise ValueError('Significance level must be between 0 and 1')
    if frac_type == 'risk':
        frac = rel_risk(p_val, c_val, m_val, n_val)
    elif frac_type == 'odds':
        frac = odds_rat(p_val, c_val, m_val, n_val)
    else:
        raise ValueError('frac_type must be "risk" or "odds"')
    dis = distri_frac(p_val, c_val, m_val, n_val, pri_val, frac_type)
    dis = dis.subs({alpha: C + PI_1, b: N - C + PI_2,
                    theta: P + PI_3, phi: M - P + PI_4})
    low_temp = dis - (signif / 2)
    upp_temp = dis - (1 - (signif / 2))
    if ans == 'exact':
        low_ext = solveset(low_temp, z, domain=S.Reals)
        upp_ext = solveset(upp_temp, z, domain=S.Reals)
        # Insert values from contingency table
        low = low_ext.subs({P: p_val, C: c_val, M: m_val, N: n_val,
                            PI_1: pri_val[0], PI_2: pri_val[1],
                            PI_3: pri_val[2], PI_4: pri_val[3]})
        upp = upp_ext.subs({P: p_val, C: c_val, M: m_val, N: n_val,
                            PI_1: pri_val[0], PI_2: pri_val[1],
                            PI_3: pri_val[2], PI_4: pri_val[3]})
        return frac, low, upp
    elif ans == 'estim':
        low_est = low_temp.subs({P: p_val, C: c_val, M: m_val, N: n_val,
                                 PI_1: pri_val[0], PI_2: pri_val[1],
                                 PI_3: pri_val[2], PI_4: pri_val[3]})
        low = nsolve(low_est, frac, tol=10**(900))
        upp_est = upp_temp.subs({P: p_val, C: c_val, M: m_val, N: n_val,
                                 PI_1: pri_val[0], PI_2: pri_val[1],
                                 PI_3: pri_val[2], PI_4: pri_val[3]})
        upp = nsolve(upp_est, frac, tol=10**(900))
        return frac, low, upp
    else:
        raise ValueError('ans must be "estim" or "exact"')


### Highest posterior density interval
def hpd_int_frac(p_val, c_val, m_val, n_val, pri_val, frac_type, signif, minimisation_start):
    """Calculates the Bayesian credible interval using the highest posterior density approach.

    Parameters
    ==========

    p_val : Number of exposed in group one
    c_val : Number of exposed in group two
    m_val : Total number in group one
    n_val : Total number in group two
    pri_val : Tuple containing belief parameters for the two beta distributions,\
                B(c_val + pi_1, n_val - c_val + pi_2) and B(p_val + pi_3, m_val - p_val + pi_4),\
                given in the order: pi_1, pi_2, pi_3, pi_4
    frac_type : Desired ratio - relative risk ("risk") or odds ratio ("odds")
    signif : Significance cut off desired - default is 0.05
    minimisation_start : starting points for minimisation (i.e. starting estimates\
                                        of lower and  upper interval points)

    Returns
    =======

    A tuple with the ratio, and lower and upper values of the interval\
        of the ratio (in that order)

    Raises
    ======

    TypeError
        Count inputs must be integers
    ValueError
        Significance level must be between 0 and 1
        frac_type must be "risk" or "odds"
        ans must be "estim" or "exact"

    See Also
    =======

    eqt_int_frac : Equal-tailed interval

    Examples
    ========

    >>> hpd_int_frac(56, 126, 366, 354, (0, 0, 0, 0), "risk", 0.05, None)
    (236/549, 0.18274558146543513, 0.84884394841446875)

    """
    if not (isinstance(p_val, int) and isinstance(c_val, int) and
            isinstance(m_val, int) and isinstance(n_val, int)):
        raise TypeError('Count inputs must be integers')
    if not 0 <= signif <= 1:
        raise ValueError('Significance level must be between 0 and 1')
    if frac_type == 'risk':
        frac = rel_risk(p_val, c_val, m_val, n_val)
    elif frac_type == 'odds':
        frac = odds_rat(p_val, c_val, m_val, n_val)
    else:
        raise ValueError('frac_type must be "risk" or "odds"')

    if minimisation_start is None:
        minimisation_start = (max(0, frac - 0.2), frac + 0.2)

    dens = densi_frac(p_val, c_val, m_val, n_val, pri_val, frac_type)
    dis = distri_frac(p_val, c_val, m_val, n_val, pri_val, frac_type)
    #Generate the density and distribution at the upper and lower confidence values
    dens_lower = dens.subs({z: l})
    dens_upper = dens.subs({z: u})
    dis_lower = dis.subs({z: l})
    dis_upper = dis.subs({z: u})

    #Generate the interval function
    interval = Abs(dens_upper - dens_lower) + Abs(dis_upper - dis_lower - (1 - sigma))
    #Generate the concrete interval function for these parameter values
    interval_concrete = interval.subs({PI_1: pri_val[0],
                                       PI_2: pri_val[1],
                                       PI_3: pri_val[2],
                                       PI_4: pri_val[3],
                                       P: p_val,
                                       C: c_val,
                                       M: m_val,
                                       N: n_val,
                                       sigma: signif})

    #Convert to a function
    #print interval_concrete
    interval_fn = vectorize(lambdify((l, u), interval_concrete, modules="mpmath"))
    #print interval_fn(0,1)

    def interval_fn_min(x0):
        """A minimisable form of the interval function

        Parameters
        ==========
        x0 : The parameters to vary. This shoule be a scalar array containing\
        lower bound and delta (difference between the lower and upper)
        """
        assert x0[0] > 0, 'Lower bound must be greater than 0. Was {}'.format(x0[0])
        assert x0[1] >= 0, 'Delta must be greater than or equal to 0. Was {}'.format(x0[1])

        return interval_fn(x0[0], x0[0] + x0[1])

    minimise_result = minimize(fun=interval_fn_min,
                               x0=np.array(minimisation_start),
                               bounds=[(0.000000000001, None), (0, None)],
                               method='L-BFGS-B',
                               options={'eps': 1E-10}
                               #approx_grad=True,
                               #maxfun=400
                              )
    #Process the result
    lower = minimise_result['x'][0]
    upper = minimise_result['x'][0] + minimise_result['x'][1]

    #Check to see if the minimisation worked
    if minimise_result['status'] > 0:
        raise Exception('Minimisation failed: {}\n{}'.format(
            minimise_result['message'], minimise_result))

    #Some sanity checks
    if frac < lower:
        raise ValueError('Central estimate ({}) was lower than the lower bound ({})'
                         ''.format(frac, lower))
    if frac > upper:
        raise ValueError('Central estimate ({}) was higher than the upper bound ({})'
                         ''.format(frac, upper))
    return (frac, lower, upper)


### Wrapper giving both intervals
def frac_ints(p_val, c_val, m_val, n_val, pri_val, frac_type, signif):
    """Provides the results from calculating Bayesian credible intervals using\
    the equal-tailed approach and the highest posterior density approach.

    Parameters
    ==========

    p_val : Number of exposed in group one
    c_val : Number of exposed in group two
    m_val : Total number in group one
    n_val : Total number in group two
    pri_val : Tuple containing belief parameters for the two beta distributions,\
                B(c_val + pi_1, n_val - c_val + pi_2) and B(p_val + pi_3, m_val - p_val + pi_4),\
                given in the order: pi_1, pi_2, pi_3, pi_4
    frac_type : Desired ratio - relative risk ("risk") or odds ratio ("odds")
    signif : Significance cut off desired

    Returns
    =======

    A tuple with the two intervals

    Raises
    ======

    TypeError
        Count inputs must be integers

    See Also
    =======

    eqt_int_frac : Equal-tailed interval
    hpd_int_frac : Highest posterior density interval

    Examples

    >>> frac_ints(56, 126, 366, 354, (0, 0, 0, 0), "risk", 0.05)
    ((236/549, 0.184135819539239, 0.667343920284484),
    (236/549, 0.18274558146543513, 0.84884394841446875))

    """
    if not (isinstance(p_val, int) and isinstance(c_val, int) and
            isinstance(m_val, int) and isinstance(n_val, int)):
        raise TypeError('Count inputs must be integers')
    args = (p_val, c_val, m_val, n_val, pri_val, frac_type, signif)
    return eqt_int_frac(*args, ans="estim"), hpd_int_frac(*args, minimisation_start=None)
