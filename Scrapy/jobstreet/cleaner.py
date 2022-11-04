#cleaner for indeed

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id, col, udf
from pyspark.sql.types import StringType
import string

from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
nltk.download('stopwords')
import string
from nltk.stem.porter import PorterStemmer

from collections import Counter
import json
import pandas as pd
import pyarrow


def cleanitup(text):
    from nltk.corpus import stopwords
    tokens = word_tokenize(text)
    tokens = [w.lower() for w in tokens]
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    words = [word for word in stripped if word.isalpha()]
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    # porter = PorterStemmer()
    # stemmed = [porter.stem(word) for word in words]
    filtered_sentence = (" ").join(words)
    final_text = filtered_sentence
    return (final_text)


def lowersalary(text):
    if text == None:
        return None
    split_salary = text.split(" - ")
    lower = ""
    for i in split_salary[0]:
        if i.isnumeric():
            lower += i
    return int(lower)

def uppersalary(text):
    if text == None:
        return None
    split_salary = text.split(" - ")
    idx = 1
    if len(split_salary) == 1:
        idx = 0  
    upper = ""

    for i in split_salary[idx]:
        if i.isnumeric():
            upper += i
    return int(upper)


def getskills(text):
    job_skills = []
    for i in skills:
        to_check = " " + i + " "
        if to_check in text:
            job_skills.append(i)
    return job_skills



spark = SparkSession.builder.appName('sg.edu.smu.is459.jobstreet').getOrCreate()


#Cleaning text function to udf
colcleanitup = udf(lambda z: cleanitup(z), StringType())
spark.udf.register("colcleanitup", colcleanitup)

collowersalary = udf(lambda z: lowersalary(z), StringType())
spark.udf.register("collowersalary", collowersalary)

coluppersalary = udf(lambda z: uppersalary(z), StringType())
spark.udf.register("coluppersalary", coluppersalary)

colgetskills = udf(lambda z: getskills(z), StringType())
spark.udf.register("colgetskills", colgetskills)

# Load data

with open('./keyword2.json', 'r') as myfile:
    skills_data = myfile.read()

skill = json.loads(skills_data)

skills = skill["skills"]

jobstreet_df = spark.read.load('/user/danteliew6/jobstreet.parquet')


jobstreet_df.show(10)
print(jobstreet_df.count())
# Clean the dataframe by removing rows with any null value and tokenizing text
jobstreet_df = jobstreet_df.na.drop('all')
jobstreet_df = jobstreet_df.dropDuplicates()
jobstreet_df = jobstreet_df.withColumn("job_description",colcleanitup(col("job_description")))
jobstreet_df = jobstreet_df.withColumn("salary_lower",collowersalary(col("salary")))
jobstreet_df = jobstreet_df.withColumn("salary_upper",coluppersalary(col("salary")))
jobstreet_df = jobstreet_df.withColumn("skills",colgetskills(col("job_description")))

jobstreet_df = jobstreet_df.drop("salary")
jobstreet_df = jobstreet_df.drop("job_description")


jobstreet_df.show(10)
print(jobstreet_df.count())

jobstreet_df = jobstreet_df.toPandas()

jobstreet_df.to_parquet('~/jobstreet_cleaned.parquet')

