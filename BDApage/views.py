from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import json
import numpy as np
from mlxtend.frequent_patterns import apriori
from mlxtend.preprocessing import TransactionEncoder
from collections import Counter
# Create your views here.
#request response 
#request handler

def process():
    df = pd.read_csv('BDApage/consolidated_jobs.csv')
    df = df.dropna(thresh=5)

    df['smean'] = (df['salary_lower'] +df['salary_upper'])/2

    df['company'] = df['company'].apply(lambda x: x.title())

    df1= df.groupby('company').mean().reset_index()

    df1 = df1.sort_values(['smean'], ascending=False)
    df1 = df1.drop(columns=['salary_lower','salary_upper'])

    df2 = df1.head(20)

    result= df2.to_dict('list')

    return result


def say_hello(request):
    mydata = process()
    return render(request, 'top_comp.html',{'mydata': mydata})

def popular_skillsets_chart(request):
    mydata = apriori_df()
    return render(request, 'popular_skillsets.html',{'mydata': mydata})

def popular_skills(request):
    mydata = wordcount_df()
    return render(request, 'popular_skills.html',{'mydata': mydata})

def job_title_chart(request):
    mydata = job_title_analysis()
    mydata2 = highest_paying_job_analysis()
    return render(request, 'job_title.html',{'mydata': mydata, 'mydata2': mydata2})

def popular_languages_chart(request):
    mydata = popular_programming_languages()
    return render(request, 'popular_languages.html',{'mydata': mydata})

def apriori_df():
    stop_words = ["experience", "support", "technology", "systems", "system", "business", "computer", "science", "management", "shortlistedcandidates", "resume", "applications", "application", "email", "personaldata", "privacy"]

    df = pd.read_csv('BDApage/consolidated_jobs.csv')
    df = df.dropna(thresh=5)
    skill_list = df['skills'].tolist()
    skill_list_cleaned = []    
    for i in skill_list:
        i = i[1:-1]
        i = i.replace(" ","")
        i = i.split(",")
        i = list(filter(lambda w: w not in stop_words, i))
        skill_list_cleaned.append(i)
    
    num_records = len(skill_list_cleaned)
    te = TransactionEncoder()  
    te_ary = te.fit(skill_list_cleaned).transform(skill_list_cleaned)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    frequent_itemsets = apriori(df, min_support=0.04, use_colnames=True)

    frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
    frequent_itemsets = frequent_itemsets[ (frequent_itemsets['length'] == 3) & (frequent_itemsets['support'] >= 0.03) ]

    frequent_skills = frequent_itemsets.sort_values("support",ascending=False).head(10)

    frequent_skills['count'] = frequent_skills['support'].apply(lambda x: round(x * num_records))
    frequent_skills = frequent_skills.to_dict("list")
    frequent_skills['itemsets'] = [list(x) for x in frequent_skills['itemsets']]

    return frequent_skills



