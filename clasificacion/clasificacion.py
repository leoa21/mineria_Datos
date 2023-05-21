import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

#Tendremos dos categorias 0 - si el torneo es la copa america y 1 - si el torneo es el mundial
#Contaremos con la cantidad de goles anotados para cada equipo y el porcentaje de victorias 


df = pd.read_csv('csv/torneos_oficiales.csv')
goles = pd.read_csv('csv/goles.csv')

df.drop(['Unnamed: 0'], axis=1, inplace=True)
df.drop(['Neutral'], axis=1, inplace=True)
goles.drop(['Unnamed: 0'], axis=1, inplace=True)

#inner = pd.merge(df, goles, on=['Fecha', 'Local', 'Visitante'], how='left')

#goles[goles['Equipo'] == 'Argentina']

argentina_L = df[(df['Local'] == 'Argentina')]
argentina_L_torneo = argentina_L[(argentina_L['Torneo'] == 'FIFA World Cup') | (argentina_L['Torneo'] == 'Copa América')].reset_index(drop = True)
argentina_L_torneo = argentina_L_torneo.drop(['Local','Ciudad', 'Pais', 'Fecha'], axis=1)

argentina_V = df[(df['Visitante'] == 'Argentina')]
argentina_V_torneo = argentina_V[(argentina_V['Torneo'] == 'FIFA World Cup') | (argentina_V['Torneo'] == 'Copa América')].reset_index(drop = True)
argentina_V_torneo = argentina_V_torneo.drop(['Visitante','Ciudad', 'Pais', 'Fecha'], axis=1)
argentina_V_torneo


def clasifTorneo(columnaTorneo): 
    if columnaTorneo == 'Copa América': 
        return 0
    else: 
        return 1 

argentina_L_torneo['Grupo'] = argentina_L_torneo['Torneo'].apply(clasifTorneo)
argentina_V_torneo['Grupo'] = argentina_V_torneo['Torneo'].apply(clasifTorneo)

argentina_L_torneo['Resultado'] = pd.Series(dtype = object)
argentina_V_torneo['Resultado'] = pd.Series(dtype = object)


for i in range(len(argentina_L_torneo)):

    if argentina_L_torneo.iloc[i, -5] < argentina_L_torneo.iloc[i, -4]:
        argentina_L_torneo['Resultado'].iloc[i] = 'P'
    elif argentina_L_torneo.iloc[i, -5] > argentina_L_torneo.iloc[i, -4]:
        argentina_L_torneo['Resultado'].iloc[i] = 'G'
    else:
        argentina_L_torneo['Resultado'].iloc[i] = 'E'


for i in range(len(argentina_V_torneo)):

    if argentina_V_torneo.iloc[i, -4] < argentina_V_torneo.iloc[i, -5]:
        argentina_V_torneo['Resultado'].iloc[i] = 'P'
    elif argentina_V_torneo.iloc[i, -4] > argentina_V_torneo.iloc[i, -5]:
        argentina_V_torneo['Resultado'].iloc[i] = 'G'
    else:
        argentina_V_torneo['Resultado'].iloc[i] = 'E'

argentina_V_torneo_cp = argentina_V_torneo[argentina_V_torneo['Grupo'] == 0]
argentina_L_torneo_cp = argentina_L_torneo[argentina_L_torneo['Grupo'] == 0]
argentina_L_torneo_m = argentina_L_torneo[argentina_L_torneo['Grupo'] == 1]
argentina_V_torneo_m = argentina_V_torneo[argentina_V_torneo['Grupo'] == 1]


def datosEquipoL(lista_equiposV, columnaEquiposV, columnaGolesL, columnaResultadoL, columnaGrupo):
    #Recibe
    # columnaMinutosL_df -> Columna del dataframe que contiene los minutos en los que anotaron gol de local
    # lista_minutosL-> lista con los valores únicos de la columna minuto

    equipo = {

    }

    equipo_datos = {

    }

    for equipo1 in lista_equiposV:

        num_partidos = 0
        cant_goles = 0
        cant_victorias = 0

        for i in range(len(columnaEquiposV)):
            if equipo1 == columnaEquiposV.iloc[i]:

                num_partidos += 1
                cant_goles += columnaGolesL.iloc[i]
                grupo = columnaGrupo.iloc[i]

                if columnaResultadoL.iloc[i] == 'G':
                    cant_victorias += 1

            equipo_datos = {
                'goles_anotados': cant_goles,
                'num_partidos': num_partidos,
                'num_victorias': cant_victorias,
                'grupo': grupo
            }

        equipo[equipo1] = equipo_datos

    return equipo


def datosEquipoV(lista_equiposL, columnaEquiposL, columnaGolesV, columnaResultadoV, columnaGrupo):
    #Recibe
    # columnaMinutosL_df -> Columna del dataframe que contiene los minutos en los que anotaron gol de local
    # lista_minutosL-> lista con los valores únicos de la columna minuto

    equipo = {

    }

    equipo_datos = {

    }

    for equipo1 in lista_equiposL:

        num_partidos = 0
        cant_goles = 0
        cant_victorias = 0

        for i in range(len(columnaEquiposL)):
            if equipo1 == columnaEquiposL.iloc[i]:

                num_partidos += 1
                cant_goles += columnaGolesV.iloc[i]
                grupo = columnaGrupo.iloc[i]

                if columnaResultadoV.iloc[i] == 'G':
                    cant_victorias += 1

            equipo_datos = {
                'goles_anotados': cant_goles,
                'num_partidos': num_partidos,
                'num_victorias': cant_victorias,
                'grupo': grupo
            }

            equipo[equipo1] = equipo_datos

    return equipo


