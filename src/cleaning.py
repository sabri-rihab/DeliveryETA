import pandas as pd

df = pd.read_csv('data/dataset.csv')
df.drop_duplicates()