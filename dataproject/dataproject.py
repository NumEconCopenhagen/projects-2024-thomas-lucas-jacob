# installing API reader, that will allow to load data from DST.
import pandas as pd
import pandas_datareader # install with `pip install pandas-datareader`
from dstapi import DstApi # install with `pip install git+https://github.com/alemartinello/dstapi`

def supply_balance_BNP():
    supply_balance = DstApi('NAN1') #import NAN1 from DST
    params = supply_balance._define_base_params(language= 'en') #defines all parameters in NAN1
    SB1 = supply_balance.get_data(params=params) #creates a dataframe from the supply balance
    SB1_1= SB1[SB1['TID'] >= 1990] #removes data from before 1990
    SB2=SB1_1[SB1_1['PRISENHED']=='2010-prices, chained values, (bill. DKK.)'] #create new DF, filtered for price type = chained prices (2010)
    supply_balance_BNP=SB2[SB2['TRANSAKT'] == 'B.1*g Gross domestic product']  #create new DF, filtered only BNP
    del supply_balance_BNP['TRANSAKT'] #deletes the TRANSAKT column
    del supply_balance_BNP['PRISENHED'] #deletes the PRISENHED column
    supply_balance_BNP_sorted = supply_balance_BNP.sort_values(by= 'TID') #we sort the dataframe by year
    return supply_balance_BNP_sorted

def supply_balance_import():
    supply_balance = DstApi('NAN1') #import NAN1 from DST
    params = supply_balance._define_base_params(language= 'en') #defines all parameters in NAN1
    SB1 = supply_balance.get_data(params=params) #creates a dataframe from the supply balance
    SB1_1= SB1[SB1['TID'] >= 1990] #removes data from before 1990
    SB2=SB1[SB1['PRISENHED']=='2010-prices, chained values, (bill. DKK.)'] #create new DF, filtered for price type = chained prices (2010)
    supply_balance_import=SB2[SB2['TRANSAKT'] == 'P.7 Imports of goods and services']  #create new DF, filtered only import
    del supply_balance_import['TRANSAKT'] #deletes the TRANSAKT column
    del supply_balance_import['PRISENHED'] #deletes the PRISENHED column
    supply_balance_import_sorted = supply_balance_import.sort_values(by= 'TID') #we sort the dataframe by year
    return supply_balance_import_sorted

def supply_balance_export():
    supply_balance = DstApi('NAN1') #import NAN1 from DST
    params = supply_balance._define_base_params(language= 'en') #defines all parameters in NAN1
    SB1 = supply_balance.get_data(params=params) #creates a dataframe from the supply balance
    SB1_1= SB1[SB1['TID'] >= 1990] #removes data from before 1990
    SB2=SB1[SB1['PRISENHED']=='2010-prices, chained values, (bill. DKK.)'] #create new DF, filtered for price type = chained prices (2010)
    supply_balance_export=SB2[SB2['TRANSAKT'] == 'P.6 Exports of goods and services']  #create new DF, filtered only export
    del supply_balance_export['TRANSAKT'] #deletes the TRANSAKT column
    del supply_balance_export['PRISENHED'] #deletes the PRISENHED column
    supply_balance_export_sorted = supply_balance_export.sort_values(by= 'TID') #we sort the dataframe by year
    return supply_balance_export_sorted

def supply_balance_privat():
    supply_balance = DstApi('NAN1') #import NAN1 from DST
    params = supply_balance._define_base_params(language= 'en') #defines all parameters in NAN1
    SB1 = supply_balance.get_data(params=params) #creates a dataframe from the supply balance
    SB1_1= SB1[SB1['TID'] >= 1990] #removes data from before 1990
    SB2=SB1[SB1['PRISENHED']=='2010-prices, chained values, (bill. DKK.)'] #create new DF, filtered for price type = chained prices (2010)
    supply_balance_privat=SB2[SB2['TRANSAKT'] == 'P.31 Private consumption']  #create new DF, filtered only privat consumption
    del supply_balance_privat['TRANSAKT'] #deletes the TRANSAKT column
    del supply_balance_privat['PRISENHED'] #deletes the PRISENHED column
    supply_balance_privat_sorted = supply_balance_privat.sort_values(by= 'TID') #we sort the dataframe by year
    return supply_balance_privat_sorted

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

def quarterly_BNP_for_mov_avg():
    Q_bnp_1 = DstApi('NKN1')
    params_q_1 = Q_bnp_1._define_base_params(language= 'en') #defines all parameters in NAN1
    Q1_1 = Q_bnp_1.get_data(params= params_q_1) #creates a dataframe from the supply balance
    Q2_1=Q1_1[Q1_1['PRISENHED']=='2010-prices, chained values, (bill. DKK.)'] #create new DF, filtered for price type = chained prices (2010)
    Q3_1=Q2_1[Q2_1['SÆSON'] == 'Seasonally adjusted']
    BNP_quarterly_1=Q3_1[Q3_1['TRANSAKT'] == 'B.1*g Gross domestic product']  #create new DF, filtered only BNP
    del BNP_quarterly_1['TRANSAKT'] #deletes the TRANSAKT column
    del BNP_quarterly_1['PRISENHED'] #deletes the PRISENHED column
    del BNP_quarterly_1['SÆSON'] #deletes the SÆSON column
    BNP_quarterly_sorted_1 = BNP_quarterly_1.sort_values(by= 'TID') #we sort the dataframe by year
    return BNP_quarterly_sorted_1