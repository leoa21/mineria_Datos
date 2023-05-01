import pandas as pd 

df = pd.read_csv('csv/results.csv')

#Cambiando el nombre a las columnas
columnas = ['Fecha', 'Local', 'Visitante', 'Goles_Local',
            'Goles_Visitantes', 'Torneo', 'Ciudad', 'Pais', 'Neutral']

df.columns = columnas

df['Fecha'] = pd.to_datetime(df['Fecha'])

goals = pd.read_csv('csv/goalscorers.csv')

#Cambiando el nombre a las columnas
columnas_goles = ['Fecha', 'Local', 'Visitante', 'Equipo', 'Anotador',
            'Minuto', 'Autogol', 'Penal']

goals.columns = columnas_goles

goals['Fecha'] = pd.to_datetime(goals['Fecha'])

#Acotamos el dataframe para que solo nos muestre los torneos avalados por la FIFA
df1 = df[(df['Torneo'] == 'UEFA Nations League') | (df['Torneo'] == 'CONCACAF Nations League League') | (df['Torneo'] == 'Confederations Cup') | (df['Torneo'] == 'Gold Cup') | (df['Torneo'] == 'Oceania Nations Cup') | (
    df['Torneo'] == 'UEFA Euro') | (df['Torneo'] == 'African Cup of Nations') | (df['Torneo'] == 'FIFA World Cup qualification') | (df['Torneo'] == 'FIFA World Cup') | (df['Torneo'] == 'Copa América')]
lista = [i for i in range(1, 11856)]
df1.index = lista

print(df1)
print(goals)

df1.to_csv("csv/torneos_oficiales.csv")
goals.to_csv("csv/goles.csv")

