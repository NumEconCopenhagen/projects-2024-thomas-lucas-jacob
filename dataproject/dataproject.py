def keep_regs(df, regs):
    """ Example function. Keep only the subset regs of regions in data.

    Args:
        df (pd.DataFrame): pandas dataframe 

    Returns:
        df (pd.DataFrame): pandas dataframe

    """ 
    
    for r in regs:
        I = df.reg.str.contains(r)
        df = df.loc[I == False] # keep everything else
    
    return df

# installing API reader, that will allow to load data from DST.
%pip install git+https://github.com/alemartinello/dstapi
%pip install pandas-datareader

import pandas_datareader # install with `pip install pandas-datareader`
from dstapi import DstApi # install with `pip install git+https://github.com/alemartinello/dstapi`

supply_balance = DstApi('NAN1') #import NAN1 from DST
params = supply_balance._define_base_params(language= 'en') #defines all parameters in NAN1
SB1 = supply_balance.get_data(params=params) #creates a dataframe from the supply balance
SB2=SB1[SB1['PRISENHED']=='2010-prices, chained values, (bill. DKK.)'] #create new DF, filtered for price type = chained prices (2010)
supply_balance_import=SB2[SB2['TRANSAKT'] == 'B.1*g Gross domestic product']  #create new DF, filtered only BNP
del supply_balance_import['TRANSAKT'] #deletes the TRANSAKT column
del supply_balance_import['PRISENHED'] #deletes the PRISENHED column

Q_bnp = DstApi('NKN1')


