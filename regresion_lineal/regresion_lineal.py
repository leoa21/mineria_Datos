import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from scipy.stats import pearsonr
from sklearn import linear_model
import pandas as pd

#Queremos probar si existe correlacion entre el promedio de goles y los minutos
#tomando en cuenta los goles la selección argentina en la copa américa desde 1916 hasta 2021


df = pd.read_csv('csv/torneos_oficiales.csv')
goles = pd.read_csv('csv/goles.csv')

df.drop(['Unnamed: 0'], axis=1, inplace=True)
df.drop(['Neutral'], axis=1, inplace=True)
goles.drop(['Unnamed: 0'], axis=1, inplace=True)

inner = pd.merge(df, goles, on=['Fecha', 'Local', 'Visitante'], how='left')

#Segmentamos el dataframe para obtener los goles de la seleccion argentina en la copa america
cp_argentina = inner[(inner['Torneo'] == 'Copa América')
                    & (inner['Equipo'] == 'Argentina')]

#Funcion para contar los goles
def cantidadGolesMin(lista_minutos, columnaMinutos_df):
    goles_porMin = {

    }

    for gol1 in lista_minutos:
        cont = 0
        for i in range(len(columnaMinutos_df)):
            if gol1 == columnaMinutos_df.iloc[i]:
                cont += 1
            goles_porMin[gol1] = cont

    return goles_porMin

#Funcion para convertir un diccionario en dataframe
def DictToDF(dict1):

    dataframe = pd.DataFrame([[minuto, dict1[minuto]]
                            for minuto in dict1.keys()], columns=['Minuto', 'Goles'])

    return dataframe


g = cantidadGolesMin(
    list(cp_argentina['Minuto'].unique()), cp_argentina['Minuto'])
goles_cp_argentina = DictToDF(g)

goles_cp_argentina = goles_cp_argentina[goles_cp_argentina['Minuto'] <= 90]

goles_cp_argentina = goles_cp_argentina.sort_values(
    'Minuto').reset_index(drop=True)

#Obtenemos el promedio de los goles por minuto
total_goles = goles_cp_argentina['Goles'].sum()
g = goles_cp_argentina['Goles']

promedio_golesMinuto = [ x/total_goles for x in g]

#Agregamos esta nueva informacion al dataframe
goles_cp_argentina['Promedio_GolesMinuto'] = promedio_golesMinuto


#---------------------------
#Modelo de regresion
#y = variable dependiente -> Goles
#x = variable independiente -> Minutos

m = goles_cp_argentina.iloc[:, 0] #Tiene almacenado los minutos
g = goles_cp_argentina.iloc[:, 2] #Almacena los promedios de gol por minuto

pruebaCorrelacion = pearsonr(m, g) 

print("Coeficiente de correlacion de Pearson: ", pruebaCorrelacion[0])
print("p-value: ", pruebaCorrelacion[1])

X = goles_cp_argentina['Minuto'].values.reshape((-1, 1))
y = goles_cp_argentina['Promedio_GolesMinuto']

X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=0.2) #Escogemos el 80 por ciento de los datos para entrenamiento

regresion = linear_model.LinearRegression()

modelo = regresion.fit(X_train, y_train)

Y_predict = modelo.predict(X_test)

w = modelo.coef_
b = modelo.intercept_

print(f"Recta: {w}*x + {b}")

print('Precision del modelo: ', modelo.score(X_train, y_train))

plt.tight_layout()
plt.title('Relacion entre el promedio de goles y los minutos de la seleccion argentina en la copa américa desde 1916 a 2021')
plt.scatter(x="Minuto", y="Promedio_GolesMinuto",
            data=goles_cp_argentina, color='blue')  # Datos del dataset
plt.scatter(X_test, y_test, color = 'red')  # Valores utilizados para probar el modelo 
plt.plot(X_test, Y_predict, color = 'black')  # Graficamos la recta de regresión 
plt.ylabel('Promedio de Goles')
plt.xlabel('Minuto')
plt.gcf().set_size_inches(18, 10)
plt.savefig("regresion_lineal/grafica_regresion.png")
