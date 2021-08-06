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

#load in the raw data
df = pd.read_excel(r"C:\Users\tcary@suncor.com\Documents\Order of Merit week 1 test.xlsx")

#set table displays in ipython
pd.set_option("display.max_columns", 25)
pd.set_option("display.max_rows", None)



#function to calculate handicap
def handicap_eq(df):
    
    slope = {'Red':111,'White':123,'B/W':126,'Blue':129,'Silver':132,'Black':134}
    rating = {'Red':64.7,'White':68.7,'B/W':70.0,'Blue':71.0,'Silver':72.0,'Black':73.6}
    
    
    for index in df.index:
        
        value = round(df.loc[index,'Index']*(slope[df.loc[index,'Tee Box']]/113)+(rating[df.loc[index,'Tee Box']]-72))
        
        df.loc[index,'Handicap'] = value
        
        #df['Handicap'] = df['Handicap'].astype('int')
        
    return df

#calculate results, feed in the df, the current week and the current combined results df
def results(df,week,results_comb):
    
    #filter for given event
    comp = df['Event'] == week
    
    #define points for rankings
    point_chart={1:25,2:18,3:15,4:12,5:10,6:8,7:6,8:4,9:2}
    
    df = df[comp]
    
    #select the player and event data
    results_df=pd.DataFrame(df[['Player','Event']])
    
    
    for index in df.index:
        #calculate front 9 score
        results_df.loc[index,'Front 9']= df.loc[index,'Hole 1'] + df.loc[index,'Hole 2'] + df.loc[index,'Hole 3'] + df.loc[index,'Hole 4'] \
        + df.loc[index,'Hole 5'] + df.loc[index,'Hole 6'] + df.loc[index,'Hole 7'] + df.loc[index,'Hole 8'] + df.loc[index,'Hole 9']
        
        #calculate back 9 score                
        results_df.loc[index,'Back 9']= df.loc[index,'Hole 10'] + df.loc[index,'Hole 11'] + df.loc[index,'Hole 12'] + df.loc[index,'Hole 13'] \
        + df.loc[index,'Hole 14'] + df.loc[index,'Hole 15'] + df.loc[index,'Hole 16'] + df.loc[index,'Hole 17'] + df.loc[index,'Hole 18']               
        
        #total gross 
        results_df.loc[index,'Total Gross'] = results_df.loc[index,'Front 9'] + results_df.loc[index,'Back 9']
        
        #total net
        results_df.loc[index,'Total Net'] = results_df.loc[index,'Total Gross'] - df.loc[index,'Handicap']
    
    #sort the net values and then reset the index and make it a column to define rank    
    results_df = results_df.sort_values(['Total Net','Back 9'])
    results_df = results_df.reset_index()
    results_df['Rank'] = (results_df.index + 1)
    
    #loop that assigns points for a rank, gives 1 point otherwise
    for index,rank in enumerate(results_df['Rank']):
        if results_df.loc[index,'Rank'] <10:
            results_df.loc[index,'Points'] = point_chart[rank]
        else:
            results_df.loc[index,'Points'] = 1 
    #results_df['Event'] == week
    if len(results_df['Player'])<10:
        results_df['Points'] = results_df['Points']*0.5
    elif len(results_df['Player'])<15:
        results_df['Points'] = results_df['Points']*0.75
    
    
    for i in np.arange(len(results_df)-2):
        if results_df.loc[i+2,'Total Net'] == results_df.loc[i+1,'Total Net']:
            points_sum = results_df.loc[i+2,'Points'] + results_df.loc[i+1,'Points']
            results_df.loc[i+1,'Points'] = points_sum/2
            results_df.loc[i+2,'Points'] = points_sum/2
    #print(results_df)
    #append the weeks results to the main df     
    results_comb = results_comb.append(results_df)
    results_comb = results_comb.drop('index',axis=1)   
    return results_comb



#function to calculate total points so far
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

#%%
#initiate the sequence of results
    
#initiate results df week 0
results_comb=pd.DataFrame()    

df= handicap_eq(df)

results_comb = results(df,'Week 1',results_comb)

results_comb = results(df,'Week 2',results_comb) #run each week after the other

results_comb = results(df,'Week 3',results_comb)
#%%
total_scores = total_points(results_comb)

#print(total_scores)
#print(results_comb)

results_comb = results_comb.append(total_scores)
print(results_comb)

#%%
results_comb.to_csv(r"C:\Users\tcary@suncor.com\Documents\OOM_results.csv",index=False)
#results_comb = results_comb[['Player','Event','Front 9','Back 9','Total Gross','Total Net']]
#week = 'Week 1'
#for player in results_comb['Player'].unique().tolist():
#    print(results_comb.loc[results_comb['Player'] == player, 'Points'].sum())