import pyspark
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.functions import monotonically_increasing_id, col, udf
from datetime import date, datetime
from pyspark.sql.types import StringType, IntegerType

# uncomment the line below if nltk is not downloaded
# nltk.download()

spark = SparkSession.builder.appName('danteliew6.consolidate_parquet').getOrCreate()


# Load data
jobsdb_df = spark.read.load('/user/danteliew6/parquets/jobsDB.parquet')
grabjobs_df = spark.read.load('/user/danteliew6/parquets/grabjobs_cleaned.parquet')
indeed_df = spark.read.load('/user/danteliew6/parquets/indeed_cleaned.parquet')
jobstreet_df = spark.read.load('/user/danteliew6/parquets/jobstreet_cleaned.parquet')
monster_df = spark.read.load('/user/danteliew6/parquets/monster.parquet')
monster_df = monster_df.select('job_title', 'company', col('error1').alias('salary_lower'), col('error2').alias('salary_upper'), col("['skills']").alias('skills'))
jobsdb_df = jobsdb_df.select('job_title', 'company', col('lowersalary').alias('salary_lower'), col('uppersalary').alias('salary_upper'), str('skills'))

from functools import reduce  # For Python 3.x
from pyspark.sql import DataFrame
def unionAll(*dfs):
    return reduce(DataFrame.unionAll, dfs)

def formatSalary(text):
    if text == None or not text.isnumeric():
        return None
    salary = int(text)
    if salary < 10:
        return None
    # salary < 50 hourly pay, to format to monthly pay
    elif salary <= 50:
        salary = salary * 40 * 4
    #daily Salary
    elif salary <= 350:
        salary = salary * 30
    # Weekly salary
    elif salary <= 600:
        salary = salary * 4
    # salary > 25000 annual pay, to format to monthly pay
    elif salary >= 25000:
        salary = salary / 12
    return int(salary)

final_df = unionAll(grabjobs_df,indeed_df,jobstreet_df, monster_df, jobsdb_df)

colFormatSalary = udf(lambda z: formatSalary(z))
spark.udf.register("colFormatSalary", colFormatSalary)

final_df = final_df.withColumn("salary_lower_cleaned",colFormatSalary(col("salary_lower")).cast(IntegerType()))
final_df = final_df.withColumn("salary_upper_cleaned",colFormatSalary(col("salary_upper")).cast(IntegerType()))
final_df = final_df.select('job_title', 'company', col('salary_lower_cleaned').alias('salary_lower'), col('salary_upper_cleaned').alias('salary_upper'),'skills')

final_df.show()

#final_df.select('job_title', 'salary_lower').groupBy('job_title', 'salary_lower').agg(F.count("*")).orderBy(F.desc("salary_lower")).show()
#final_df = final_df.select('job_title', 'salary_lower').groupBy('job_title', 'salary_lower').agg(F.count("*")).orderBy(F.asc("salary_lower"))
#final_df.na.drop(subset=['salary_lower']).show()
final_df = final_df.toPandas()

final_df.to_parquet('~/consolidated_jobs.parquet')
final_df.to_csv('~/consolidated_jobs.csv', index=False)
