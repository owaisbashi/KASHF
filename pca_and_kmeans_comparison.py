
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

df=pd.read_csv('featured_added_labels.csv')

repay_df=pd.read_csv('Repay_labels.csv')


comparing_dfs=pd.merge(repay_df,df,on=['LOAN_CODE'],how='inner')[['LOAN_CODE','LABEL','labels']]


comparing_dfs

comparing_dfs.groupby(["LABEL", "labels"]).size().reset_index(name='time')


df_final=pd.merge(repay_df,df,on=['LOAN_CODE'],how='inner')
df_final


df_final.drop(columns=['labels'],inplace=True)
df_final.head()

df_final.drop(columns=['ADVANCE','DEFAULT','DELINQUENT','SECURE'],inplace=True)



df_final=df_final[df_final['LABEL'].notna()]


df_final['LABEL'].value_counts(dropna=False)

df_final.loc[df_final['LABEL'] == 'ADVANCE', 'LABEL'] = 'SECURE'
df_final


df_final.loc[df_final['LABEL'] == 'DELINQUENT', 'LABEL'] = 'DEFAULT'
df_final.head()

colors = {'DEFAULT':'tab:blue', 'SECURE':'tab:orange'}
c=df_final['LABEL'].map(colors)



custom = [Line2D([], [], marker='.', color='red', linestyle='None'),
          Line2D([], [], marker='.', color='blue', linestyle='None')]

plt.legend(handles = custom, labels=['DEFAULT', 'SECURE'], bbox_to_anchor= (1.05, 0.5), loc= "lower left")


df=pd.read_csv('features_normalized_And_encoded.csv')
df


df_final['LABEL'].value_counts(dropna=False)


y=df_final['LABEL']
pca=PCA(n_components=2)

px=df_final.loc[:, df_final.columns != 'LABEL']
px_pf=pca.fit_transform(px)


principal_df=pd.DataFrame(data=px_pf,columns=['pc1','pc2'])
principal_df['target']=df_final['LABEL']
fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)
targets = ['SECURE','DEFAULT']
colors = [ 'g', 'b']
for target, color in zip(targets,colors):
    indicesToKeep = principal_df['target'] == target
    ax.scatter(principal_df.loc[indicesToKeep, 'pc1']
               , principal_df.loc[indicesToKeep, 'pc2']
               , c = color
               , s = 50)
ax.legend(targets)
ax.grid()


# # 3 comp pca
pca=PCA(n_components=2)
features=df_final.loc[:, df_final.columns != 'LABEL'].columns.to_list()
pcd3d_results=pca.fit_transform(df_final[features])
print(pcd3d_results[:,0])

sns.set_style('whitegrid')
fig=plt.figure(1,figsize=(8,6))
ax=Axes3D(fig, elev=-150, azim=110)
ax.scatter(pcd3d_results[:,0], pcd3d_results[:,1], pcd3d_results[:,2],
               c=c,
               s=40)

custom = [Line2D([], [], marker='.', color='tab:orange', linestyle='None'),
          Line2D([], [], marker='.', color='tab:blue', linestyle='None')]

plt.legend(handles = custom, labels=['SECURE','DEFAULT'], bbox_to_anchor= (1.05, 0.5), loc= "lower left")
ax.set_xlabel("1st eigenvector", fontsize=35)
ax.set_ylabel("2nd eigenvector", fontsize=35)
ax.set_zlabel("3rd eigenvector", fontsize=35)

