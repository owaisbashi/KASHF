
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from sklearn.model_selection import ParameterGrid
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

df=pd.read_csv('demo_features (1).csv')
print(df.columns)

df2=pd.read_csv('rs_features (1).csv')
print(df2.columns)
merged_df=pd.merge(df,df2,on=['LOAN_CODE'])

df['Data_lagged_LOAN_AMT_APP'].value_counts(dropna=False)


print(merged_df['LOAN_CODE'].nunique())


merged_df.drop_duplicates(inplace=True)
merged_df.drop(50183,inplace=True)

df_col_normalized=['LOAN_CYCLE_NO', 'BUSINESS_DURATION', 'LOAN_AMT_REQ',
       'NO_OF_CHILDREN', 'NO_OF_DEPENDENTS', 'NO_OF_EARNERS',
       'NO_OF_FAMILY_MEM', 'IN_CURRENT_AREA', 'IN_CURRENT_HOUSE','AGE','MONTHLY_INCOME','PRIMARY_INCOME','SECONDARY_INCOME',
                   'NDI','PSC_SCORE','CONSUMER_RATIO','EARNER_RATIO','MEMBERSHIP_DURATION','RECENCY_OF_CNIC_EXPIRATION',
                   'BUSINESS_DURATION_MONTHS','Biz_Exp-BUSINESS PLACE RENT','Biz_Exp-LEASE PAYMENT OF BUSINESS ASSETS',
                   'Biz_Exp-MAINTENANCE','Biz_Exp-OTHERS','Biz_Exp-PURCHASE OF ASSETS','Biz_Exp-RAW MATERIAL / INVENTORY',
                   'Biz_Exp-TELEPHONE EXPENSE','Biz_Exp-TRAVELLING EXPENSE','Biz_Exp-UTILITY BILLS','Biz_Exp-WAGES / SALARY',
                   'HH_Exp-CLOTHING','HH_Exp-COMMITTEE','HH_Exp-EDUCATION','HH_Exp-FOOD','HH_Exp-LEASE PAYMENT OF HOUSEHOLD ASSETS',
                   'HH_Exp-MARRIAGE AND OTHER OCCASIONS','HH_Exp-MEDICAL','HH_Exp-OTHER LOAN INSTALLMENT','HH_Exp-RENT',
                   'HH_Exp-TELEPHONE EXPENSE','HH_Exp-TRAVELLING','HH_Exp-UTILITY BILLS',
                   
        'Data_lagged_PURCHASE OF ASSETS',
       'Data_lagged_MAINTENANCE / REPAIR OF BUSINESS ASSETS',
       'Data_lagged_PURCHASE OF RAW MATERIAL / INVENTORY',
       'Data_lagged_PAYMENT OF SALARIES',
       'Data_lagged_PAYMENT OF UTILITY BILLS', 'Data_lagged_PAYMENT OF RENT',
       'Data_lagged_CONSTRUCTION OR IMPROVEMENT OF BUSINESS PLACE',
       'Data_lagged_LOAN_AMT_APP', 'count_adv',
       'avg_days_delayed', 'months_sinceLastLoan', 'mnth_since_del',
       'mnth_since_od', 'del_last2', 'od_last2', 'del_last6', 'od_last6'
                  ]          
numerical_df=merged_df[df_col_normalized]

print(numerical_df)


numerical_df_scaled = numerical_df.copy()

numerical_df_scaled[numerical_df_scaled.columns] = StandardScaler().fit_transform(numerical_df_scaled)
numerical_df_scaled.fillna(0,inplace=True)

kmeans_model = KMeans()     # instantiating KMeans model
numerical_df['LOAN_CODE']=merged_df['LOAN_CODE']

numerical_df_scaled['LOAN_CODE']=merged_df['LOAN_CODE']

categorical_features=set(merged_df.columns)-set(numerical_df.columns)
categorical_df=merged_df[list(set(merged_df.columns)-set(numerical_df.columns))]
categorical_df
categorical_df.drop(columns=['Disbursement_date','CNIC_EXP_DATE','MEMBERSHIP_DATE','BDO'],inplace=True)

categorical_features_encode=categorical_df.loc[:,(categorical_df.columns != 'CO_BWR_SAN_FLG') & (categorical_df.columns != 'BUSINESS_DURATION_YEARS')]

dummies_cat_features=pd.get_dummies(categorical_features_encode)
categorical_df['LOAN_CODE']=merged_df['LOAN_CODE']

dummies_cat_features['LOAN_CODE']=merged_df['LOAN_CODE']

dummies_cat_features['CO_BWR_SAN_FLG']=categorical_df['CO_BWR_SAN_FLG']

df_features_scaled=pd.concat([dummies_cat_features,numerical_df_scaled],axis=1)
df_features_scaled


df_features_scaled.to_csv('features_normalized_And_encoded.csv',index=False)


kmeans = KMeans(n_clusters=2)
kmeans.fit(df_features_scaled)


kmeans.labels_

df_features_scaled['labels']=kmeans.labels_



df_features_scaled.to_csv('featured_added_labels.csv',index=False)


