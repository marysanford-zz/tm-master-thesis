# Script name: date_conversion
# Description: Normalise the dates parsed from the HTML files for use in R
# Author: Mary Sanford
# Email: mpsanford17@gmail.com

import pandas as pd
import numpy as np
import re

# import article dataframe
df_de = pd.read_csv("FILE PATHNAME HERE")

# create date column 
dates_de = df['date']

# initialise regex for date format DD/MM/YYYY 
date_a = re.compile(r'(\d{1,2}\.)(\s)(januar|februar|märz|april|mai|juni|juli|august|september|oktober|november|dezember)(\s)(\d{4})')

# initialise regex for date format MM/YYYY
date_b = re.compile(r'(januar|februar|märz|april|mai|juni|juli|august|september|oktober|november|dezember)(\s)(\d{4})')

n = 0

new_dates = pd.Series(index=np.arange(len(df_de['date'])))

# iterate over date column in original date frame
for i in dates:
    # make all strings lowercase and search item for regex's defined above
    i = i.lower()
    result_a = date_a.search(i)
    result_b = date_b.search(i)
    
    # strip and parse into DD/MM/YYYY format
    if result_a != None:
        try:
            day = result_a.groups()[0].strip('.')
            month = result_a.groups()[2]
            year = result_a.groups()[4][2:]

            months = {'januar':'1', 'februar':'2','märz':'3','april':'4','mai':'5','juni':'6','juli':'7',
                     'august':'8','september':'9','oktober':'10','november':'11','dezember':'12'}

            month = months[month]

            date = day + '.' + month + '.' + year

        except:
            print(i) 
    
    # strip and parse into MM/YYYY format 
    elif result_b != None:
        try:
            month = result_b.groups()[0]
            year = result_b.groups()[2][2:]
            
            month = months[month]
            
            date = "01." + month + "." + year
        
        except:
            print(i)
    
    else:
        date = i
    
    new_dates[n] = date
    n+=1


df_de['new_date'] = new_dates


# FRANCE 
df_fr=pd.read_csv("FILE PATHNAME HERE")
dates = df_fr['date']

date_a = re.compile(r'(\d{1,2})(\s)(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)(\s)(\d{4})')
date_b = re.compile(r'(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)(\s)(\d{4})')
date_c = re.compile(r'(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)(\s)(\d{1,2})(\s)(\d{4})')
n = 0

new_dates_fr = pd.Series(index=np.arange(len(df_fr['date'])))

for i in dates:
    i=i.lower()
    result_a = date_a.search(i)
    result_b = date_b.search(i)
    result_c = date_c.search(i)
    
    if result_a != None:
        try:
            day = result_a.groups()[0].strip('.')
            month = result_a.groups()[2]
            year = result_a.groups()[4][2:]

            months = {'janvier':'1', 'février':'2','mars':'3','avril':'4','mai':'5','juin':'6','juillet':'7',
                     'août':'8','septembre':'9','octobre':'10','novembre':'11','décembre':'12'}

            month = months[month]

            date = day + '.' + month + '.' + year
            #print("correct: " + date)

        except:
            #print("wrong: " + i) 
            pass
    
    elif result_b != None:
        try:
            month = result_b.groups()[0]
            year = result_b.groups()[2][2:]
            
            month = months[month]
            
            date = "01." + month + "." + year
            
            #print("correct: " + date)
        
        except:
            #print("wrong: " + i)
            #print(i)
            pass
    
    elif result_c != None:
        try:
            day = result_c.groups()[2]
            month = result_c.groups()[0]
            year = result_c.groups()[4][2:]
    
            month = months[month]
        
            date = day + '.' + month + '.' + year
        
        except:
            pass
    
    else:
        
        date = i
        print('error:' + i)
    
    new_dates_fr[n] = date
    n+=1

df_fr['new_date'] = new_dates_fr

# UK
df_uk=pd.read_csv("FILE PATHNAME HERE")
dates_uk = df_uk['date']

