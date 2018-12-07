#!/usr/bin/env python
# coding: utf-8

from tqdm import tqdm
import pandas as pd
import csv

#Import website list from csv
df_pid = pd.read_csv('ENTER CSV FILE HERE.csv')
print(df_pid.head())
print(len(df_pid))

#Initialize variables needed for loop
pid_row = 0
pid_pass = []
df_action_logs = []
df_action_logs_all_append = []

#Loop through list
for pid_row in tqdm(range(0,len(df_pid))):

    #Acquire string from list
    pid_num = df_pid.iloc[pid_row][0]

    #Insert string into url
    url = pid_num

    try:
        #Assign the list of dataframes from the url to df_tables
        df_tables = pd.read_html(url, header = 0)

        #Used for the first action log
        if len(df_action_logs_all_append) == 0:
            df_action_logs_all_append = df_tables[1]
            df_action_logs_all_append['nc_pid'] = pid_num
                    #print(df_action_logs_all_append)

        #Append everything henceforth
        else:
            df_action_logs = df_tables[1]
            df_action_logs['nc_pid'] = pid_num
            df_action_logs_all_append = df_action_logs_all_append.append(df_action_logs)

    #This will handle error from a url that does not contain tables
    except ValueError:
        print('error')
        pid_pass.append(pid_num)
        pass

#Format the final action log dataframe
df_action_logs_col = ['step', 'hrs', 'date', 'action_log', 'doa_step', 'child_pn', 'files', 'pid']
df_action_logs_all_append.columns = df_action_logs_col
df_action_logs_all_append.head()

df_action_logs_all_append.shape

#Identify all the problem urls
print(pid_pass)

#Export to csv
df_action_logs_all_append.to_csv('EXPORT FILENAME HERE.csv')
