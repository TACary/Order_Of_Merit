# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 21:04:22 2021

@author: Tim
"""

## Order of Merit 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as dt
import seaborn as sns

df = pd.read_excel(r"C:\Users\Tim\Documents\Python Scripts\Order of Merit.xlsx")

pd.set_option("display.max_columns", 25)
pd.set_option("display.max_rows", None)




def handicap_eq(df):
    
    slope = {'Red':111,'White':123,'B/W':126,'Blue':129,'Silver':132,'Black':134}
    rating = {'Red':64.7,'White':68.7,'B/W':70.0,'Blue':71.0,'Silver':72.0,'Black':73.6}
    
    
    for index in df.index:
        
        value = round(df.loc[index,'Index']*(slope[df.loc[index,'Tee Box']]/113)+(rating[df.loc[index,'Tee Box']]-72))
        
        df.loc[index,'Handicap'] = value
        
        #df['Handicap'] = df['Handicap'].astype('int')
        
    return df

def results(df,week,results_comb):
    
    comp = df['Event'] == week
    
    point_chart={1:25,2:18,3:15,4:12,5:10,6:8,7:6,8:4,9:2}
    
    df = df[comp]
    
    results_df=pd.DataFrame(df[['Player','Event']])
    
    for index in df.index:
        results_df.loc[index,'Front 9']= df.loc[index,'Hole 1'] + df.loc[index,'Hole 2'] + df.loc[index,'Hole 3'] + df.loc[index,'Hole 4'] \
        + df.loc[index,'Hole 5'] + df.loc[index,'Hole 6'] + df.loc[index,'Hole 7'] + df.loc[index,'Hole 8'] + df.loc[index,'Hole 9']
                        
        results_df.loc[index,'Back 9']= df.loc[index,'Hole 10'] + df.loc[index,'Hole 11'] + df.loc[index,'Hole 12'] + df.loc[index,'Hole 13'] \
        + df.loc[index,'Hole 14'] + df.loc[index,'Hole 15'] + df.loc[index,'Hole 16'] + df.loc[index,'Hole 17'] + df.loc[index,'Hole 18']               

        results_df.loc[index,'Total Gross'] = results_df.loc[index,'Front 9'] + results_df.loc[index,'Back 9']
        
        results_df.loc[index,'Total Net'] = results_df.loc[index,'Total Gross'] - df.loc[index,'Handicap']
        
    results_df = results_df.sort_values('Total Net')
    results_df = results_df.reset_index()
    results_df['Rank'] = (results_df.index + 1)
    
    for index,rank in enumerate(results_df['Rank']):
        if results_df.loc[index,'Rank'] <10:
            results_df.loc[index,'Points'] = point_chart[rank]
        else:
            results_df.loc[index,'Points'] = 1 
    #results_df['Event'] == week
        
    results_comb = results_comb.append(results_df)
    results_comb = results_comb.drop('index',axis=1)   
    return results_comb


results_comb=pd.DataFrame()

def total_points(results_comb):
    total_scores=pd.DataFrame(columns={'Player','Event','Points'})
    total_scores['Player'] = results_comb['Player'].unique().tolist()
    total_scores['Event'] ='Total'
    for index,player in enumerate(total_scores['Player']):
        
        total_scores.loc[index,'Points'] = results_comb.loc[results_comb['Player'] == player, 'Points'].sum()
    total_scores = total_scores.sort_values('Points',ascending =False)
    total_scores = total_scores.reset_index(drop=True)
    total_scores['Rank'] = (total_scores.index + 1)
    
    
    return total_scores

df= handicap_eq(df)

results_comb = results(df,'Week 1',results_comb)

results_comb = results(df,'Week 2',results_comb)

total_scores = total_points(results_comb)

#print(total_scores)
#print(results_comb)

results_comb = results_comb.append(total_scores)
print(results_comb)

results_comb.to_csv(r"C:\Users\Tim\Documents\Python Scripts\OOM_results.csv",index=False)
#results_comb = results_comb[['Player','Event','Front 9','Back 9','Total Gross','Total Net']]
#week = 'Week 1'
#for player in results_comb['Player'].unique().tolist():
#    print(results_comb.loc[results_comb['Player'] == player, 'Points'].sum())
