import openai
import re
import base64
import requests
import json
import pandas as pd

# Leemos el archivo CSV que subimos al entorno de Colab, tienen que estar todas las keys en una columna con la cabecera "keywords"
df = pd.read_csv('docs/keywords.csv')

# RELLENAR: Añade aquí tu API de LlamaAI
openai.api_key = "COLOCA-Tu-API-AQUI"


# Crea un contador de keywords procesadas y un índice de lote inicial
contador_keywords = 0
indice_lote = 0

# Calcular el numero total de keywords
num_keywords = len(df['keywords'])

# Crea las listas vacías para cada columna de la tabla
keywords = []
intencion = []
etapa = []

# Mientras el contador sea menor al número total de keywords en el archivo CSV
while contador_keywords < num_keywords:
    # Obtener el lote de 100 keywords
    lote = df['keywords'][indice_lote:indice_lote+100]
    
    # Convertimos el lote de keywords a una cadena de texto
    lote_string = '\n'.join(lote)
    
    prompt = f"Para el siguiente listado de sentencias : \n\n {lote_string} \n \n devuelve por cada una la intención de búsqueda (Conversacional, Consulta o Generacional) y la etapa del embudo de conversión (Descubrimiento , Consideración  o Conversión ). Habrá una palabra por línea con el formato: Keyword | Intención | Etapa"

#    Llamamos a OpenAI para que atribuya las intenciones y etapas de las keys
    categorizacion = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=1500,
        temperature=0.7,
    )   
   
    # Procesar las keywords categorizadas
    keywords_categorizadas = categorizacion.choices[0].text.split('\n')

    # Itera sobre cada elemento de la lista
    for elemento in keywords_categorizadas:
        # Divide la cadena en subcadenas utilizando el delimitador '|'
        subcadenas = elemento.split('|')
        # Si hay tres subcadenas, asigna cada subcadena a una variable temporal
        if len(subcadenas) == 3:
            keyword, intencion_temp, etapa_temp = subcadenas
        # Si no hay tres subcadenas, asigna las subcadenas disponibles a las variables temporales
        # y deja las variables restantes vacías
        else:
            keyword = subcadenas[0] if len(subcadenas) > 0 else ''
            intencion_temp = subcadenas[1] if len(subcadenas) > 1 else ''
            etapa_temp = subcadenas[2] if len(subcadenas) > 2 else ''
        # Añade cada subcadena a la lista correspondiente
        keywords.append(keyword)
        intencion.append(intencion_temp)
        etapa.append(etapa_temp)

    # Aumenta el contador de keywords procesadas y el índice de lote
    contador_keywords += len(lote)
    indice_lote += 100

# Crea un DataFrame de Pandas a partir de las tres listas
tabla = pd.DataFrame({'Keywords': keywords, 'Intencion': intencion, 'Etapa': etapa})


tabla.to_csv('docs/results.csv')