argentina_V_torneo_cp = argentina_V_torneo[argentina_V_torneo['Grupo'] == 0]
argentina_L_torneo_cp = argentina_L_torneo[argentina_L_torneo['Grupo'] == 0]
argentina_L_torneo_m = argentina_L_torneo[argentina_L_torneo['Grupo'] == 1]
argentina_V_torneo_m = argentina_V_torneo[argentina_V_torneo['Grupo'] == 1]

x_cp = datosEquipoL(lista_equiposV=list(argentina_L_torneo_cp['Visitante'].unique()), columnaEquiposV=argentina_L_torneo_cp['Visitante'],
                    columnaGolesL=argentina_L_torneo_cp['Goles_Local'], columnaResultadoL=argentina_L_torneo_cp['Resultado'], columnaGrupo=argentina_L_torneo_cp['Grupo'])
x_m = datosEquipoL(lista_equiposV=list(argentina_L_torneo_m['Visitante'].unique()), columnaEquiposV=argentina_L_torneo_m['Visitante'],
                    columnaGolesL=argentina_L_torneo_cp['Goles_Local'], columnaResultadoL=argentina_L_torneo_m['Resultado'], columnaGrupo=argentina_L_torneo_m['Grupo'])

y_cp = datosEquipoV(lista_equiposL=list(argentina_V_torneo_cp['Local'].unique()), columnaEquiposL=argentina_V_torneo_cp['Local'],
                    columnaGolesV=argentina_V_torneo_cp['Goles_Visitantes'], columnaResultadoV=argentina_V_torneo_cp['Resultado'], columnaGrupo=argentina_V_torneo_cp['Grupo'])
y_m = datosEquipoV(lista_equiposL=list(argentina_V_torneo_m['Local'].unique()), columnaEquiposL=argentina_V_torneo_m['Local'],
                    columnaGolesV=argentina_V_torneo_m['Goles_Visitantes'], columnaResultadoV=argentina_V_torneo_m['Resultado'], columnaGrupo=argentina_V_torneo_m['Grupo'])

a_localdf_cp = pd.DataFrame.from_dict(x_cp, orient='index')
a_localdf_cp = a_localdf_cp.reset_index()
a_localdf_cp.columns = ['Equipo', 'Goles Anotados',
                        'Num Partidos', 'Num Victorias', 'Grupo']

a_localdf_m = pd.DataFrame.from_dict(x_m, orient='index')
a_localdf_m = a_localdf_m.reset_index()
a_localdf_m.columns = ['Equipo', 'Goles Anotados',
                        'Num Partidos', 'Num Victorias', 'Grupo']

a_visitdf_cp = pd.DataFrame.from_dict(y_cp, orient='index')
a_visitdf_cp = a_visitdf_cp.reset_index()
a_visitdf_cp.columns = ['Equipo', 'Goles Anotados',
                        'Num Partidos', 'Num Victorias', 'Grupo']

a_visitdf_m = pd.DataFrame.from_dict(y_m, orient='index')
a_visitdf_m = a_visitdf_m.reset_index()
a_visitdf_m.columns = ['Equipo', 'Goles Anotados',
                        'Num Partidos', 'Num Victorias', 'Grupo']

n = pd.concat([a_localdf_cp, a_localdf_m])
m = pd.concat([a_visitdf_cp, a_visitdf_m])

arg_df = pd.concat([n, m], ignore_index=True)

#-------------------------- Modelo KNN ----------- 

cp_arg = arg_df[arg_df['Grupo'] == 0]

m_arg = arg_df[arg_df['Grupo'] == 1]

X = arg_df[['Goles Anotados', 'Num Victorias']]
y = arg_df['Grupo']

escalador = MinMaxScaler().fit(X.values)

X = escalador.fit_transform(X.values)

clasificador = KNeighborsClassifier(n_neighbors=3)
clasificador.fit(X, y)


num_victorias = 4
cant_goles = 8

nuevo = escalador.transform([[num_victorias, cant_goles]])
print("Clase", clasificador.predict(nuevo))

#plt.figure(figsize = (10, 15))
plt.scatter(cp_arg['Num Victorias'], cp_arg['Goles Anotados'], marker='*', color='blue',
            label='Clase 0: Copa America')
plt.scatter(m_arg['Num Victorias'], m_arg['Goles Anotados'], marker='*', color='red',
            label='Clase 1: Mundial')
plt.scatter(num_victorias, cant_goles, marker='P',
            color='green', label='Nuevo')

plt.ylabel('Goles Anotados')
plt.xlabel('Numero de Victorias')
plt.legend(bbox_to_anchor=(1, 0.2))
plt.savefig("clasificacion/clasificacion.png")

#plt.show()
