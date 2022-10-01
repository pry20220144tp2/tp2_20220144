import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix

import matplotlib.pyplot as plt

from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import roc_curve, auc, roc_auc_score

data = pd.read_csv('dataset_phishing.csv')

data

data = data.drop('id', 1)

data

y = data['Result']
x = data.drop('Result', axis=1)

# print(x.shape)
# print(x.isnull().sum())

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.25, random_state=42, stratify=y)

# Tuning
# n_estimators: Número de árboles
# max_features: Cantidad de variables a considerar al buscar el mejor split
# max_depth: Profundidad del árbol

param_grid = {
    'n_estimators': [200, 700],
    'max_features': ['auto', 'sqrt', 'log2'],
    'max_depth': [2, 3, 4, 5, 6, 7, 8, 9, 10]
}

grid = GridSearchCV(RandomForestClassifier(), param_grid,
                    refit=True, verbose=2, cv=5)
grid.fit(x_train, y_train)

print(grid.best_estimator_)

# Random Forest
classifier = RandomForestClassifier(
    max_depth=10, max_features='sqrt', n_estimators=200).fit(x_train, y_train)

y_pred = classifier.predict(x_test)

confusion_matrix(y_test, y_pred)

# Graficando la matriz de confusión
titles_options = [("Confusion matrix, without normalization", None),
                  ("Normalized confusion matrix", 'true')]
for title, normalize in titles_options:
    disp = plot_confusion_matrix(classifier, x_test, y_test,
                                 # display_labels=y_test,
                                 cmap=plt.cm.Blues,
                                 normalize=normalize)
    disp.ax_.set_title(title)

    print(title)
    print(disp.confusion_matrix)

plt.show()

y_pred_prob = classifier.predict_proba(x_test)

false_positive_rate, true_positive_rate, thresholds = roc_curve(
    y_test, y_pred_prob[:, 1])

roc_auc = auc(false_positive_rate, true_positive_rate)
roc_auc

plt.title('Receiver Operating Characteristic')
plt.plot(false_positive_rate, true_positive_rate,
         color='red', label='AUC = %0.4f' % roc_auc)
plt.legend(loc='lower right')
plt.plot([0, 1], [0, 1], linestyle='--')
plt.axis('tight')
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()

# Reporte de clasificación
print(classification_report(y_test, y_pred))

pickle.dump(classifier, open('rfc_model', 'wb'))
