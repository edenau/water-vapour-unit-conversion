######################################################################
# Purpose:
#         This function converts units of a vertical profile of water vapour.
# Method:
#         Convert whatever unit to number density (dennum), then to the unit of your choice
#         In other words, unitinp -> dennum -> unitout
# Usage:
#         from convert_h2o import convert_h2o
#         wout = convert_h2o(p,t,winp,unitinp,unitout)
# Input:  p       - Pressure profile in hPa
#         t       - Temperature profile in K
#         winp    - Water vapour concentration in
#         unitinp - Input units
#         unitout - Output units
#
#         unitinp,unitout, character:
#                         'M' Mass Mixing Ratio (g/Kg)
#                         'V' Volume Mixing Ratio (ppv)
#                         'H' Relative Humidity (%)
#                         'S' Specific Humidity
#                         'D' Dew Point (K)
#                         'P' Partial Pressure (hPa)
#                         'N' Number Density (cm-3)
#                         'R' Mass Density (kg/m3)
#                         'C' Colummnar conntent (mm) (output only)
# Matlab Version:
#         Guido Masiello, April 2005, September 2009, May 2017
#         Guido Masiello, September 2017, Optimization for Dewpoint Output.
#                         In the current version the routine solves analytically
#                         Clausius - Clapeyron law avoiding iterative approach of
#                         matlab fsolve function (used in the past version).
# Python Version:
#         Eden Au (edenau.github.io), translates matlab code to Python script.
# Development:
#         py1.0 - STABLE - 13 June 2019
#                 conversion available from M/H/N to M/H/N/C,
#                 outputs cross-checked with matlab version
# Python lib dependencies:
#         numpy
######################################################################
# Libraries

import numpy as np
######################################################################
# Convert to number density (unitinp -> dennum)

def M2N(p,t,winp,const):
    return const['r'] * winp / (1e3 + const['r'] * winp) * const['rhoair']

def N2N(p,t,winp_or_dennum,const):
    return winp_or_dennum

def H2N(p,t,winp,const):
    a = const['t0'] / t
    # saturation pressure
    densat = a * const['b'] * np.exp(const['c1'] + const['c2']*a + const['c3']*a*a) * 1e-6
    return densat * (winp/100)
######################################################################
# Convert from number density (dennum -> unitout)

def N2M(p,t,dennum,const):
    return dennum / (const['rhoair']-dennum) / (const['r']*1e-3)

def N2H(p,t,dennum,const):
    a = const['t0'] / t
    densat = a * const['b'] * np.exp(const['c1'] + const['c2']*a + const['c3']*a*a) * 1e-6
    return 100 * dennum / densat

def N2C(p,t,dennum,const):
    # # Compute specific Umidity
    # q = dennum / (const['r'] * const['rhoair'] + (1-2*const['r']) * dennum)
    # # Integrate over the colummn
    # wout = 0
    # for i in range(p.size-1):
    #     wout = wout + 0.5 / const['g'] * (q[i]+q[i+1]) * 100 * (p[i] - p[i+1])

    # Compute mass Mixing Ratio
    mmr = dennum / (const['rhoair']-dennum) / (const['r']*1e-3)
    # Integrate over the colummn
    wout = 0
    for i in range(p.size-1):
        wout = wout + 0.5 / const['g'] * (mmr[i]+mmr[i+1]) * 0.1 * (p[i] - p[i+1])
    return wout
######################################################################
# Error messages

def dim_error(p,t,winp):
    return f'Input vectors have inconsistent dimensions: {p.shape}, {t.shape}, and {winp.shape} respectively.'

unitinp_error = '''Character flag for input unit is not defined.
Available choices are:
'M' - Mass Mixing Ratio (g/Kg),
'V' - Volume Mixing Ratio (ppv),
'H' - Relative Umidity (%),
'S' - Specific Humidity,
'D' - Dew Point (K),
'P' - Partial Pressure (hPa),
'N' - Number Density (cm-3), and
'R' - Mass Density (kg/m3).'''

unitout_error = '''Character flag for output unit is not defined.
Available choices are:
'M' - Mass Mixing Ratio (g/Kg),
'V' - Volume Mixing Ratio (ppv),
'H' - Relative Umidity (%),
'S' - Specific Humidity,
'D' - Dew Point (K),
'P' - Partial Pressure (hPa),
'N' - Number Density (cm-3),
'R' - Mass Density (kg/m3), and
'C' - Colummnar content (mm).'''
######################################################################
# Main

def get_module_version():
    return 'py1.0'

def convert_h2o(p, t, winp, unitinp, unitout):
    # Convert lists to numpy arrays
    p = np.array(p)
    t = np.array(t)
    winp = np.array(winp)
    # Sanity check for consistent dimensions
    if not (p.shape == t.shape == winp.shape):
        raise ValueError(dim_error(p,t,winp))
    # Constants
    avogad=6.02214199e+23    # Avogadro Number
    alosmt=2.6867775e+19     # Loschmidt Number
    airmwt=28.964            # Air Molecular weight (grams)
    amwt1=18.015             # H2O Molecular weigth (grams)
    g=9.806                  # gravity acceleration
    c1=18.9766               #
    c2=-14.9595              # Clausius - Clapeyron Constants
    c3=-2.43882              #
    p0=1013.25
    t0=273.15
    r = airmwt/amwt1
    b = avogad/amwt1
    rhoair = alosmt * (p/p0) *(t0/t) # Air Density (molecules/cm3)

    # Constant dictionary
    const = {'avogad':avogad,
             'alosmt':alosmt,
             'airmwt':airmwt,
             'amwt1':amwt1,
             'g':g,
             'c1':c1,
             'c2':c2,
             'c3':c3,
             'p0':p0,
             't0':t0,
             'r':r,
             'b':b,
             'rhoair':rhoair
             }

    # a switcher to pick the correct function
    switch_to_dennum = {'M':M2N,
                        #'V':V2N,
                        'H':H2N,
                        #'S':S2N,
                        #'D':D2N,
                        #'P':P2N,
                        'N': N2N,
                        #'R':R2N
                        }

    # (unitinp -> dennum)
    try:
        dennum = switch_to_dennum[unitinp](p, t, winp, const)
    except:
        raise ValueError(unitinp_error)


    # a switcher to pick the correct function
    switch_from_dennum = {'M':N2M,
                          #'V':N2V,
                          'H':N2H,
                          #'S':N2S,
                          #'D':N2D,
                          #'P':N2P,
                          'N': N2N,
                          #'R':N2R,
                          'C':N2C
                          }

    # (dennum -> unitout)
    try:
        wout = switch_from_dennum[unitout](p, t, dennum, const)
    except:
        raise ValueError(unitout_error)

    return wout
######################################################################
