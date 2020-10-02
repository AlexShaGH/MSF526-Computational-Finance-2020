# -*- coding: utf-8 -*-

# MCStockPrices.py - Stock Prices simulation with Monte Carlo method 
# under the assumption of geometric brownian motion.
# MSF 526
# Illinois Institute of Technology
# Homework 2
# Author: Oleksandr Shashkov
# ID: A20229995
# Email: oshashko@hawk.iit.edu

__author__ = "oshashkov"

def MCStockPrices(S0, sigma, rateCurve, t, samples, integrator):
    """ Simulates stock prices using requested integrator method
    

    Parameters
    ----------
    S0 : float
        the stock prices at time t0
    sigma : float
        the constant volatility
    rateCurve : numpy array
        an InterestRateCurve stored as a numpy array
    t : array
        an array of fixing times ti; i = 1...N to simulate to
    samples : array
        an array of uniform random samples to use. The length of samples
        should be N x M where N is the number of fixing times
        and M is the number of paths
    integrator : string
        controls how the samples are generated according
        to the following value list:
        - 'standard', the paths are generated by using the solution of
        the Black-Scholes SDE step-by-step
        - 'euler', to use Euler-method integration of the BlackScholes SDE
        - 'milstein', to use Milstein-method integration of the BlackScholes SDE

    Returns
    -------
    numpy array of simulated stock prices having the same dimensions as samples

    """
    return numpy array
