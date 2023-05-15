#Practica 4

#Se tienen los datos de los goles anotados por la seleccion de brasil durante los primeros 45min de partido desde 1930 hasta 2022.
#Verificar si los datos siguen una distribucion normal utilizando la prueba de la chi cuadrada con un alpha de 0.05

#----------------------- Hipotesis -------------------
#H_0: Los datos de los 94 goles anotados por la seleccion de brasil durante los primeros 45 minutos siguen una distribucion normal
#H_1: Los datos de los 94 goles anotados por la seleccion de brasil durante los primeros 45 minutos no siguen una distribucion normal


"""
Columnas dataframe df 
Fecha: Fecha en la que se jugo el partido - tipo -> Datetime
Local: Nombre de la seleccion que jugó como local - tipo -> string
Visitante: Nombre de la seleccion que jugó de visitante - tipo -> string
Goles_Local: Goles anotados por la seleccion local - tipo -> int
Goles_Visitante: Goles anotados por la seleccion visitante - tipo -> int
Torneo: Torneo disputado - tipo -> string
Ciudad: Ciudad donde se jugó el partido - tipo -> string

-------------------
Columnas dataframe goles
Fecha: Fecha en la que se jugó el partido - tipo -> Datetime
Local: Nombre de la seleccion que jugó como local - tipo -> string
Visitante: Nombre de la seleccoin que jugó como visitante - tipo -> string
Equipo: Seleccion del jugador que anotó el gol - tipo -> string
Anotador: Nombre del jugador que anotó el gol - tipo -> string
Minuto: Minuto en el fue anotado el gol - tipo -> float
Autogol: Si el gol anotado se marcó como en propia puerta - tipo -> bool
Penal: Si el gol anotado se marcó como penal - tipo -> bool

"""
import pandas as pd

df = pd.read_csv('csv/torneos_oficiales.csv')
goles = pd.read_csv('csv/goles.csv')

df.drop(['Unnamed: 0'], axis=1, inplace=True)
df.drop(['Neutral'], axis=1, inplace=True)
goles.drop(['Unnamed: 0'], axis=1, inplace=True)

inner = pd.merge(df, goles, on=['Fecha', 'Local', 'Visitante'], how='left')

#Segmentamos nuestro dataframe para que solo nos muestre los partidos de brasil en los mundiales
mundialbr = inner[(inner['Torneo'] == 'FIFA World Cup')
                    & (inner['Equipo'] == 'Brazil')]

mbr_L = mundialbr[mundialbr['Local'] == 'Brazil'] #Dataframe con los partidos que jugó brasil como local
mbr_V = mundialbr[mundialbr['Visitante'] == 'Brazil'] #Dataframe con los partidos que jugó como visitante

#Funcion para contar los goles de local
def cantidadGolesMinL(lista_minutosL, columnaMinutosL_df):
    #Recibe
    # columnaMinutosL_df -> Columna del dataframe que contiene los minutos en los que anotaron gol de local
    # lista_minutosL-> lista con los valores únicos de la columna minuto

    goles_porMinL = {

    }

    for gol1 in lista_minutosL:
        cont = 0
        for i in range(len(columnaMinutosL_df)):
            if gol1 == columnaMinutosL_df.iloc[i]:
                cont += 1
            goles_porMinL[gol1] = cont

    return goles_porMinL

#Funcion para contar los goles de Vistitante
def cantidadGolesMinV(lista_minutosV, columnaMinutosV_df):
    #Recibe
    # columnaMinutosL_df -> Columna del dataframe que contiene los minutos en los que anotaron gol de visitante
    # lista_minutosL-> lista con los valores únicos de la columna minuto

    goles_porMinV = {

    }

    for gol2 in lista_minutosV:
        cont = 0
        for i in range(len(columnaMinutosV_df)):
            if gol2 == columnaMinutosV_df.iloc[i]:
                cont += 1
            goles_porMinV[gol2] = cont

    return goles_porMinV

#Funcion para sumar los elementos de dos diccionarios, regresa un dataframe con los datos
def sumaDict(dict1, dict2):
    from collections import Counter

    dict_res = Counter(dict1) + Counter(dict2)

    dataframe = pd.DataFrame([[jugador, dict_res[jugador]]
                            for jugador in dict_res.keys()], columns=['Minuto', 'Goles'])

    return dataframe

x = cantidadGolesMinL(lista_minutosL=list(
    mbr_L['Minuto'].unique()), columnaMinutosL_df=mbr_L['Minuto'])
