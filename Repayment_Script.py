import pandas as pd
import numpy as np
import datetime

df=pd.read_csv('Repayment_All_Merged.csv',sep='~')
df['PAYMENT_DATE'] = pd.to_datetime(df['PAYMENT_DATE'])
df['PAID_DATE']=pd.to_datetime(df['PAID_DATE'])
df['diff_payment']=(df['PAID_DATE']-df['PAYMENT_DATE']).dt.days
df['PAYMENT_STATUS'].value_counts()
print(sum(df['PAID_DATE'].isna()))
print(df[df['diff_payment']<0]['PAYMENT_STATUS'].value_counts())

current_date=datetime.datetime.now()

col         = 'diff_payment'
conditions  = [ df[col] < 0,df[col] ==0 ,(df[col] > 0) & (df[col]<= 29), df[col] > 29,df[col].isna()]
choices     = [ "ADVANCE", 'SECURE', 'DELIQUENT','DEFAULT','DEFAULT']
    
df["TEMP_STATUS"] = np.select(conditions, choices, default=np.nan)

print(df['TEMP_STATUS'].value_counts())
df['PAID_DATE'].value_counts(dropna=False)
print(df['PAYMENT_DATE'].value_counts(dropna=False))
print(df['diff_payment'].value_counts(dropna=False))

pd.set_option('display.max_columns', 1000)
df.to_csv('Repayment_modified.csv',index=False)







