import numpy as np
import glob as glob
import pandas as pd

base_path = ""
file_name = "Demo_All_Merged.csv"
file = base_path + file_name

df = pd.read_csv(file, sep="~")

# Data correction
for col in ["LOAN_CODE", "EXPENSE_VALUE", "LOAN_UTILIZATION_AMOUNT", "LOAN_AMT_REQ", "LOAN_AMT_APP"]:
    df[col]=df[col].astype('str')
    df[col]=df[col].str.replace(",","")
for col in ["MEMBERSHIP_DATE","APPLICATION_DATE", "IN_CURRENT_AREA", "IN_CURRENT_HOUSE","CNIC_EXP_DATE"]:
    df[col] = pd.to_datetime(df[col])

df["EXPENSE_VALUE"] = df["EXPENSE_VALUE"].astype(float)
df["LOAN_UTILIZATION_AMOUNT"] = df["LOAN_UTILIZATION_AMOUNT"].astype(float) 
df["LOAN_AMT_REQ"] = df["LOAN_AMT_REQ"].astype(float)
df["LOAN_AMT_APP"] = df["LOAN_AMT_APP"].astype(float)

# Separating basic features
features = df[["PARTY_ID", "LOAN_CODE", "APPLICATION_DATE", "LOAN_CYCLE_NO", "BUSINESS_DURATION", "LOAN_AMT_APP", "LOAN_AMT_REQ",
               "NO_OF_CHILDREN", "NO_OF_DEPENDENTS", "NO_OF_EARNERS", "NO_OF_FAMILY_MEM", "IN_CURRENT_AREA", "IN_CURRENT_HOUSE", 
               "BRANCH_NAME", "OCCUPATION", "AREA_NAME","AGE","GENDER","MEMBERSHIP_DATE","CNIC_EXP_DATE","MARITAL_STATUS","HOUSE_STATUS","BDO","COMMUNITY","SECTOR","ACTIVITY","LOAN_USER","CO_BWR_SAN_FLG","OWENERSHIP_TYPE","BIZ_PRPRTY_OWENERSHIP","MONTHLY_INCOME","PRIMARY_INCOME","SECONDARY_INCOME","NDI","PSC_SCORE","EDU_LVL"]].drop_duplicates()
print(features.columns)
features["CONSUMER_RATIO"] = features["NO_OF_DEPENDENTS"]/features["NO_OF_FAMILY_MEM"]
features["EARNER_RATIO"] = features["NO_OF_EARNERS"]/features["NO_OF_FAMILY_MEM"]

# Calculate current area and house in months
for col in ["IN_CURRENT_AREA", "IN_CURRENT_HOUSE"]:
    features[col] = ((features["APPLICATION_DATE"] - features[col])/np.timedelta64(1, 'M'))

# Membership_duration is calculated by subtracting application date from membershipDate
features["MEMBERSHIP_DURATION"]=(features["APPLICATION_DATE"]-features["MEMBERSHIP_DATE"])/np.timedelta64(1, 'M')

#Recency of cnic expiration is calculated by subtracting cnic exp date application date
features["RECENCY_OF_CNIC_EXPIRATION"]=(features["CNIC_EXP_DATE"]-features["APPLICATION_DATE"])/np.timedelta64(1, 'M')

features["BUSINESS_DURATION_YEARS"] = features['BUSINESS_DURATION'].str.extract("(\d+) years")
features["BUSINESS_DURATION_MONTHS"] = features['BUSINESS_DURATION'].str.extract("(\d+) month")
features = features.fillna(0)
features["BUSINESS_DURATION"] = features["BUSINESS_DURATION_YEARS"].astype(int)*12 + features["BUSINESS_DURATION_MONTHS"].astype(int)

# Make columns from all expense types
expenses = df.sort_values('EXPENSE_VALUE', ascending=False)\
    .drop_duplicates(["PARTY_ID", "APPLICATION_DATE", "LOAN_CODE", "LOAN_CYCLE_NO", "EXPENDITURE_DESC"]).sort_index()
expenses = expenses\
    .pivot_table('EXPENSE_VALUE', ["PARTY_ID", "APPLICATION_DATE", "LOAN_CODE", "LOAN_CYCLE_NO"], 'EXPENDITURE_DESC').reset_index()

#total_expenses = df.sort_values('EXPENSE_VALUE', ascending=False)\
#    .drop_duplicates(["PARTY_ID", "APPLICATION_DATE", "LOAN_CODE", "LOAN_CYCLE_NO", "EXPENDITURE_DESC"]).sort_index()
#total_expenses = df\
#    .groupby(["PARTY_ID", "APPLICATION_DATE", "LOAN_CODE", "LOAN_CYCLE_NO"])["EXPENSE_VALUE"].sum().reset_index()
#total_expenses\
#    .rename(columns = {"EXPENSE_VALUE": "TOTAL_EXPENSE_VALUE"}, inplace=True)

# Make columns for all loan types and get the previous loan utilization
loan_utilization = df.sort_values('LOAN_UTILIZATION_AMOUNT', ascending=False)\
    .drop_duplicates(["PARTY_ID", "APPLICATION_DATE", "LOAN_CODE", "LOAN_CYCLE_NO", "LOAN_UTILIZATION_TYPE"]).sort_index()

cols = list(loan_utilization["LOAN_UTILIZATION_TYPE"].unique())

loan_utilization = loan_utilization\
    .pivot_table('LOAN_UTILIZATION_AMOUNT', ["PARTY_ID", "APPLICATION_DATE", "LOAN_CODE", "LOAN_CYCLE_NO"], 'LOAN_UTILIZATION_TYPE').reset_index()

for col in cols:
    loan_utilization['Data_lagged_' + col] = loan_utilization\
        .sort_values(by=["PARTY_ID", "APPLICATION_DATE"], ascending=True)\
        .groupby(["PARTY_ID"])[col].shift(1)
    loan_utilization.drop(col, axis=1, inplace=True)

expenses.drop("APPLICATION_DATE", axis=1, inplace=True)
loan_utilization.drop("APPLICATION_DATE", axis=1, inplace=True)

all_features = pd.merge(features, expenses, on=["PARTY_ID", "LOAN_CODE", "LOAN_CYCLE_NO"], how="inner")
all_features = pd.merge(all_features, loan_utilization, on=["PARTY_ID", "LOAN_CODE", "LOAN_CYCLE_NO"], how="inner")

all_features["Data_lagged_" + "LOAN_AMT_APP"] = all_features\
    .sort_values(by=["PARTY_ID", "APPLICATION_DATE"], ascending=True)\
    .groupby(["PARTY_ID"])["LOAN_AMT_APP"].shift(1)
all_features.drop("LOAN_AMT_APP", axis=1, inplace=True)


all_features.sort_values(by=["PARTY_ID", "APPLICATION_DATE"], ascending=True).to_csv("demo_features_new.csv", index=False)

