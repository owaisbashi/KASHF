import pandas as pd
import numpy as np
import datetime as dt

df=pd.read_csv('Repayment_All_Merged.csv',sep='~')

date_object = dt.date.today()
print(date_object)

df.drop_duplicates(inplace=True)

df['PAID_DATE'] = df['PAID_DATE'].fillna(date_object)
df.drop(columns=['PAYMENT_STATUS'],inplace=True)
df['PAYMENT_DATE'] = pd.to_datetime(df['PAYMENT_DATE'])
df['PAID_DATE']=pd.to_datetime(df['PAID_DATE'])

df['diff_payment']=(df['PAID_DATE']-df['PAYMENT_DATE']).dt.days



col         = 'diff_payment'
conditions  = [ df[col] < 0,df[col] ==0 ,(df[col] > 0) & (df[col]<= 29), (df[col] > 29) | (df[col].isna())]
choices     = [ "ADVANCE", 'SECURE', 'DELINQUENT','DEFAULT']
    
df["TEMP_STATUS"] = np.select(conditions, choices, default=np.nan)

for i in df.columns:
    print(sum(df[i].isna()))


df_repay = df.groupby(['LOAN_CODE','TEMP_STATUS'])['INSTALLMENT_NO'].agg('count').reset_index()
print(df_repay)

print(df_repay.pivot_table(index=['LOAN_CODE'], columns='TEMP_STATUS', values='INSTALLMENT_NO').rename_axis(columns=None).reset_index())

final = (df_repay.pivot_table(index=['LOAN_CODE'], columns='TEMP_STATUS', values='INSTALLMENT_NO').rename_axis(columns=None)).reset_index().fillna(0)
print(final)

conditions = [
   (final['DEFAULT'] >0),
   (final['DELINQUENT']>=2),
    ((final['ADVANCE']>0) | (final['SECURE']>0))
    
]
choices=['DEFAULT','DELINQUENT','ADVANCE']
final['LABEL']=np.select(conditions,choices,default=np.nan)

print(final['LABEL'].value_counts())
print(df['LOAN_CODE'].nunique())

final.to_csv('Repay_labels.csv',index=False)

