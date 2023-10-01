import openai
import pandas as pd

import config


def categorize_keywords():

    # Leemos el archivo CSV que subimos al entorno de Colab, tienen que estar todas las keys en una columna con la cabecera "keywords"
    df = pd.read_csv('docs/keywords.csv')

    # RELLENAR: Añade aquí tu API de OpenAI
    openai.api_key = config.API_KEY

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
        # Get a batch of 100 keywords from the DataFrame
        lote = df['keywords'][indice_lote : indice_lote + 100]

        # Convert the batch of keywords to a string
        lote_string = '\n'.join(lote)

        # Create a prompt for the OpenAI API
        prompt = f'Para el siguiente listado de sentencias : \n\n {lote_string} \n \n devuelve por cada una la intención de \
                búsqueda (Conversacional, Consulta o Generacional) y la etapa del embudo de conversión (Descubrimiento ,\
                Consideración  o Conversión ). Habrá una palabra por línea con el formato: Keyword | Intención | Etapa'

        # Call the OpenAI API to categorize the keywords
        categorizacion = openai.Completion.create(
            model='text-davinci-003',
            prompt=prompt,
            max_tokens=1500,
            temperature=0.7,
        )

        # Process the categorized keywords
        keywords_categorizadas = categorizacion.choices[0].text.split('\n')

        # Iterate over each element in the list
        for elemento in keywords_categorizadas:
            # Split the string into substrings using the delimiter '|'
            subcadenas = elemento.split('|')
            # Assign each substring to a temporary variable if there are three substrings
            if len(subcadenas) == 3:
                keyword, intencion_temp, etapa_temp = subcadenas
            # Assign the available substrings to temporary variables and leave the remaining variables empty
            else:
                keyword = subcadenas[0] if len(subcadenas) > 0 else ''
                intencion_temp = subcadenas[1] if len(subcadenas) > 1 else ''
                etapa_temp = subcadenas[2] if len(subcadenas) > 2 else ''
            # Añade cada subcadena a la lista correspondiente
            keywords.append(keyword)
            intencion.append(intencion_temp)
            etapa.append(etapa_temp)

        # Update the counters
        contador_keywords += len(lote)
        indice_lote += 100
    return keywords, intencion, etapa


keywords, intencion, etapa = categorize_keywords()

# Crea un DataFrame de Pandas a partir de las tres listas
tabla = pd.DataFrame(
    {'Keywords': keywords, 'Intencion': intencion, 'Etapa': etapa}
)


tabla.to_csv('docs/results.csv')
