import glob as glob
import pandas as pd 
from pyarrow import csv

base_path = "D:\\Sindh Complete Data Csv\\Raw csvs\\"

files = glob.glob(base_path + "*.csv")

repay_rename = {"REGION_NAME": "REGION_NAME", 
    "AREA_NAME": "AREA_NAME", 
    "BRANCH": "BRANCH_NAME", 
    "CLNT_SEQ": "CLIENT_PARTY_ID", 
    "LOAN_APP_SEQ": "LOAN_CODE", 
    "DSBMT_DT": "DISBURSMENT_DATE", 
    "PRD_GRP_NM": "PRODUCT_DESC", 
    "LOAN_CYCL_NUM": "LOAN_CYCLE_CD", 
    "INST_NUM": "INSTALLMENT_NO", 
    "DUE_DT": "PAYMENT_DATE", 
    "PPAL_AMT_DUE": "PRINCIPLE_AMOUNT_DUE", 
    "PAID_DT": "PAID_DATE", 
    "REF_CD_DSCR": "PAYMENT_STATUS"}

demo_rename = {"EX_DESC": "EXPENDITURE_DESC", 
    "EXP_AMT": "EXPENSE_VALUE", 
    "LOAN_UTILIZTION_TYPE": "LOAN_UTILIZATION_TYPE",
    "BIZ_OWENERSHIP_TYPE": "OWENERSHIP_TYPE",
    "CLNT_REL_SEQ": "REL_PARTY_ID"}

demo_cols = ["REGION_NAME","AREA_NAME","BRANCH_NAME","BRANCH_CD","PARTY_ID",
    "MEMBERSHIP_DATE","APPLICATION_DATE","LOAN_CODE","DISBURSMENT_DATE",
    "LOCATION","PARTY_TYPE","REL_PARTY_ID","RELATION","NAME",
    "FATHER_NAME","SPOUSE_NAME","BIRTH_DT","AGE","GENDER",
    "CNIC_EXP_DATE","FAMILY_NO","MARITAL_STATUS","HOUSE_STATUS",
    "NO_OF_CHILDREN","NO_OF_DEPENDENTS","NO_OF_EARNERS",
    "NO_OF_FAMILY_MEM","BDO","EMP_PARTY_ID","PRODUCT","COMMUNITY",
    "SECTOR","ACTIVITY","LOAN_AMT_REQ","LOAN_AMT_APP","LOAN_PURPOSE",
    "BUSINESS_DURATION","LOAN_USER","IN_CURRENT_AREA","IN_CURRENT_HOUSE",
    "NOMINEE","CO_BORRWER","OWENERSHIP_TYPE","MONTHLY_INCOME",
    "EXPENDITURE_DESC","EXPENSE_VALUE","BUSSINESS_ADDRESS","NDI",
    "LOAN_CYCLE_NO","OCCUPATION","LOAN_UTILIZATION_TYPE",
    "LOAN_UTILIZATION_AMOUNT","BUS_APP_ID","APPLICATION_ID"]

dfs_demo = []
dfs_repay = []
for file in files:
    if "ProfileInfo" in file:
        df = pd.read_csv(file)
        df.rename(columns = demo_rename, inplace=True)
        dfs_demo.append(df[demo_cols])
    if "Repayment" in file:
        df = pd.read_csv(file)
        df.rename(columns = repay_rename, inplace=True)
        dfs_repay.append(df)

df_all = pd.concat(dfs_demo)
df_all.to_csv("Demo_All_Merged.csv", index=False, sep="~")

df_all = pd.concat(dfs_repay)
df_all.to_csv("Repayment_All_Merged.csv", index=False, sep="~")
