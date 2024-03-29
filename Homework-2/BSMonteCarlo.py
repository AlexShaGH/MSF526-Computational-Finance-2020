# -*- coding: utf-8 -*-

# BSMonteCarlo.py - The function to price vanilla european-exercise options
# MSF 526
# Illinois Institute of Technology
# Homework 2
# Author: Oleksandr Shashkov
# ID: A20229995
# Email: oshashko@hawk.iit.edu

__author__ = "oshashkov"

import numpy as np
from numpy import exp,sqrt,maximum,mean,std
from numpy.random import randn
from scipy.stats import sem

# these are standard tenors for US Treasury Yield Curve as of 10/1/2020
RATE_CURVE_TENORS = [1/12,2/12,3/12,6/12,1,2,3,5,7,10,20,30]

def InterpolateRateCurve(curve,T,tenors=None):
    """ Interpolates the value of Yield Rate based on the provided rate curve
   
    Parameters
    ----------
    curve : array of floats
         represents rate curve. The length of curve and tenors must be the same
    T : float
        Time to interpolate rate for expressed in years
    tenors : array of floats, optional
        Tenors for Yield Rate curve . The default is None.

    Returns
    -------
    rate : float
        interpolated value of rate
    """
    if curve is None:
        raise ValueError("Yield curve can not be None")    
        
    if tenors is None:
        tenors = RATE_CURVE_TENORS #assume it's constant
    if len(tenors) != len(curve):
        return None
    return np.interp(T,tenors,curve)


def BSMonteCarlo(S0, K, T, sigma, checkpoints, rateCurve, samples=None):
    """ Estimates value of vanilla european-exercise options usinf Monte Carlo
    method in Black-Scholes-Merton model
    
    ### Call option for the purpose of programming assignment ###

    Parameters
    ----------
    S0 : float
        current price of underlying asset
    K : float
        option strike price
    T : float
        time to expiration expressed in years (1 month = 1/12 -> T = 0.08(3))
    sigma : float
        volatility of underlying expressed as a fraction
        (i.e. sigma = 0.5 stands for volatility of 50%)
    checkpoints : ordered list
        is an ordered list of integer sample counts at which to return
        the running mean, standard deviation, and estimated error
    rateCurve : numpy array
        is an InterestRateCurve stored as a numpy array
    samples : numpy array of floats, optional
        is a numpy array of uniform random samples to use. 
        The default is None

    Returns
    -------
    dict { 'TV': , # The final value ( i.e. mean at checkpoints[-1] )
            'Means': , # The running mean at each checkpoint
            'StdDevs': , # The running standard deviation at each checkpoint
            'StdErrs': , # The running standard error at each checkpoint
            }
    """
    
    # test parameters for None and NaN
    if np.isnan(K):
        raise ValueError("Strike price can not be NaN")
    if np.isnan(S0):
        raise  ValueError("Underlying price can not be NaN")
    if np.isnan(T):
        raise  ValueError("Time to expiration can not be NaN")
    if np.isnan(sigma):
        raise  ValueError("Volatility can not be NaN")
    if rateCurve is None:
        raise ValueError("Yield curve can not be None")
    if checkpoints is None:
        raise ValueError("checkpoints can not be None")        
    
    # check values of input parameters
    if S0 <= 0:
        raise ValueError("Underlying price can not be zero or negative")
    if K <= 0:
        raise ValueError("Strike price can not be zero or negative")
    if T <= 0:
        raise ValueError("Expiration time can not be zero or negative")
    if sigma <= 0:
        raise ValueError("Volatility can not be zero or negative")
    
    M = checkpoints[-1]
    
    # check for samples and generate them if needed
    if samples is None:
        samples = randn(M)
    elif len(samples) < M:
        raise ValueError('Not enough samples: {0}'.format(len(samples)))
    
    # find the value of "r" for given T using rate curve
    r = InterpolateRateCurve(rateCurve,T)
    if r is None:
        raise ValueError('Unable to obtain r')
    
    running_means = []
    running_stds = []
    running_st_errs = []
    vals = []
       
    for i in range(len(checkpoints)):
        # compute option values using MC method
        vals = exp(-r*T) * maximum(0,S0*exp((r-0.5*sigma**2)*T 
                + sigma*sqrt(T)*samples[:checkpoints[i]])-K)
        #compute running means, stds and errors
        running_means.append(mean(vals))
        running_stds.append(std(vals))
        running_st_errs.append(sem(vals))
    
    results = {}
    results['TV'] = running_means[-1]# The final value ( i.e. mean at checkpoints[-1] )
    results['Means'] = running_means# The running mean at each checkpoint
    results['StdDevs'] = running_stds# The running standard deviation at each checkpoint
    results['StdErrs'] = running_st_errs# The running standard error at each checkpoint

    return results




if __name__ == '__main__':
    # Problem 1 test:
    rate_curve = np.array(
        [0.08,0.08,0.10,0.11,0.12,0.13,0.16,0.28,0.47,0.69,1.23,1.46])

    S0=100.0
    K=110.0
    T=2.5
    sigma=0.4
    print('Parameters:\nS0 = {0}, K = {1}, T = {2}, Sigma = {3}\n'.format(
        S0,K,T,sigma))
    
    r = InterpolateRateCurve(rate_curve,T)
    print('Calculated r = {0}\n'.format(r))
      
    checkpoints = 10**np.arange(2,8)
    print('Checkpoints:\n{0}\n'.format(checkpoints))
    
    samples = randn(checkpoints[-1])
    str_expected_results = '''
    # matlab: [Call, Put] = blsprice(100,110,0.145,2.5,0.4)
    # Call = 35.4805
    
    # bsformula results for Call option:
    # Price = 35.4805'''
    
    print("Expected results:\n{0}\n".format(str_expected_results))
    
    output = BSMonteCarlo(S0, K, T, sigma, checkpoints, rate_curve, samples)
    print("Calculated results:\n")
    for key in output.keys():
        print('{0}:\n{1}\n'.format(key,output[key]))
