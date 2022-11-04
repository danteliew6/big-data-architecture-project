import pandas as pd
import nltk.corpus
import string
from nltk.corpus import stopwords
import json

#Load CSV and keywords
jobs = pd.read_csv('jobsDB.csv')
data = json.load(open('keyword2.json'))

# Function to check job desc for keywords
def getskills(strIn):
    liout = []
    strIn = strIn.lower()
    checker = strIn.split()
    for i in keyword_list:
        if i in checker:
            liout.append(i)
    return liout

# Data cleaning 
stop_words = stopwords.words('english')
jobs['clean_job_description'] = jobs['job_description'].apply(lambda x: ' '.join([word.lower() for word in x.split() if word not in (stop_words)]))
jobs['clean_job_description'] = jobs['clean_job_description'].str.replace('[^\w\s]','')

# Narrow down job desc to keywords
keyword_list = data['skills']
def getskills(strIn):
    liout = []
    checker = strIn.split()
    for i in keyword_list:
        if i in checker:
            liout.append(i)
    return liout
jobs['skills'] = jobs['clean_job_description'].apply(lambda x: getskills(x))

# Clean up columns
result = jobs
result.insert(loc=3, column='uppersalary', value=['' for i in range(result.shape[0])])
result.insert(loc=3, column='lowersalary', value=['' for i in range(result.shape[0])])
result.drop(result.columns[[0]], axis=1, inplace=True) 
result.drop(['job_description','clean_job_description'], axis=1, inplace=True)

result.to_parquet('cleanjobsdb.parquet')