import pandas as pd

# https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html

df = pd.DataFrame()

df = pd.read_csv('position.csv')

print(df)

#newobj = df.loc[1:,'position']

#print(newobj)

#newobj1 = df.loc[2:,'position']

#print(newobj1)

newobj2 = df.loc[lambda df: df['position'] > 100, :] # creates a new dataframe with only those positions with over 100 shares

print (newobj2)

#df_new['new_security_type'].str.contains('STK')

newobj3 = df.loc[lambda df: df['security_type'].str.contains('STK'), :] # creates a new dataframe with only those positions that are stock

print(newobj3)

newobj4 = df.loc[lambda df: df['security_type'].str.contains('STK') & df['position'] > 100, :] # creates a new dataframe with only those positions that are stock and over 100 shares

print(newobj4)