y = cantidadGolesMinL(lista_minutosL=list(
    mbr_V['Minuto'].unique()), columnaMinutosL_df=mbr_V['Minuto'])

mundialbr_df = sumaDict(x, y)

#Guardamos en otro dataframe los goles anotados hasta el min 45
mundialbr_df1 = mundialbr_df[mundialbr_df['Minuto'] <= 45]
mundialbr_df1 = mundialbr_df1.sort_values('Minuto')
mundialbr_df1 = mundialbr_df1.reset_index(drop=True)

#Se reunió la informacion del dataframe anterior en una tabla de frecuancias
br_golesMinuto = pd.DataFrame({
    'Lim_inf': [1.0, 7.0, 14.0, 20.0, 26.0, 32.0, 39.0],
    'Lim_sup': [7.0, 14.0, 20.0, 26.0, 32.0, 39.0, 45.0],
    'Frecuencia Observada': [6, 16, 16, 8, 13, 17, 18]
})

#---------------------------------------
#Realizando la prueba estadística

from statistics import mean, stdev

#Calculamos la media muestral y desviacion estandar muestral
est_mu = mean(list(br_golesMinuto['Frecuencia Observada']))
est_sigma = stdev(list(br_golesMinuto['Frecuencia Observada']))

#Calculando la probabilidad de cada intervalo
from scipy.stats import norm, chi2, chisquare

prob_normal = [norm.cdf(br_golesMinuto.iloc[m+1, 1], est_mu, est_sigma) - norm.cdf(br_golesMinuto.iloc[m+1, 0], est_mu, est_sigma) for m in range(5)]
prob_normal.insert(0, norm.cdf(br_golesMinuto.iloc[0,1], est_mu, est_sigma)) #Probabilidad del primer intervalo
prob_normal.append(1-norm.cdf(br_golesMinuto.iloc[6, 0], est_mu, est_sigma)) #Probabilidad del ultimo invervalo

#Verificando que la suma sea igual a 1
print("Suma probabilidades intervalo: ", sum(prob_normal))

#Calculando la frecuencia esperada 
n = sum(br_golesMinuto['Frecuencia Observada'])

freq_esperada = [n*p_n for p_n in prob_normal]
#Verificandoque la frecuencia esperada sea igual al numero de datos que tenemos
print("Suma Frecuencias esperadas: ",sum(freq_esperada))

#Agregamos esta nueva informacion al dataframe
br_golesMinuto['Probabilidad'] = prob_normal
br_golesMinuto['Frecuencia Esperada'] = freq_esperada

print(br_golesMinuto)

#Para poder utilizar este método todas las frecuencias esperadas tienen que ser mayores a 5, como las últimas no lo cumplen sumaremos esas columnas 
# Eliminamos las columnas Limite inferior y Limite superior para más comodida al manipular el dataframe
br_golesMinuto.drop(columns=['Lim_inf', 'Lim_sup'], inplace=True)

suma_freqEsperada = [
    br_golesMinuto.iloc[0],
    br_golesMinuto.iloc[1],
    br_golesMinuto.iloc[2],
    br_golesMinuto.iloc[3:7].sum()  # Sumamos los ultimos datos 
]

#Obtenemos el nuevo intervalo
nuevo_intervalo = ['1.0 - 7.0', '7.0 - 14.0', '14.0 - 20.0', '20.0 - 45.0']

#Lo agregamos al dataframe
br_golesMinuto1 = pd.DataFrame(suma_freqEsperada)  # Hacemos un nuevo dataframe
br_golesMinuto1.insert(0, 'Intervalo', nuevo_intervalo)
br_golesMinuto1.rename(index = {'Unnamed 0':3}, inplace = True) #Renombramos los indices

print("------------------------------------------------")
print("\n",br_golesMinuto1)

# Obtenemos la lista con los valores de la frecuencia observada
freq_obs = br_golesMinuto1['Frecuencia Observada']
# Obtenemos la lista con los valores de la frecuencia esperada
freq_esp = br_golesMinuto1['Frecuencia Esperada']

print("------------------")
#Obteniendo el estadístico de prueba
ep = chisquare(f_obs=freq_obs,
            f_exp=freq_esp)[0]

#Para calcular el valor de tabla se utilizan los siguientes datos
#num de intervalos = 4, num de parametros estimados = 2
chi = chi2.isf(0.05,
                4-2-1)

if(ep > chi): 
    print("Se rechaza la hipótesis nula: Los datos no siguen una distribucion normal")
else: 
    print("No se rechaza la hipótesis nula: Los datos siguen una distribucion normal")