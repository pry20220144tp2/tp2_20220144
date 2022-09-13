import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

import caracteristicas_extraidas
import urls_analizados


def getResult(url):

    # load the model from disk
    model = pickle.load(open('rfc_model', 'rb'))

    # Searching for the input url in URL file
    x_input = url
    status = urls_analizados.url_search(x_input)
    l = []

    if (status == 'NOT FOUND'):

        x_new = []
        x_new = caracteristicas_extraidas.generate_data_set(x_input)
        l.append(x_new[0])
        x_new[0] = np.array(x_new[0]).reshape(1, -1)

        try:

            prediction = model.predict(x_new[0])
            print("La predicción es", prediction)
            if prediction == -1:
                res = "es un URL sospechoso de phishing"

            else:
                res = "es URL seguro/legítimo"

        except:
            print("¡Ocurrió una excepción!")
            res = "es un URL sospechoso de phishing"

        print("La predicción del URL es : ", res)
        #print("Time taken to generate dataset : ",(x_new[1])," seconds")

        # Add the url into the csv file if it is not already present
        urls_analizados.url_update(x_input, res, l[0])
        l.append(res)

    else:
        print("Las características extraídas del URL son : ", status[1])
        print("El estado del URL en la base de datos es : ", status[0])
        print("Tiempo transcurrido para encontrar el estado del URL en la base de datos : ",
              status[2], " segundos")

        # print(status)
        li = [int(i.strip('[]')) for i in status[1].split(',')]
        l.append(li)
        l.append(status[0])

    return l
