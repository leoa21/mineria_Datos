#Analizaremos los partidos de brazil en los mundiales

from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv('csv/torneos_oficiales.csv')
goles = pd.read_csv('csv/goles.csv')

df.drop(['Unnamed: 0'], axis=1, inplace=True)
df.drop(['Neutral'], axis=1, inplace=True)
goles.drop(['Unnamed: 0'], axis=1, inplace=True)

brazil_df_l = df[df['Local'] == 'Brazil']

brazil_df_l = brazil_df_l.drop(
    ['Local', 'Visitante', 'Goles_Visitantes', 'Torneo', 'Ciudad', 'Pais'], axis=1)

brazil_df_v = df[df['Visitante'] == 'Brazil']
brazil_df_v = brazil_df_v.drop(
    ['Local', 'Visitante', 'Goles_Local', 'Torneo', 'Ciudad', 'Pais'], axis=1)


brazil_df_v.columns = ['Fecha', 'Goles']
brazil_df_l.columns = ['Fecha', 'Goles']

brazil_df = pd.concat([brazil_df_l, brazil_df_v], ignore_index=True)


#brazil_df.Fecha = pd.to_datetime(brazil_df.Fecha)


#j = brazil_df.iloc[0, 0]

def partidosFecha(fecha):
    fechaTexto = str(fecha)
    return str(fechaTexto[0])+str(fechaTexto[1])+str(fechaTexto[2])+str(fechaTexto[3])


brazil_df["Año"] = brazil_df["Fecha"].apply(partidosFecha)

df2 = brazil_df.groupby(['Año']).sum()

df2 = df2.reset_index()

df2 = df2[df2['Año'] >= '1940'].reset_index(drop=True)

#df2 = df2.set_index('Año')

df2 = df2.astype(int)

f_27 = df2[df2['Año'] <= 1969].astype(int)

l_27 = df2[df2['Año'] >= 1996].astype(int)


regresionTodos = LinearRegression()
regresion_f27 = LinearRegression()
regresion_l27 = LinearRegression()


X_todos = df2['Año'].values.reshape((-1, 1))
X_f27 = f_27['Año'].values.reshape((-1, 1))
X_l27 = l_27['Año'].values.reshape((-1, 1))

regresionTodos.fit(X_todos, df2['Goles'])
regresion_f27.fit(X_f27, f_27['Goles'])
regresion_l27.fit(X_l27, l_27['Goles'])


def linea(x, w, b): return w*x + b


print(
    f"Recta Regresion Todos: {regresionTodos.coef_}*x + {regresionTodos.intercept_}")
print(
    f"Recta Regresion Primeros 27 Partidos: {regresion_f27.coef_}*x + {regresion_f27.intercept_}")
print(
    f"Recta Regresion Ultimos 27 Partidos: {regresion_l27.coef_}*x + {regresion_l27.intercept_}")


#plt.figure(figsize=(15, 8))
plt.plot(X_todos, [linea(x, regresionTodos.coef_,
            regresionTodos.intercept_) for x in list(df2['Año'])])
plt.plot(X_f27, [linea(x, regresion_f27.coef_, regresion_f27.intercept_)
            for x in list(f_27['Año'])])
plt.plot(X_l27, [linea(x, regresion_l27.coef_, regresion_l27.intercept_)
            for x in list(l_27['Año'])])
plt.scatter(df2['Año'], df2['Goles'])
plt.ylabel('Cantidad de goles')
plt.xlabel('Año')
plt.xticks(rotation=90)

plt.savefig("forecasting/forecasting.png")

#plt.show()