def popular_programming_languages():
    popular_languages = ['abap', 'actionscript', 'ada', 'algol', 'alice', 'apl', 'asp / asp.net', 'assembly language', 'awk', 'bbc basic', 'c', 'c++', 'c#', 'cobol', 'cascading style sheets', 'd', 'delphi', 'dreamweaver', 'erlang and elixir', 'f#', 'forth', 'fortran', 'functional programming', 'go', 'haskell', 'html', 'idl', 'intercal', 'java', 'javascript', 'jquery', 'labview', 'lisp', 'logo', 'metaquotes language', 'ml', 'modula-3', 'ms access', 'mysql', 'nxt-g', 'object-oriented programming', 'objective-c', 'ocaml', 'pascal', 'perl', 'php', 'pl/i', 'pl/sql', 'postgresql', 'postscript', 'prolog', 'pure data', 'python', 'r', 'rapidweaver', 'ravendb', 'rexx', 'ruby on rails', 's-plus', 'sas', 'scala', 'sed', 'sgml', 'simula', 'smalltalk', 'smil', 'snobol', 'sql', 'sqlite', 'ssi', 'stata', 'swift', 'tcl/tk', 'tex and latex', 'unified modeling language', 'unix shells', 'verilog', 'vhdl', 'visual basic', 'visual foxpro', 'vrml', 'wap/wml', 'xml', 'xsl', 'bluehost', 'dreamhost', 'siteground', 'a2 hosting', 'greengeeks', 'hostinger', 'ado.net', 'ai programming', 'ascii encoding', 'backbone.js', 'books', 'cakephp', 'cgi', 'cocoa', 'codeigniter', 'cookies', 'corba', 'cvs', 'dom', 'extreme programming', 'ffmpeg', 'gate', 'git', 'gnustep', 'imagemagick', 'json', 'laravel', 'linked lists', 'machine learning', 'mantisbt', 'mdn', 'mercurial', 'mpi', 'msxml', 'ncurses', '.net', 'network programming', 'netcdf', 'oauth', 'opencl', 'openid', 'openssl', 'os development', 'phprojekt', 'project management', 'regex', 'robots', 'sorting algorithms', 'ssh', 'soap', 'subversion', 'url', 'vi', 'wcf', 'webkit web inspector', 'web standards', 'wsdl', 'wsgi', 'yui', 'zikula', 'chyrp', 'drupal coding standards', 'linux programming', 'mandriva linux', 'ms-dos', 'ms-windows', 'raspberry pi', 'ubuntu', 'umbraco', 'unix programming', 'xaraya']

    df = pd.read_csv('BDApage/consolidated_jobs.csv')
    df = df.dropna(thresh=5)
    skill_list = df['skills'].tolist()
    skill_list_cleaned = []    
    for i in skill_list:
        i = i[1:-1]
        i = i.replace(" ","")
        i = i.split(",")
        i = list(filter(lambda w: w in popular_languages, i))
        skill_list_cleaned.append(i)
    
    num_records = len(skill_list_cleaned)
    te = TransactionEncoder()  
    te_ary = te.fit(skill_list_cleaned).transform(skill_list_cleaned)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    frequent_itemsets = apriori(df, min_support=0.00001, use_colnames=True)

    frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
    frequent_itemsets = frequent_itemsets[(frequent_itemsets['length'] == 1) & (frequent_itemsets['support'] >= 0.00001) ]

    frequent_skills = frequent_itemsets.sort_values("support",ascending=False).head(20)

    frequent_skills['count'] = frequent_skills['support'].apply(lambda x: round(x * num_records))
    frequent_skills = frequent_skills.to_dict("list")
    frequent_skills['itemsets'] = [list(x)[0] for x in frequent_skills['itemsets']]

    frequent_languages_lst = []
    for i in range(len(frequent_skills['itemsets'])):
        temp = {}
        temp["x"] = frequent_skills['itemsets'][i]
        temp["value"] = frequent_skills['count'][i]
        frequent_languages_lst.append(temp)
    
    return_element = {"result": frequent_languages_lst}
    return return_element

def wordcount_df():

    df = pd.read_csv('BDApage/consolidated_jobs.csv')
    df.head()
    df['skill_list'] = df['skills'].apply(lambda x: x[1:-2].split(','))

    stop_words = ["singapore", "services", "service", "responsible","implementation","experience", "support", "technology", "systems", "system", "business", "computer", "science", "management", "shortlistedcandidates", "resume", "applications", "application", "email", "personaldata", "privacy"]
    full_list = []  # list containing all words of all texts
    for elmnt in df['skill_list']:  # loop over lists in df
        full_list += elmnt  # append elements of lists to full list
    skill_list_cleaned = []    
    for i in full_list:
        if i.strip() not in stop_words:
            skill_list_cleaned.append(i.strip())

    val_counts = pd.Series(skill_list_cleaned).value_counts()
    result = val_counts.head(20).to_dict()
    return result


