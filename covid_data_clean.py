# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 15:59:59 2020

@author: schir
"""
#Datetime To Convert Dates
from datetime import datetime

#Import Packages for Data
import pandas as pd
import statistics

#USA Data will be the dataframe for national data
site = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
us_df = pd.read_csv(site)

#Change to datetime
us_df['date'] = pd.to_datetime(us_df['date'])

#This function just appends to each data frame the number of days, so we don't have issues later with time data
days_after = []
for i in range(1,len(us_df['date'].to_list()) + 1):
    days_after.append(i)
us_df.insert(1,"days_since_start", days_after)

#This is a simple function that returns items based on their change over time. 
def total_change(input_list, rounded_val=2):
    total_list = []
    day_change = 0
    day_before = 0
    
    for day in input_list:
        try:
              day_change = day - day_before
        except:
              day_before = 0

        total_list.append(day_change)
        day_before = day
    return total_list

#This is a simple function that returns items based on their change over time. 
def percent_change(input_list, rounded_val=2):
    percent_list = []
    last_year = 0
    
    for this_year in input_list:
        try:
              pct_increase = ((this_year - last_year) / last_year) * 100
        except:
              pct_increase = 0

        percent_list.append(round(pct_increase,2))
        last_year = this_year

    percent_list = [round(i, rounded_val) for i in percent_list] #This function combines rounding inside of it, since percents are easier to use

    return percent_list

#Convert to total Change
cases_new = total_change(us_df['cases'].to_list())
deaths_new = total_change(us_df['deaths'].to_list())

#Insert Total Change
us_df.insert(3, "cases_increase", cases_new)
us_df.insert(5, "deaths_increase", deaths_new)

#Convert to Percent Change
cases_pct = percent_change(us_df['cases'].to_list())
deaths_pct = percent_change(us_df['deaths'].to_list())

#Insert Percent Change Change
us_df.insert(4, "cases_pct_inc", cases_pct)
us_df.insert(7, "deaths_pct_inc", deaths_pct)

#1 week, 2 week, 6 week
for i in range(14,1,-7):
    us_df.insert(4, f'{i}_day_cases', us_df['cases_increase'].rolling(i).mean())

for i in range(14,1,-7):
    us_df.insert(10, f'{i}_day_deaths', us_df['deaths_increase'].rolling(i).mean())

us_df.insert(6, '42_day_cases', us_df['cases_increase'].rolling(42).mean())
us_df.insert(12, f'42_day_deaths', us_df['deaths_increase'].rolling(42).mean())

#Save this as a df
us_df.to_csv('new_covid_data.csv')

