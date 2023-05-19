from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('csv/torneos_oficiales.csv')
goles = pd.read_csv('csv/goles.csv')

df.drop(['Unnamed: 0'], axis=1, inplace=True)
df.drop(['Neutral'], axis=1, inplace=True)
goles.drop(['Unnamed: 0'], axis=1, inplace=True)

francia = df[(df['Local'] == 'France') | (df['Visitante'] == 'France')] #Segmentamos nuestro dataframe solamente a los partidos de Francia

francia1 = francia.drop(['Fecha', 'Ciudad', 'Pais'], axis=1) #Eliminamos las columnas que no necesitaremos para nuestro analisis

francia1['Resultado'] = pd.Series() #Creamos una nueva columna donde pondremos si Francia Ganó, Empato o Perdió 


#Etiquetamos cada partido en dataframe si ganó, perdió o empató
for i in range(len(francia1)):
    if francia1['Local'].iloc[i] == 'France':
        if francia1.iloc[i, -4] < francia1.iloc[i, -3]:
            francia1['Resultado'].iloc[i] = 'P'
        elif francia1.iloc[i, -4] > francia1.iloc[i, -3]:
            francia1['Resultado'].iloc[i] = 'G'
        else:
            francia1['Resultado'].iloc[i] = 'E'
    else:
        if francia1.iloc[i, -4] < francia1.iloc[i, -3]:
            francia1['Resultado'].iloc[i] = 'G'
        elif francia1.iloc[i, -4] > francia1.iloc[i, -3]:
            francia1['Resultado'].iloc[i] = 'P'
        else:
            francia1['Resultado'].iloc[i] = 'E'

francia1 = francia1.reset_index(drop=True)


def datosEquipoL(lista_equiposV, columnaEquiposV, columnaGolesL, columnaResultadoL):
    #Recibe
    # lista_equiposV -> Lista con los valores unicos de los nombres de las selecciones que enfrentaron a Francia de visitante
    # columna_equiposV-> Columna del dataframe con el nombre de las selecciones selecciones ue enfrentaron a Francia de visitante
    # columnaGolesL -> Columna con la cantidad de goles que anotó Francia
    #columnaResultadoL -> Columna del dataframe que indica si Francia ganó, perdió o empató

    equipo = {

    }

    equipo_datos = {

    }

    for equipo1 in lista_equiposV:

        num_partidos = 0
        cant_goles = 0
        cant_victorias = 0
        cant_derrotas = 0
        cant_empates = 0

        for i in range(len(columnaEquiposV)):
            if equipo1 == columnaEquiposV.iloc[i]:

                num_partidos += 1
                cant_goles += columnaGolesL.iloc[i]

                if columnaResultadoL.iloc[i] == 'G':
                    cant_victorias += 1
                elif columnaResultadoL.iloc[i] == 'P':
                    cant_derrotas += 1
                else:
                    cant_empates += 1

            equipo_datos = {
                'goles_anotados': cant_goles,
                'num_partidos': num_partidos,
                'num_victorias': cant_victorias,
                'num_derrotas': cant_derrotas,
                'num_empates': cant_empates
                }

            equipo[equipo1] = equipo_datos

    return equipo


def datosEquipoV(lista_equiposL, columnaEquiposL, columnaGolesV, columnaResultadoV):
    #Recibe
    # lista_equiposL -> Lista con los valores unicos de los nombres de las selecciones que enfrentaron a Francia de local
    # columna_equiposV-> Columna del dataframe con el nombre de las selecciones selecciones ue enfrentaron a Francia de local
    # columnaGolesV -> Columna con la cantidad de goles que anotó Francia
    #columnaResultadoV -> Columna del dataframe que indica si Francia ganó, perdió o empató

    equipo = {

    }

    equipo_datos = {

    }

    for equipo1 in lista_equiposL:

        num_partidos = 0
        cant_goles = 0
        cant_victorias = 0
        cant_derrotas = 0
        cant_empates = 0

        for i in range(len(columnaEquiposL)):
            if equipo1 == columnaEquiposL.iloc[i]:

                num_partidos += 1
                cant_goles += columnaGolesV.iloc[i]

                if columnaResultadoV.iloc[i] == 'G':
                    cant_victorias += 1
                elif columnaResultadoV.iloc[i] == 'P':
                    cant_derrotas += 1
                else:
                    cant_empates += 1

            equipo_datos = {
                'goles_anotados': cant_goles,
                'num_partidos': num_partidos,
                'num_victorias': cant_victorias,
                'num_derrotas': cant_derrotas,
                'num_empates': cant_empates
            }

            equipo[equipo1] = equipo_datos

    return equipo


f_l = francia1[francia1['Local'] == 'France'] #Segmentamos unicamente a los partidos que jugó Francia de Local
f_v = francia1[francia1['Visitante'] == 'France'] #Segmentamos unicamente a los partidos que jugó Francia de Visitante