def job_title_analysis():
    from nltk import ngrams
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from nltk.tokenize import RegexpTokenizer
    df = pd.read_csv('BDApage/consolidated_jobs.csv')
    #lowercase
    df["Text_1"] = df.job_title.str.lower()
    #remove \n
    df["Text_2"] = df.Text_1.str.replace("\\n", " ")
    df["Text_2"] = df.Text_2.apply(lambda x: str(x))

    df.head()
    #remove punctuation and tokenize
    df["Tokens"] = df.apply(lambda row: word_tokenize(row['Text_2']) if row['Text_2'] != None else None, axis=1)
    # #remove stopwords
    stop_words = set(stopwords.words('english'))
    df['Tokens_1'] = df['Tokens'].apply(lambda x: [item for item in x if item not in stop_words])
    # #merge tokens back into string text
    df['Text_3']=[" ".join(txt) for txt in df["Tokens_1"].values]
    # #create bigrams
    df["Tokens_2"] = df["Tokens_1"].apply(lambda row: list(ngrams(row, 2)))
    df = df.explode('Tokens_2')
    df['Tokens_2'] = df['Tokens_2'].str.join(" ")
    df["Text_2"] = df.Text_1.str.replace("\\n", " ")
    df['Tokens_3'] = df.Tokens_2.str.replace('[^a-zA-Z\\s]', ' ')
    df['Tokens_3'] = df.Tokens_3.str.strip(' ')
    df['job_title'] = df['Tokens_3']
    df = df.loc[df['job_title'] != '']
    df = df.loc[df['job_title'] != 'k']
    df = df.loc[df['job_title'] != 'contract']

    df['average_salary'] = df[['salary_lower', 'salary_upper']].mean(axis=1)

    df_grouped = df.groupby(['job_title']).agg(avg_salary=('average_salary','mean'), counts=('job_title','count')).reset_index()
    df_grouped = df_grouped.sort_values(['counts'], ascending=False)
    # df_grouped.drop(columns=['Text_1','Text_2', 'Tokens_1', 'Tokens', 'Text_3', 'Tokens_2'])
    result = df_grouped.head(10).to_dict('list')
    return result


def highest_paying_job_analysis():
    from nltk import ngrams
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from nltk.tokenize import RegexpTokenizer
    df = pd.read_csv('BDApage/consolidated_jobs.csv')
    df = get_clean_job_titles(df)
    #lowercase
    df["Text_1"] = df.job_title.str.lower()
    #remove \n
    df["Text_2"] = df.Text_1.str.replace("\\n", " ")
    df["Text_2"] = df.Text_2.apply(lambda x: str(x))

    df.head()
    #remove punctuation and tokenize
    df["Tokens"] = df.apply(lambda row: word_tokenize(row['Text_2']) if row['Text_2'] != None else None, axis=1)
    # #remove stopwords
    stop_words = set(stopwords.words('english'))
    df['Tokens_1'] = df['Tokens'].apply(lambda x: [item for item in x if item not in stop_words])
    # #merge tokens back into string text
    df['Text_3']=[" ".join(txt) for txt in df["Tokens_1"].values]
    # #create bigrams
    df["Tokens_2"] = df["Tokens_1"].apply(lambda row: list(ngrams(row, 2)))
    df = df.explode('Tokens_2')
    df['Tokens_2'] = df['Tokens_2'].str.join(" ")
    df["Text_2"] = df.Text_1.str.replace("\\n", " ")
    df['Tokens_3'] = df.Tokens_2.str.replace('[^a-zA-Z\\s]', ' ')
    df['Tokens_3'] = df.Tokens_3.str.strip(' ')
    df['job_title'] = df['Tokens_3']
    df = df.loc[df['job_title'] != '']
    df = df.loc[df['job_title'] != 'k']
    df = df.loc[df['job_title'] != 'contract']
    df['average_salary'] = df[['salary_lower', 'salary_upper']].mean(axis=1)

    df_grouped = df.groupby(['job_title']).agg(avg_salary=('average_salary','mean'), counts=('job_title','count')).reset_index()
    df_grouped = df_grouped.loc[df_grouped['counts'] > 30]
    df_grouped = df_grouped.sort_values(['avg_salary'], ascending=False)
    # df_grouped.drop(columns=['Text_1','Text_2', 'Tokens_1', 'Tokens', 'Text_3', 'Tokens_2'])
    result = df_grouped.head(25).to_dict('list')
    return result

