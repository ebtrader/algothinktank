import pandas as pd

# https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html

df = pd.DataFrame()

df = pd.read_csv('position_test.csv')

print('all positions:', df)

#newobj = df.loc[1:,'position']

#print(newobj)

#newobj1 = df.loc[2:,'position']

#print(newobj1)

newobj2 = df.loc[lambda df: df['position'] > 100, :] # creates a new dataframe with only those positions with over 100 shares

print ('Positions over 100 shares:', newobj2)

#df_new['new_security_type'].str.contains('STK')

newobj3 = df.loc[lambda df: df['security_type'].str.contains('STK'), :] # creates a new dataframe with only those positions that are stock

print('only stock positions', newobj3)

newobj3sm = df.loc[lambda df: df['security_type'].str.contains('OPT'), :] # creates a new dataframe with only those positions that are OPT

print('only option positions', newobj3sm)

#this is not working
#newobj4 = df.loc[lambda df: df['security_type'].str.contains('STK') & df['position'] > 100, :] # creates a new dataframe with only those positions that are stock and over 100 shares

#print(newobj4)

newobj5 = df.loc[lambda df: df['symbol'].str.contains('TQQQ'), :] # creates a new dataframe with only those positions that are TQQQ

print('only TQQQ positions', newobj5)

df2 = pd.DataFrame()
df2 = newobj5

newobj7 = df2.loc[lambda df2: df2['position'] > 99, :] # creates a new dataframe with only those positions that are TQQQ and position over 100 shares

print('TQQQ positions over 100 shares', newobj7)

newobj9 = df.loc[lambda df: df['symbol'].str.contains('AAPL'), :] # creates a new dataframe with only those positions that are AAPL

print('all AAPL positions', newobj9)
