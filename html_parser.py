# Script name: html_parser
# Description: Parse html pages to retrieve article text
# Author: Mary Sanford
# Email: mpsanford17@gmail.com

import pandas as pd
import numpy as np
from lxml import etree
import bs4, time, urllib, glob, sys, codecs, pprint, re

# define global variables
urls = set()
total = pd.DataFrame(columns=['source','date','title'])
url_df = pd.DataFrame(columns=['source','url','date','title'])

# select HTML pages to parse
pages = ['French_Language_News2018-06-02_11-00','French_Language_News2018-06-02_11-06',
         'French_Language_News2018-06-02_11-07','French_Language_News2018-06-02_11-10',
         'French_Language_News2018-06-02_11-14']


# scrape each page
for p in pages:

    # open page
    f = codecs.open('text/LexisNexis/'+p+'.HTML', 'rb')
    # parse page into tree
    article = etree.iterparse(f,html=True)
    content = []

    err = re.compile(r'\xa0')
	
    # select each "span" element and append content of the element to the content list
    for i,elem in article:
        if elem.tag == "span":
            try:
                if elem.text != None:
                    if re.search(err,elem.text):
                        err.sub('',elem.text)
                    content.append(elem.text)
            except TypeError:
                print(type(elem.text))



    # remove weird chracters 
    for i in content:
        if i == '\xa0':
            content.remove(i)


    # scrape metadata (source, date, title); filter junk entries     
    n=1
    c=1
    urls = set()

    metadata = dict()
    meta_urls = dict()
    index_regex = re.compile(r'(\d*) of \d* DOCUMENTS')

    for i in content:

        try:
            ind = re.search(index_regex, i)

            if ind:

                if "http" in content[c+1]:
                    urls.add(content[c+1])
                    meta_urls[n] = [content[c], content[c+1], content[c+2], content[c+3]]
                
                elif len(content[c+1]) > 40:
                    metadata[n]=[content[c],content[c+2],content[c+3]]
                
                else:
                    metadata[n]=[content[c],content[c+1],content[c+2]]

                n+=1  

        except TypeError:
            print('Error')

        c+=1   
    
    print("Original length of df: " + str(len(metadata.items())))
    
    for i in urls:
        urls.add(i)

    #retrieve text of each artile 
    text = [i for i in content if re.search(index_regex,i) or len(i)>70]

    # put text into dictionary format
    text_dict = dict()
    n=1

    for i in text:
        index=re.search(index_regex,i)

        if index:
            n = index.group(1)
            m = int(n)
            text_dict[m]=[]
            continue

        else:
            text_dict[m].append(i)


    # generate dataframes for the metadata and text 
    cs = ['source','date','title']
    df = pd.DataFrame(metadata)
    df = df.T
    df.columns = cs 
    
    if len(meta_urls.items()) != 0:
        df_urls = pd.DataFrame(meta_urls)
        df_urls = df_urls.T
        df_urls.columns = ['source','url','date','title']
        url_df = url_df.append(df_urls)
    
    # join together all values for each entry (article)
    for i,v in text_dict.items():
        text_dict[i] = ''.join(v)


    # generate text df from text dictionary; merge with metadata df
    text_df = pd.DataFrame(pd.Series(text_dict), columns= ['text'])
    merged= df.merge(text_df, left_index = True, right_index = True)
    print("Length of merged dataframe before duplicate drop: " + str(len(merged_de)))
    
    # drop duplicates 
    merged = merged.drop_duplicates()
    print("Length of merged dataframe after duplicate drop: " + str(len(merged_de)))
    
    # determine how many junk entries we have 
    for i in merged['text']:
        try:
            words = i.split(' ')
            if len(words) < 300:
                ind = merged.index[merged['text']==i]
                merged = merged.drop(ind,axis=0)
    
        except AttributeError:
            print(merged.index[merged['text']==i])
            
    print("Final length of merged dataframe: " + str(len(merged)))
    
    print("Length of busted entries: " + str(len(urls)))
    
    total = total.append(merged)

# export to csv
total.to_csv('data',header=True,index=True)


# retrieve text from busted URLs
retrieved = pd.DataFrame(columns=['url','text'])
n = 1
errors=[]
for url in urls_de:
    
    req = urllib.request.Request(url, headers={'User-Agent': 'OII class 2018.1/msan'})
    

    # Use soup data structure to decode and then parase the page's text
    try:
        infile = urllib.request.urlopen(req)    
        text = infile.read()
        soup = bs4.BeautifulSoup(text.decode("ISO-8859-1"), "lxml")
    
    
        art = []

        for i, p in enumerate(soup.select('p')):

            if len(p.text.strip()) > 90:
                art.append(p.text.strip())

        retrieved.loc[n,'url'] = url
        retrieved.loc[n,'text'] = art
        
        
    except (UnicodeDecodeError, urllib.error.HTTPError) as e:
        print(str(e) + ": " + url +'\n')
        errors.append(url)
    
    n+=1

for i in retrieved['text']:
    ''.join(i)
    
agg = url_df.merge(retrieved, how="outer")


agg = agg.drop('url',axis=1)

total = pd.concat([de_total,agg], axis=0)

total.to_csv('all_de',header=True,index=True)