date_a = re.compile(r'(\d{1,2})(\s)(january|february|march|april|may|june|july|august|september|october|november|december)(\s)(\d{4})')
date_b = re.compile(r'(january|february|march|april|may|june|july|august|september|october|november|december)(\s)(\d{4})')
date_c = re.compile(r'(january|february|march|april|may|june|july|august|september|october|november|december)(\s)(\d{1,2}\,*)(\s)(\d{4})')
n = 0

new_dates_uk = pd.Series(index=np.arange(len(df_uk['date'])))

for i in dates_uk:
    i=i.lower()
    
    result_a = date_a.search(i)
    result_b = date_b.search(i)
    result_c = date_c.search(i)
    
    months = {'january':'1', 'february':'2','march':'3','april':'4','may':'5','june':'6','july':'7',
                     'august':'8','september':'9','october':'10','november':'11','december':'12'}


    if result_c != None:

        try:
            #print(result_c.groups())
            
            day = result_c.groups()[2].strip(',')
            
            month = result_c.groups()[0]
            month = months[month]
            
            year = result_c.groups()[4][2:]
            
            date = day + '.' + month + '.' + year
           
        except:
            pass
    
    
    elif result_a != None:

        try:
            day = result_a.groups()[0].strip('.')
            month = result_a.groups()[2]
            year = result_a.groups()[4][2:]
            
            month = months[month]

            date = day + '.' + month + '.' + year

        except:
            pass
    
    elif result_b != None:
        try:
            month = result_b.groups()[0]
            year = result_b.groups()[2][2:]
            
            month = months[month]
            
            date = "01." + month + "." + year
        
        except:
            pass 
   
    else:
        date = i
        print('error: '+i) 
    
    new_dates_uk[n] = date
    n+=1

df_uk['new_date'] = new_dates_uk


# US
df_us=pd.read_csv("FILE PATHNAME HERE")
dates_us = df_us['date']

date_a = re.compile(r'(\d{1,2})(\s)(january|february|march|april|may|june|july|august|september|october|november|december)(\s)(\d{4})')
date_b = re.compile(r'(january|february|march|april|may|june|july|august|september|october|november|december)(\s)(\d{4})')
date_c = re.compile(r'(january|february|march|april|may|june|july|august|september|october|november|december)(\s)(\d{1,2}\,*)(\s)(\d{4})')
n = 0

new_dates_us = pd.Series(index=np.arange(len(df_us['date'])))

for i in dates_us:
    i=i.lower()
    
    result_a = date_a.search(i)
    result_b = date_b.search(i)
    result_c = date_c.search(i)
    
    months = {'january':'1', 'february':'2','march':'3','april':'4','may':'5','june':'6','july':'7',
                     'august':'8','september':'9','october':'10','november':'11','december':'12'}


    if result_c != None:

        try:
            day = result_c.groups()[2].strip(',')
            
            month = result_c.groups()[0]
            month = months[month]
            
            year = result_c.groups()[4][2:]
            
            date = day + '.' + month + '.' + year
         
        except:
            pass
    
    
    elif result_a != None:
        try:
            day = result_a.groups()[0].strip('.')
            month = result_a.groups()[2]
            year = result_a.groups()[4][2:]

            
            month = months[month]

            date = day + '.' + month + '.' + year

        except:
            pass
    
    elif result_b != None:
        try:
            month = result_b.groups()[0]
            year = result_b.groups()[2][2:]
            
            month = months[month]
            
            date = "01." + month + "." + year

        
        except:
            pass 
   
    else:
        date = i
        print('error: '+i)
    
    
    new_dates_us[n] = date
    n+=1

df_us['new_date'] = new_dates_us


df_uk.to_csv('uk_data_updated.csv',header=True,index=True)
df_fr.to_csv('fr_data_updated.csv',header=True,index=True)
df_de.to_csv('de_data_updated.csv',header=True,index=True)
df_us.to_csv('us_date_updated.csv',header=True,index=True)