def get_clean_job_titles(df):
    from nltk import ngrams
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from nltk.tokenize import RegexpTokenizer
    #lowercase
    df["Text_1"] = df.job_title.str.lower()
    #remove \n
    df["Text_2"] = df.Text_1.str.replace("\\n", " ")
    df["Text_2"] = df.Text_2.apply(lambda x: str(x))

    df.head()
    #remove punctuation and tokenize
    df["Tokens"] = df.apply(lambda row: word_tokenize(row['Text_2']) if row['Text_2'] != None else None, axis=1)
    # #remove stopwords
    stop_words = set(stopwords.words('english'))
    df['Tokens_1'] = df['Tokens'].apply(lambda x: [item for item in x if item not in stop_words])
    # #merge tokens back into string text
    df['Text_3']=[" ".join(txt) for txt in df["Tokens_1"].values]
    # #create bigrams
    df["Tokens_2"] = df["Tokens_1"].apply(lambda row: list(ngrams(row, 2)))
    df = df.explode('Tokens_2')
    df['Tokens_2'] = df['Tokens_2'].str.join(" ")
    df["Text_2"] = df.Text_1.str.replace("\\n", " ")
    df['Tokens_3'] = df.Tokens_2.str.replace('[^a-zA-Z\\s]', ' ')
    df['Tokens_3'] = df.Tokens_3.str.strip(' ')
    df['job_title'] = df['Tokens_3']
    df = df.loc[df['job_title'] != '']
    df = df.loc[df['job_title'] != 'k']
    df = df.loc[df['job_title'] != 'contract']
    return df


def show_range(request):
    mydata = find_by_range()
    return render(request, 'show_range.html', {'mydata':mydata})  

def processdict(dict_obj,y):
    most_common = dict(Counter(dict_obj).most_common(10))
    li =[]
    for k,v in most_common.items():
        li.append((k, round(v/y,3) ))
    return li

def find_by_range():
    df = pd.read_csv('BDApage/consolidated_jobs.csv')
    df = df.dropna()
    df = df[df['skills'] != '[]']
    df['smean'] = (df['salary_lower'] +df['salary_upper'])/2
    df1 = df.drop(columns=['salary_lower','salary_upper'])
    df1['range'] = pd.cut(df1['smean'], 3, 
    labels=['Freshgrad','Manager','Executive'])
    df1['range'].value_counts()
    key_words =['shortlisted candidates',"experience", "support", "technology", "systems",'service','services', "system", "business", "computer", "science", "shortlistedcandidates", "resume", "applications", "application", "email", "personaldata", "privacy"]

    final_list = []

    for x,y in df1.groupby('range'):
        skilldict = {} 
        for skills in y['skills']:
            skills =skills.strip('[')
            skills =skills.strip(']')
            li = skills.split(',')
            for i in li:
                if (i.strip() not in key_words):
                    if (i.strip() not in skilldict):
                        skilldict[i.strip()] = 1
                    else:
                        skilldict[i.strip()] =skilldict[i.strip()] +1
        top_list = processdict(skilldict,int(y['smean'].count()))
        obj = {
            'range': x,
            'mean':int(y['smean'].mean()),
            'std':int(y['smean'].std()),
            'count': int(y['smean'].count()),
            'top-skills': top_list
        }
        final_list.append(obj)

    return final_list