import pandas as pd 

df = pd.read_csv('csv/results.csv')

#Cambiando el nombre a las columnas
columnas = ['Fecha', 'Local', 'Visitante', 'Goles_Local',
            'Goles_Visitantes', 'Torneo', 'Ciudad', 'Pais', 'Neutral']

df.columns = columnas

df['Fecha'] = pd.to_datetime(df['Fecha'])

