# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 22:43:43 2018

@author: admin
"""

import pandas as pd

df = pd.read_csv("E:\\Datascience\\Project\\removed_duplicates.csv")
df = pd.read_csv("removed_duplicates.csv")
import numpy as np
# bill_amount
np.mean(df.bill_amount)
np.median(df.bill_amount)
df.bill_amount.mode()
np.var(df.bill_amount)
np.std(df.bill_amount)
df.bill_amount.skew()
df.bill_amount.kurt()

# value
np.mean(df.value)
np.median(df.value)
df.value.mode()
np.var(df.value)
np.std(df.value)
df.value.skew()
df.value.kurt()

## Transactions are done between 12/18/2017 & 04/04/2018
#df = df.loc[df['order_status'] == "delivered"]

df1 = df.iloc[:,1:]

df1.retailer_names.nunique() # 160 unique retailers we have.whose master_status is deliveried
df1.retailer_names.unique()  # Unique Retailor names


df1['created'] = pd.to_datetime(df1['created'])
#df1['TotalPrice'] = df1['Quantity'] * df1['UnitPrice']
df1['created'].min()   #  min date is 12/18/2017 
df1['created'].max()   # max date is 04/04/2018

import datetime as dt
NOW = dt.datetime(2018,4,14)
#df1['created'] = pd.to_datetime(df1['created'])

rfmTable = df1.groupby('retailer_names').agg({'created': lambda x: 
    (NOW - x.max()).days, 'master_order_id': lambda x: len(x), 'bill_amount':
        lambda x: x.sum()})
    

rfmTable['created'] = rfmTable['created'].astype(int)
rfmTable.rename(columns={'created': 'recency', 
                         'master_order_id': 'frequency', 
                         'bill_amount': 'monetary_value'}, inplace=True)

rfmTable.head()
first_retailer = df1[df1['retailer_names']=='RetailerID1'] # toget the total orders made by the perticular customer
#first_retailer.bill_amount.std()
#1533+1.96*(2878/5)

Avg = df1.groupby('retailer_names').agg({'bill_amount' : lambda x:x.mean()}).reset_index()
df1['bill_amount'] = df1.bill_amount.apply(pd.to_numeric, errors='coerce')
Std = df1.groupby('retailer_names').agg({'bill_amount' : lambda x:x.std()}).reset_index()
Count = df1.groupby('retailer_names').agg({'bill_amount' : lambda x:x.count()}).reset_index()

data = pd.DataFrame(columns = ['name','Avg','Std','Count'])
data['name'] = Avg.iloc[:,0]
data['Avg'] = Avg.iloc[:,1:]
data['Std'] = Std.iloc[:,1:]
data['Count'] = Count.iloc[:,1:]
data.to_csv('E:\\Datascience\\Project\RFM\\avg_data.csv')
data['Std'] = data.Std.fillna(0)

quantiles = rfmTable.quantile(q=[0.7,0.8,0.9])
quantiles = quantiles.to_dict()
segmented_rfm = rfmTable         
#The lowest recency, highest frequency and monetary amounts are our best customers.

def RScore(x,p,d):
    if x <= d[p][0.7]:
        return 4
    elif x <= d[p][0.8]:
        return 3
    elif x <= d[p][0.9]: 
        return 2
    else:
        return 1
    
def FMScore(x,p,d):
    if x <= d[p][0.7]:
        return 1
    elif x <= d[p][0.8]:
        return 2
    elif x <= d[p][0.9]: 
        return 3
    else:
        return 4
#Add segment numbers to the newly created segmented RFM table
segmented_rfm['r_quartile'] = segmented_rfm['recency'].apply(RScore, args=('recency',quantiles,))
segmented_rfm['f_quartile'] = segmented_rfm['frequency'].apply(FMScore, args=('frequency',quantiles,))
segmented_rfm['m_quartile'] = segmented_rfm['monetary_value'].apply(FMScore, args=('monetary_value',quantiles,))
segmented_rfm.head()

#RFM segments split the customer base into an imaginary 3D cube which is hard to visualize. However, we can sort it out.

segmented_rfm['RFMScore'] = segmented_rfm.r_quartile.map(str) +segmented_rfm.f_quartile.map(str)+segmented_rfm.m_quartile.map(str)
segmented_rfm.head()
segmented_rfm[segmented_rfm['RFMScore']=='444'].sort_values('monetary_value', ascending=False).head(10)
# Reatailer whose is having RFM Score 444 is the best retailer.
# Reatailer whose is having RFM Score 111 is the least retailer.
segmented_rfm.RFMScore.unique()
segmented_rfm.RFMScore.nunique()

segmented_rfm.to_csv('E:\\Datascience\\Project\\RFM\\New_files\\new_credit.csv')

result = segmented_rfm.sort_values('RFMScore',ascending=False).reset_index()
#rfm_score = segmented_rfm.sort_values('RFMScore',ascending=True)
#rfm_score.to_csv("E:\\Datascience\\Project\\rfm_result.csv")

#result.to_csv("E:\\Datascience\\Project\\RFM\\New_files\\new_result.csv")
#rfmTable.to_csv("E:\\Datascience\\Project\\rfm_table.csv")
#
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(40,8))
sns.barplot(result.retailer_names.head(52),result.monetary_value,alpha=0.8, color='red')
plt.xticks(rotation='60')

plt.savefig('top50.png')
plt.show()

## Recency Plot
plt.figure(figsize=(12,8))
sns.countplot(x='recency', data=result, color='green')
plt.ylabel('Count', fontsize=12)
plt.xlabel('Recency', fontsize=12)
plt.xticks(rotation='vertical')
plt.title('Frequency of Recency_Flag', fontsize=15)
plt.savefig('recency.png')

## Frequency plot
plt.figure(figsize=(12,8))
sns.countplot(x='frequency', data=result, color='green')
plt.ylabel('Count', fontsize=12)
plt.xlabel('frequency', fontsize=12)
plt.xticks(rotation='vertical')
plt.title('Frequency of Frequency_Flag', fontsize=15)
plt.savefig('frquency.png')
## Monetary_value
plt.figure(figsize=(40,8))
sns.countplot(x='monetary_value', data=result, color='green')
plt.ylabel('Count', fontsize=12)
plt.xlabel('Monetary_value', fontsize=6)
plt.xticks(rotation='vertical')
plt.title('Frequency of Monetary_Flag', fontsize=15)
plt.savefig('monetary.png')


