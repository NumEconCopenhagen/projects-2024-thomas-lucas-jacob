from scipy import optimize
# installing API reader, that will allow to load data from DST.
import pandas as pd
import pandas_datareader # install with `pip install pandas-datareader`
from dstapi import DstApi # install with `pip install git+https://github.com/alemartinello/dstapi`

def quarterly_BNP():
    Q_bnp = DstApi('NKN1')
    params_q = Q_bnp._define_base_params(language= 'en') #defines all parameters in NAN1
    Q1 = Q_bnp.get_data(params= params_q) #creates a dataframe from the supply balance
    Q2=Q1[Q1['PRISENHED']=='2010-prices, chained values, (bill. DKK.)'] #create new DF, filtered for price type = chained prices (2010)
    Q3=Q2[Q2['SÆSON'] == 'Seasonally adjusted']
    BNP_quarterly=Q3[Q3['TRANSAKT'] == 'B.1*g Gross domestic product']  #create new DF, filtered only BNP
    del BNP_quarterly['TRANSAKT'] #deletes the TRANSAKT column
    del BNP_quarterly['PRISENHED'] #deletes the PRISENHED column
    del BNP_quarterly['SÆSON'] #deletes the SÆSON column
    BNP_quarterly_sorted = BNP_quarterly.sort_values(by= 'TID') #we sort the dataframe by year
    return BNP_quarterly_sorted


def solve_ss(alpha, c):
    """ Example function. Solve for steady state k. 

    Args:
        c (float): costs
        alpha (float): parameter

    Returns:
        result (RootResults): the solution represented as a RootResults object.

    """ 
    
    # a. Objective function, depends on k (endogenous) and c (exogenous).
    f = lambda k: k**alpha - c
    obj = lambda kss: kss - f(kss)

    #. b. call root finder to find kss.
    result = optimize.root_scalar(obj,bracket=[0.1,100],method='bisect')
    
    return result