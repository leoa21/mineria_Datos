#Importamos las librerias necesarias
from random import uniform
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from random import uniform 
from math import ceil

#Leemos los csv's
df = pd.read_csv('csv/torneos_oficiales.csv')
goles = pd.read_csv('csv/goles.csv')


df.drop(['Unnamed: 0'], axis=1, inplace=True)
df.drop(['Neutral'], axis=1, inplace=True)
goles.drop(['Unnamed: 0'], axis=1, inplace=True)

#Dataframe unicamente con los datos de la FIFA World Cup
df1 = df[(df['Torneo'] == 'FIFA World Cup')]

#Concatenando los goles anotados con los juegos realizados
inner = pd.merge(df, goles, on=['Fecha', 'Local', 'Visitante'], how='left')

#Máximos goleadores en la historia de los mundiales
world_cup = inner[inner['Torneo'] == 'FIFA World Cup']
max_goleador_mundiales = world_cup['Anotador'].value_counts()

#Máximos goleadores en la historia de la Copa América
copa_america = inner[inner['Torneo'] == 'Copa América']
max_goleador_copaAmerica = copa_america['Anotador'].value_counts()

#Máximos goleadores en la historia de la golden cup
gold_cup = inner[inner['Torneo'] == 'Gold Cup']
max_goleador_goldCup = gold_cup['Anotador'].value_counts()

#Autogoles
autogoles = inner[inner['Autogol'] == True]
max_equipo_autogoles = autogoles['Equipo'].value_counts()

#Graficas de barras
#Cantidad de goles anotados por la seleccion de brasil a cada uno de los equipos en la Copa América

#Funcion para contar los goles de local
def cantidadGolesPaisL(df, columnaV_df, lista_equipos):
    #Recibe
    # df -> dataframe con los datos
    # columnaL_df -> La columna con los goles que se anotaron al equipo contrario
    # lista_equipo -> lista con los diferentes equipos a los que se enfrentó

    goles_porPaisL = {

    }

    for equipo1 in lista_equipos:
        acum = 0
        for i in range(len(columnaV_df)):
            if equipo1 == columnaV_df.iloc[i]:
                acum = df.iloc[i, -5] + acum
            goles_porPaisL[equipo1] = acum

    return goles_porPaisL

#Funcion para contar los goles de Visitante
def cantidadGolesPaisV(df, columnaL_df, lista_equipos):
#Recibe 
# df -> dataframe con los datos
# columnaL_df -> La columna con los goles que se anotaron al equipo contrario
# lista_equipo -> lista con los diferentes equipos a los que se enfrentó

    goles_porPaisV = {

    }

    for equipo1 in lista_equipos:
        acum = 0
        for i in range(len(columnaL_df)):
            if equipo1 == columnaL_df.iloc[i]:
                acum = df.iloc[i, -4] + acum
            goles_porPaisV[equipo1] = acum

    return goles_porPaisV


#De nuestro dataframe copa_america obtenemos, unicamente los juegos de brasil.
copa_america = df[df['Torneo'] == 'Copa América']

copa_america_gbrL = copa_america[(copa_america['Local'] == 'Brazil')]
copa_america_gbrV = copa_america[(copa_america['Visitante'] == 'Brazil')]

#Se los pasamos a nuestras funciones 
f = cantidadGolesPaisL(df=copa_america_gbrL, columnaV_df=copa_america_gbrL['Visitante'], lista_equipos=list(
    copa_america_gbrL['Visitante'].unique()))
r = cantidadGolesPaisV(df=copa_america_gbrV, columnaL_df=copa_america_gbrV['Local'], lista_equipos=list(
    copa_america_gbrV['Local'].unique()))

#Funcion para sumar dos diccionarios y los regresa en forma de dataframe
def sumaDict(dict1, dict2): 
    from collections import Counter

    dict_res = Counter(dict1) + Counter(dict2)

    dataframe = pd.DataFrame([[jugador, dict_res[jugador]] for jugador in dict_res.keys()], columns = ['Pais', 'Goles']) 

    return dataframe

u_df = sumaDict(f, r) 

sns.barplot(data=u_df, x='Goles', y='Pais', palette='viridis')
plt.title('Cantidad de goles anotados por la seleccion de Brasil a cada uno de los equipos de la Copa América')
plt.gcf().set_size_inches(15,8)
plt.savefig("visualizacionDatos/graficas/Cantidad de goles anotados por la seleccion de Brasil a cada uno de los equipos de la Copa América.png", dpi = 100)

#Maximos goleadores en la historia a nivel selección en torneos oficiales de la FIFA

#Funcion que cuenta los goles por jugador
def golesJugador(lista_anotadores, columna_df):
    #Recibe
    #lista_anotadores -> Lista con los diferentes anotadores en el dataframe
    #columna_df -> columna del dataframe con el nombre del jugador que anotó el gol

    goles_jugador = {

    }

    for i in range(len(lista_anotadores)):
        count = 0
        for jugador in columna_df:
            if jugador == lista_anotadores[i]:
                count += 1
        goles_jugador[lista_anotadores[i]] = count

    goles_jugador_df = pd.DataFrame([[jugador, goles_jugador[jugador]]
                                for jugador in goles_jugador.keys()], columns=['Jugador', 'Goles'])

    return goles_jugador_df #Regresamos el diccionario en forma de dataframe

goles_df = golesJugador(list(goles['Anotador'].unique()), goles['Anotador'])

gf = goles_df[goles_df['Goles'] >= 40]
gf = gf.sort_values('Goles', ascending=False)