#Le pasamos los datos a las funcion
x = datosEquipoL(lista_equiposV = list(f_l['Visitante'].unique()), columnaEquiposV = f_l['Visitante'], columnaGolesL = f_l['Goles_Local'], columnaResultadoL = f_l['Resultado'])
y = datosEquipoV(lista_equiposL = list(f_v['Local'].unique()), columnaEquiposL = f_v['Local'], columnaGolesV = f_v['Goles_Visitantes'], columnaResultadoV = f_v['Resultado'])

#Convirtiendo los diccionarios obtenidos en dataframes 

#Dataframe Local
f_localdf = pd.DataFrame.from_dict(x, orient='index')
f_localdf = f_localdf.reset_index()
f_localdf.columns = ['Equipo', 'Goles Anotados', 'Num Partidos',
                    'Num Victorias', 'Num Derrotas', 'Num Empates']

#Dataframe Visitante
f_visitantedf = pd.DataFrame.from_dict(y, orient='index')
f_visitantedf.reset_index(inplace=True)
f_visitantedf.columns = ['Equipo', 'Goles Anotados',
                        'Num Partidos', 'Num Victorias', 'Num Derrotas', 'Num Empates']

#Como obtuvimos dos dataframe procederemos a juntarlos 
francia_dict = {}
index_local = []
index_visit = []

for i in range(len(f_localdf)):
    for j in range(len(f_visitantedf)):
        if f_localdf['Equipo'].iloc[i] == f_visitantedf['Equipo'].iloc[j]:
            francia_dict[f_localdf['Equipo'].iloc[i]] = {
            'Goles Anotados': f_localdf['Goles Anotados'].iloc[i] + f_visitantedf['Goles Anotados'].iloc[j],
            'Num Partidos': f_localdf['Num Partidos'].iloc[i] + f_visitantedf['Num Partidos'].iloc[j],
            'Num Victorias': f_localdf['Num Victorias'].iloc[i] + f_visitantedf['Num Victorias'].iloc[j],
            'Num Derrotas': f_localdf['Num Derrotas'].iloc[i] + f_visitantedf['Num Derrotas'].iloc[j],
            'Num Empates': f_localdf['Num Empates'].iloc[i] + f_visitantedf['Num Empates'].iloc[j]
            }

            index_local.append(f_localdf.index[i])
            index_visit.append(f_visitantedf.index[j])

f_localdf_new = f_localdf.drop(f_localdf.index[index_local])
f_visitantedf_new = f_visitantedf.drop(f_visitantedf.index[index_visit])

n = pd.concat([f_localdf_new, f_visitantedf_new])

f = pd.DataFrame.from_dict(francia_dict, orient='index')
f.reset_index(inplace=True)
f.columns = ['Equipo', 'Goles Anotados', 'Num Partidos',
            'Num Victorias', 'Num Derrotas', 'Num Empates']

francia_df = pd.concat([f, n], ignore_index=True) #Este sería nuestro dataframe con los datos que necesitamos

#-------------------------- Modelo de Clustering ------------------------

#Para nuestro modelo de clustering, 
#le pasaremos como variables el numero de victorias por equipo y la cantidad de goles que les ha anotado 

f_clustering = francia_df.iloc[:, [1, 3]]  #Segmentamos la información, solamente a esas dos columnas

escalador = MinMaxScaler().fit(f_clustering.values) #Escalamos los valores 

f_clustering = pd.DataFrame(escalador.transform(f_clustering.values),
                    columns=['Goles Anotados', 'Num Victorias'])


kmeans = KMeans(n_clusters=3).fit(f_clustering.values)

f_clustering['cluster'] = kmeans.labels_

print("Inercia: ",kmeans.inertia_)


plt.figure(figsize=(6, 5), dpi=100)

colores = ['red', 'blue', 'orange', 'black', 'purple', 'pink', 'brown']

for cluster in range(kmeans.n_clusters):
    plt.scatter(f_clustering[f_clustering['cluster'] == cluster]['Goles Anotados'],
                f_clustering[f_clustering['cluster'] == cluster]['Num Victorias'],
                marker='o', s=180, alpha=0.5, color=colores[cluster])

    plt.scatter(kmeans.cluster_centers_[cluster][0],
                kmeans.cluster_centers_[cluster][1],
                marker='P', s=280, color=colores[cluster])

plt.title('Francia k = 3 - Inercia = %0.2f' %kmeans.inertia_)
plt.xlabel('Goles Anotados')
plt.ylabel('Numero de Victorias')
plt.savefig("clustering/graficas/K - means con K = 3.png")

#plt.show()

#Metodo del codo para el numero de clusters

inercias = []

for k in range(2, 10):
    kmeans = KMeans(n_clusters=k).fit(f_clustering.values)
    inercias.append(kmeans.inertia_)

plt.figure(figsize=(6, 5), dpi=100)
plt.scatter(range(2, 10), inercias, marker='o', s=180, color='purple')
plt.xlabel('Numero de Clusters')
plt.ylabel('Inercia')
#plt.savefig("clustering/graficas/Grafica Inercia.png")

#plt.show()

#De acuerdo a la gráfica podemos observar que si hacemos 4 agrupaciones podemos obtener mejores resultados
#Se hara la prueba con k = 3, k = 4 y k = 5, para observar las diferencias
