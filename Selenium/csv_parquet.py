import pandas as pd
import pyarrow

df = pd.read_csv('x.csv')

df.to_parquet('monster.parquet')