sns.barplot(x="Goles", y="Jugador", data=gf, palette='colorblind')
plt.title('Maximos goleadores en la historia a nivel seleccion en torneos oficiales de la FIFA')
plt.gcf().set_size_inches(15, 8)
plt.savefig("visualizacionDatos/graficas/Maximos goleadores en la historia a nivel seleccion en torneos oficiales de la FIFA.png")

#Maximos goleadores en la historia de los mundiales
max_goleador_mundiales_df = max_goleador_mundiales.head(10)
max_goleador_mundiales_df.plot(kind='bar', width=0.9, color='blue')
plt.ylabel('Goles')
plt.xlabel('Jugador')
plt.yticks([i for i in range(0, 21, 3)])
plt.title('Maximos goleadores en la historia de los mundiales')
plt.tight_layout()
plt.savefig("visualizacionDatos/graficas/Maximos goleadores en la historia de los mundiales.png")

#Maximos goleadores en la historia de la Copa América
mg_copaAmerica_df = max_goleador_copaAmerica.head(10)
mg_copaAmerica_df.plot(kind='bar', width=0.9, color='orange')
plt.ylabel('Goles')
plt.xlabel('Jugador')
plt.yticks([i for i in range(0, 21, 2)])
plt.title('Maximos goleadores en la historia de la Copa América')
plt.tight_layout()
plt.savefig("visualizacionDatos/graficas/Maximos goleadores en la historia de la Copa América.png")

#Maximos goleadores en la historia de la Gold Cup
mg_goldCup_df = max_goleador_goldCup.head(10)
mg_goldCup_df.plot(kind = 'bar', width = 0.9)
plt.ylabel('Goles')
plt.xlabel('Jugador')
plt.yticks([i for i in range(0,21, 2)])
plt.title('Maximos goleadores en la historia de la Gold Cup')
#plt.gcf().set_size_inches(10, 10)
plt.tight_layout()
plt.savefig("visualizacionDatos/graficas/Maximos goleadores en la historia de la Gold Cup.png")

#Grafico de lineas
#Promedio de goles anotados y recibidos en la historia de los mundiales de 20 selecciones escogidas al azar

prom_goles_mundial = df1.groupby(['Local']).mean(numeric_only=True)
prom_goles_mundial = prom_goles_mundial.rename(
    columns={'Goles_Visitantes': 'Goles_Recibidos'})

lista_num = list(map(lambda x: ceil(x), list(uniform(0, 80) for _ in range(0, 20)))) #Lista con los numeros aleatorios
df_prom_gm = prom_goles_mundial.iloc[lista_num] 

sns.relplot(data = df_prom_gm, kind = "line")

plt.title('Promedio de goles anotados y recibidos de 20 selecciones en la historia de los mundiales')
plt.xlabel('Equipo')
plt.ylabel('Promedio Goles')
plt.xticks(rotation=90)

plt.gcf().set_size_inches(15, 8)
plt.savefig("visualizacionDatos/graficas/Promedio de goles anotados y recibidos de 20 selecciones en la historia de los mundiales.png")

#Graficas de pastel
#Porcentaje de goles de la seleccion mexicana en la historia de los mundiales

#Obtenemos solamente los datos del mundial
mundial = df[df['Torneo'] == 'FIFA World Cup']

#Obtenemos los partidos donde mexico a jugado de local y visitante
mundial_mxL = mundial[mundial['Local'] == 'Mexico']
mundial_mxV = mundial[mundial['Visitante'] == 'Mexico']

x = cantidadGolesPaisL(df=mundial_mxL, columnaV_df=mundial_mxL['Visitante'], lista_equipos=list(
    mundial_mxL['Visitante'].unique()))
y = cantidadGolesPaisV(df=mundial_mxV, columnaL_df=mundial_mxV['Local'], lista_equipos=list(
    mundial_mxV['Local'].unique()))

mundial_mx_df = sumaDict(x, y)
m = mundial_mx_df.sort_values('Goles', ascending=False)
m = m.head(14)

colors = sns.color_palette('pastel')
plt.pie(list(m['Goles']), labels=list(m['Pais']),colors=colors, autopct='%0.0f%%')
plt.title('Porcentaje de la cantidad de goles de la seleccion mexicana en la historia de los mundiales')
plt.gcf().set_size_inches(10, 5)
plt.savefig("visualizacionDatos/graficas/Porcentaje de la cantidad de goles de la seleccion mexicana en la historia de los mundiales.png")

#Porcentaje de goles por jugador de la seleccion mexicana en la historia de los mundiales
t = inner[(inner['Torneo'] == 'FIFA World Cup') & (inner['Equipo'] == 'Mexico')]
goleador_mx_mundiales = golesJugador(list(t['Anotador'].unique()), t['Anotador'])
goleador_mx_mundiales = goleador_mx_mundiales.sort_values('Goles', ascending=False)
goleador_mx_mundiales = goleador_mx_mundiales.head(10)

colors = sns.color_palette('pastel')
plt.pie(list(goleador_mx_mundiales['Goles']), labels=list(goleador_mx_mundiales['Jugador']), colors=colors, autopct='%0.0f%%')
plt.title('Porcentaje de la cantidad de goles por jugador de la seleccion mexicana en los mundiales')
plt.gcf().set_size_inches(10, 5)
plt.savefig("visualizacionDatos/graficas/Porcentaje de la cantidad de goles por jugador de la seleccion mexicana en los mundiales.png")

