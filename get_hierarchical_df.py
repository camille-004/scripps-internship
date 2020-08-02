#!/usr/bin/env python
# coding: utf-8

# ### Turn Corrected Data Into a Hierarchical DataFrame to Facilitate Analysis

# In[161]:


import pandas as pd
import numpy as np
import os

os.chdir('visualizations')
from trend_visuals_transformed_data import norm_to_day
os.chdir('../')

def hierarchical_df(table):
    """
    Generates a hierarchical DataFrame from the transformed data.
    
    Keyword arguments:
    table -- The table to convert to a hierarchical DataFrame
    """
    df = pd.read_csv(table).drop(columns=['Unnamed: 0','Time'])
    subjs = np.unique(df['SubjectName'])
    
    # The only columns we want
    order = ['Day',
                 'TimeS',
                 'Study',
                 'SubjectName',
                 'Temp_Mean', 
                 'RespMean_Mean', 
                 'HR_Mean', 
                 'RR_Mean', 
                 'AOPAMean_Mean',
                 'Y']
    
    df_new = pd.DataFrame([
        df[column] for column in order if column in df.columns]).T
    cols = df_new.columns[4:]
    _, idx = np.unique([
        col.split('_')[0] for col in cols], return_index=True)
    cols = cols[np.sort(idx)][:-1]

    final = pd.DataFrame()

    # Create the new DataFrame
    for subj in subjs:
        subj_df = df_new[df_new['SubjectName'] == subj].reset_index()

        res = pd.DataFrame(index=[np.repeat(subj, len(cols)), cols])
        
        res['Day'] = list([norm_to_day(subj_df).values]) * len(cols)
        ma = [subj_df[col].rolling(48).mean().values for col in cols]
        res['Moving_Average'] = ma

        std = [subj_df[col].rolling(48).std().values for col in cols]
        res['Standard_Dev'] = std
    
        final = pd.concat([final, res])

    return final

