import pyspark
from pyspark.sql import SparkSession
import pandas as pd

# Create session
spark = SparkSession.builder.appName('sg.edu.smu.is459.grabjobs').getOrCreate()

# Convert data to CSV
df = pd.read_parquet('../jobsDB.parquet')
df.to_csv('jobsDB.csv')

