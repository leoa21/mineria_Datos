import random
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('csv/torneos_oficiales.csv')
goles = pd.read_csv('csv/goles.csv')

df.drop(['Unnamed: 0'], axis=1, inplace=True)
df.drop(['Neutral'], axis=1, inplace=True)
goles.drop(['Unnamed: 0'], axis=1, inplace=True)

goles_df = goles.drop(['Fecha', 'Local', 'Visitante',
                        'Anotador', 'Minuto', 'Autogol', 'Penal'], axis=1)
goles_df.columns = ['Equipo']
goles_df = goles_df.head(30000)


textoGoles = ""


def Escribir_goles(renglon):
    global textoGoles
    textoGoles += str(renglon+" ")


goles_df['Equipo'].apply(Escribir_goles)

archivo = open('nube_texto/goles.txt', mode='w')
archivo.write(textoGoles)
archivo.close()

#Generamo la nube

archivo = open('nube_texto/goles.txt', mode='r')
textoGoles = archivo.read()
archivo.close()


#Función para transformar todas las imágenes PNG con fondo transparente a fondo blanco

def transform_white_backgroud(png_path):
    picture = Image.open(png_path).convert("RGBA")
    image = Image.new("RGB", picture.size, "WHITE")
    image.paste(picture, (0, 0), picture)

    #plt.imshow(image)

    mask = np.array(image)

    return mask


#Grafica con la silueta de Cristiano Ronaldo
mascaraCR7 = transform_white_backgroud('nube_texto/CR7.png')

"""
wordCloud = WordCloud(mask=mascaraCR7, background_color='white', contour_width=1, contour_color='grey',
                        max_words=25000, min_font_size=5, collocation_threshold=10).generate(textoGoles)
#plt.figure(figsize=(10, 8))
plt.imshow(wordCloud)
plt.axis('off')
plt.tight_layout(pad=0)

wordCloud.to_file("nube_texto/graficas/CR7.png")
"""

#Grafica normal
word_cloud = WordCloud(background_color='white',
                        max_words=300, min_font_size=5, collocation_threshold=10).generate(textoGoles)
plt.imshow(word_cloud)
plt.axis('off')
plt.tight_layout(pad=0)
word_cloud.to_file("nube_texto/graficas/word_cloud.png")
#plt.show()

