import pandas as pd

df = pd.read_csv('csv/results.csv')

#Cambiando el nombre a las columnas
columnas = ['Fecha', 'Local', 'Visitante', 'Goles_Local',
            'Goles_Visitantes', 'Torneo', 'Ciudad', 'Pais', 'Neutral']

df.columns = columnas

df['Fecha'] = pd.to_datetime(df['Fecha'])

#Acotamos el dataframe solamente a ciertos torneros
df1 = df[(df['Torneo'] == 'UEFA Nations League') | (df['Torneo'] == 'CONCACAF Nations League League') | (df['Torneo'] == 'Confederations Cup') | (df['Torneo'] == 'Gold Cup') | (df['Torneo'] == 'Oceania Nations Cup') | (
    df['Torneo'] == 'UEFA Euro') | (df['Torneo'] == 'African Cup of Nations') | (df['Torneo'] == 'FIFA World Cup qualification') | (df['Torneo'] == 'FIFA World Cup') | (df['Torneo'] == 'Copa América')]
lista = [i for i in range(1, 11856)]
df1.index = lista

print(df1.describe())

#Mediana
print("\nMediana:\n",  df1.median(numeric_only=True))

#Moda
print(f"\nModa goles local: {df1['Goles_Local'].mode()[0] }")
print(f"Moda goles visitante: {df1['Goles_Visitantes'].mode()[0]}")
print(f"Moda equipo local: {df1['Local'].mode()[0]}")
print(f"Moda equipo visitante: {df1['Visitante'].mode()[0]}")

print("\nPromedio de goles de la seleccion de Brasil en los mundiales que ha participado:\n", df1[(df1['Torneo'] == 'FIFA World Cup')].mean(numeric_only= True))

print("\nCantidad de goles que ha anotado diferentes selecciones en los torneos oficiales que han participado:\n", df1.groupby(['Local', 'Torneo']).sum(numeric_only=True))

df2 = df1[(df1['Torneo'] == 'FIFA World Cup')]

print("\nPromedio de goles realizados en los mundiales desde 1939 - 2022 por las diferentes selecciones que han participado:\n",
      df2.groupby(['Local']).mean(numeric_only = True))
