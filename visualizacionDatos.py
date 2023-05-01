import pandas as pd

df = pd.read_csv('csv/torneos_oficiales.csv')
goles = pd.read_csv('csv/goles.csv')

inner = pd.merge(df, goles)

print(inner)
