#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""Random variables.

Allows for the calculation of the expression for the density (densi_frac) and
distribution (distri_frac) of a ratio of two independent beta distributions.

"""

#from builtins import *
from sympy import hyper, symbols, Piecewise
from sympy.functions.special.beta_functions import beta
from sympy.abc import alpha, b, phi, theta, z, P, C, M, N

PI_1, PI_2, PI_3, PI_4 = symbols('pi:4')

## Probabilty-related functions
### Prior density
def densi_frac(p_val, c_val, m_val, n_val, pri_val, frac_type):
    """Calculates the prior density of a ratio of beta distributions.\
    Is used in interval calculations.

    Parameters
    ==========

    p_val : Number of exposed in group one
    c_val : Number of exposed in group two
    m_val : Total number in group one
    n_val : Total number in group two
    pri_val : Tuple containing belief parameters for the two beta distributions,\
                B(c_val + pi1, n_val - c_val + pi2) and B(p_val + pi3, m_val - p_val + pi4),\
                given in the order: pi1, pi2, pi3, pi4
    frac_type : Desired ratio - relative risk ("risk") or odds ratio ("odds")

    Returns
    =======

    The denstity function for these inputs

    Raises
    ======

    TypeError
        Count inputs must be integers
    ValueError
        frac_type must be "risk" or "odds"
        C must be larger than pi1
        N - C must be larger than pi2
        P must be larger than pi3
        M - P must be larger than pi4
        One or more counts are negative
        P + N + pi1 + pi2 + pi3 must be positive
        'P + pi3 + 1 must be positive
        C + M + pi1 + pi2 + pi3 must be positive
        C + pi3 + 1 must be positive

    See Also
    =======

    distri_frac : Posterior density

    Examples
    ========

    >>> densi_frac(56, 126, 366, 354, (0, 0, 0, 0), "risk")
    >>> densi_frac(25, 108, 123, 313, (0, 0, 0, 0), "risk")

    """
    if not (isinstance(p_val, int) and isinstance(c_val, int) and
            isinstance(m_val, int) and isinstance(n_val, int)):
        raise TypeError('Count inputs must be integers')
    if c_val <= pri_val[0]:
        raise ValueError('C ({:f}) must be larger than pi1 ({:f})'.format(
            c_val, pri_val[0]))
    elif n_val - c_val <= pri_val[1]:
        raise ValueError('N - C ({:f}) must be larger than pi2 ({:f})'.format(
            n_val - c_val, pri_val[1]))
    elif p_val <= pri_val[2]:
        raise ValueError('P ({:f}) must be larger than pi3 ({:f})'.format(
            p_val, pri_val[2]))
    elif m_val - p_val <= pri_val[3]:
        raise ValueError('M - P ({:f}) must be larger than pi4 ({:f})'.format(
            m_val - p_val, pri_val[3]))
    elif c_val < 0 or p_val < 0 or n_val < 0 or m_val < 0:
        raise ValueError('One or more counts are negative')
    else:
        if frac_type == 'risk':
            dens = Piecewise(
                    (beta(alpha + theta, b) / (beta(alpha, b) * beta(theta, phi)) *
                     z ** (theta - 1) * hyper((alpha + theta, 1 - phi),
                           (alpha + theta + b, ), z), z <= 1),
    # this comma needs to be here for hyper to work ^
                     (beta(alpha + theta, phi) / (beta(alpha, b) * beta(theta, phi)) *
                      z ** (- (1 + alpha)) * hyper((alpha + theta, 1 - b),
                            (alpha + theta + phi, ), 1 / z), z > 1))
        #      this comma needs to be here for hyper to work ^
        elif frac_type == 'odds':
            dens = Piecewise(
                    (beta(alpha + theta, b + phi) / (beta(alpha, b) * beta(theta, phi)) *
                     z ** (theta - 1) * hyper((alpha + theta, theta + phi),
                           (alpha + theta + b + phi, ), z), z <= 1),
                     (beta(alpha + theta, b + phi) / (beta(alpha, b) * beta(theta, phi)) *
                      z ** (- (1 + phi)) * hyper((phi + theta, phi + b),
                            (alpha + theta + b + phi, ), 1 / z), z > 1))
        else:
            raise ValueError('frac_type must be "risk" or "odds"')
        dens = dens.subs({alpha: C + PI_1, b: N - C + PI_2,
                              theta: P + PI_3, phi: M - P + PI_4})
        return dens


### Posterior distribution
def distri_frac(p_val, c_val, m_val, n_val, pri_val, frac_type):
    """Calculates the posterior distribution of a ratio of beta distributions.\
        Is used in interval calculations.

    Parameters
    ==========

    p_val : Number of exposed in group one
    c_val : Number of exposed in group two
    m_val : Total number in group one
    n_val : Total number in group two
    pri_val : Tuple containing belief parameters for the two beta distributions,\
                B(c_val + pi1, n_val - c_val + pi2) and B(p_val + pi3, m_val - p_val + pi4),\
                given in the order: pi1, pi2, pi3, pi4
    frac_type : Desired ratio - relative risk ("risk") or odds ratio ("odds")

    Returns
    =======

    The denstity function for these inputs

    Raises
    ======

    TypeError
        Count inputs must be integers
    ValueError
        frac_type must be "risk" or "odds"
        C must be larger than pi1
        N - C must be larger than pi2
        P must be larger than pi3
        M - P must be larger than pi4
        One or more counts are negative
        P + N + pi1 ({:f}) + pi2 + pi3 must be positive
        P + pi3 + 1 must be positive
        C + M + pi1 + pi2 + pi3 must be positive
        C + pi3 + 1 must be positive

    See Also
    =======

    densi_frac : Prior density

    Examples
    ========

    >>> distri_frac(56, 126, 366, 354, (0, 0, 0, 0), "risk")
    >>> distri_frac(25, 108, 123, 313, (0, 0, 0, 0), "risk")

    """
    if not (isinstance(p_val, int) and isinstance(c_val, int) and
            isinstance(m_val, int) and isinstance(n_val, int)):
        raise TypeError('Count inputs must be integers')
    if c_val <= pri_val[0]:
        raise ValueError('C ({:f}) must be larger than pi1 ({:f})'.format(
            c_val, pri_val[0]))
    elif n_val - c_val <= pri_val[1]:
        raise ValueError('N - C ({:f}) must be larger than pi2 ({:f})'.format(
            n_val - c_val, pri_val[1]))
    elif p_val <= pri_val[2]:
        raise ValueError('P ({:f}) must be larger than pi3 ({:f})'.format(
            p_val, pri_val[2]))
    elif m_val - p_val <= pri_val[3]:
        raise ValueError('M - P ({:f}) must be larger than pi4 ({:f})'.format(
            m_val - p_val, pri_val[3]))
    elif c_val < 0 or p_val < 0 or n_val < 0 or m_val < 0:
        raise ValueError('One or more counts are negative')
    else:
        if frac_type == 'risk':
            distr = Piecewise(
                    (beta(alpha + theta, b) / (beta(alpha, b) * beta(theta, phi)) *
                     z ** theta / theta * hyper((1 - phi, alpha + theta, theta),
                                                (alpha + theta + b, theta + 1), z), z <= 1),
                     (beta(theta + alpha, phi) / (beta(theta, phi) * beta(alpha, b)) *
                      z ** - alpha / alpha * hyper((theta + alpha, 1 - b, alpha),
                                                   (theta + phi + alpha, alpha + 1),
                                                   - 1 / z), z > 1))
            distr = distr.subs({alpha: C + PI_1, b: N - C + PI_2,
                                theta: P + PI_3, phi: M - P + PI_4})
            return distr
        elif frac_type == 'odds':
            raise NotImplementedError('distribution of odds ratio not currently implemented')
        else:
            raise ValueError('frac_type must be "risk" or "odds"')
