# installing API reader, that will allow to load data from DST.
import pandas_datareader # install with `pip install pandas-datareader`
from dstapi import DstApi # install with `pip install git+https://github.com/alemartinello/dstapi`

def supply_balance_DK():
    supply_balance = DstApi('NAN1') #import NAN1 from DST
    params = supply_balance._define_base_params(language= 'en') #defines all parameters in NAN1
    SB1 = supply_balance.get_data(params=params) #creates a dataframe from the supply balance
    SB1_1= SB1[SB1['TID'] >= 1990] #removes data from before 1990
    SB2=SB1[SB1['PRISENHED']=='2010-prices, chained values, (bill. DKK.)'] #create new DF, filtered for price type = chained prices (2010)
    supply_balance_BNP=SB2[SB2['TRANSAKT'] == 'B.1*g Gross domestic product']  #create new DF, filtered only BNP
    del supply_balance_BNP['TRANSAKT'] #deletes the TRANSAKT column
    del supply_balance_BNP['PRISENHED'] #deletes the PRISENHED column
    return supply_balance_BNP

def quarterly_BNP():
    Q_bnp = DstApi('NKN1')
    params_q = Q_bnp._define_base_params(language= 'en') #defines all parameters in NAN1
    Q1 = Q_bnp.get_data(params= params_q) #creates a dataframe from the supply balance
    Q2=Q1[Q1['PRISENHED']=='2010-prices, chained values, (bill. DKK.)'] #create new DF, filtered for price type = chained prices (2010)
    Q3=Q2[Q2['SÆSON'] == 'Seasonally adjusted']
    BNP_quarterly=Q3[Q3['TRANSAKT'] == 'B.1*g Gross domestic product']  #create new DF, filtered only BNP
    del BNP_quarterly['TRANSAKT'] #deletes the TRANSAKT column
    del BNP_quarterly['PRISENHED'] #deletes the PRISENHED column
    del BNP_quarterly['SÆSON']
    return BNP_quarterly
