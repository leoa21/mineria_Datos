#Estadistica Descriptiva

import pandas as pd

df = pd.read_csv('csv/torneos_oficiales.csv')
goles = pd.read_csv('csv/goles.csv')

df.drop(['Unnamed: 0'], axis=1, inplace=True)
df.drop(['Neutral'], axis = 1, inplace=True)
goles.drop(['Unnamed: 0'], axis=1, inplace=True)

print(df.describe())

#Mediana
print("\nMediana:\n",  df.median(numeric_only=True))

#Moda
print(f"\nMaxima cantidad de goles de un equipolocal: {df['Goles_Local'].max()}")
print(f"Maxima cantidad de goles del equipo visitante: {df['Goles_Visitantes'].max()}")
print(f"El equipo local que más se repita: {df['Local'].mode()[0]}")
print(f"El equipo visitante que más se repite: {df['Visitante'].mode()[0]}")

print("\nPromedio de goles de la seleccion de Brasil en torneos oficales:\n",
      df[(df['Local'] == 'Brazil')].mean(numeric_only=True))

print("\nCantidad de goles que ha anotado diferentes selecciones en los torneos oficiales que han participado:\n",
      df.groupby(['Local', 'Torneo']).sum(numeric_only=True))

df1 = df[(df['Torneo'] == 'FIFA World Cup')]

print("\nPromedio de goles realizados en los mundiales desde 1939 - 2022 por las diferentes selecciones que han participado:\n",
      df1.groupby(['Local']).mean(numeric_only=True))

#Concatenando los goles anotados con los juegos realizados 
inner = pd.merge(df, goles, on=['Fecha', 'Local', 'Visitante'], how='left')

#Acotando solamente a los juegos del mundial
world_cup = inner[inner['Torneo'] == 'FIFA World Cup']

#Máximo anotador en la historia de los mundiales
max_goleador_mundiales = world_cup['Anotador'].value_counts()
print("Maximo goleador en la historia de los mundiales:", max_goleador_mundiales.head(1))

#TOP 3 
print("\nMaximos goleadores en la historia de los mundiales\n",
      max_goleador_mundiales.head(5))

copa_america = inner[inner['Torneo'] == 'Copa América']


#Máximo anotador en la historia de la Copa América
print("")
max_goleador_copaAmerica = copa_america['Anotador'].value_counts()
print("Maximo goleador en la historia de la Copa América:",
      max_goleador_copaAmerica.head(1))

#TOP 5
print("\nMaximos goleadores en la historia de la Copa América\n",
      max_goleador_copaAmerica.head(5))

gold_cup = inner[inner['Torneo'] == 'Gold Cup']

#Máximo anotador en la historia de la golden cup
max_goleador_goldCup = gold_cup['Anotador'].value_counts()
print("")
print("Maximo goleador en la historia de la Gold Cup:",
      max_goleador_goldCup.head(1))

#TOP 5
print("\nMaximos goleadores en la historia de la Gold Cup\n",
      max_goleador_goldCup.head(5))

print("")
#Autogoles
autogoles = inner[inner['Autogol'] == True]
max_equipo_autogoles = autogoles['Equipo'].value_counts()
print("Las tres selecciones con mas goles en propia puerta en torneos oficiales\n", max_equipo_autogoles.head(3))


