"""
Created on Wed Jul  8 17:16:18 2020

@author: carlosbrown
"""
import pandas as pd

def plot_pivot(df, by='PESI Class', outcome='adverseEvent'):
    df_test = pd.DataFrame(df.groupby(by)[outcome].value_counts()).unstack().reset_index()
    df_test.columns = df_test.columns.droplevel(0)
    df_test.rename(columns={'':by}, inplace=True)
    df_melt = df_test.melt(id_vars=by)
    df_melt.rename(columns={'variable':outcome, 'value':'count'}, inplace=True)
    df_melt[outcome].replace(0,'No', inplace=True)
    df_melt[outcome].replace(1,'Yes', inplace=True)
    return df_melt