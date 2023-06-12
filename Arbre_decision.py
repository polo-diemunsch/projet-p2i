import SQL.commandes_bd as cbd
import pandas as pd  # library to work with dataframes
from sklearn.model_selection import train_test_split  # découpage de jeu de données en train et test
from sklearn.preprocessing import MinMaxScaler  # min-max scaler
from sklearn import tree  # decision trees
from sklearn import metrics  # evaluation metrics
from sklearn.neighbors import KNeighborsClassifier  # knn
import matplotlib.pyplot as plt  # Visualization library
import operator

# Code permettant de recréer le fichier csv si on veut le modifier

connexion_bd = cbd.ouvrir_connexion_bd()
cbd.create_CSV_train_data(connexion_bd)

# RECUPERATION DES DONNEES

# Import des données
train_data = pd.read_csv('train_data.csv', sep=";")  # jeu de donnés d'entrainement

# Informations générales sur le jeu de données
print("*" * 40)
print(f"Informations générales sur le jeu de donnée train_data :")
print("*" * 40 + "\n")

# affichage du nombre de lignes et de colonnes
print("Taille du jeu de données d'entrainement:")
print(f"Nombre de lignes: {train_data.shape[0]:,}\nNombre de colonnes: {train_data.shape[1]:,}\n")

print("Résumé du dataset :\n")
train_data.info()
print("")

pd.set_option("max_columns", None) # show all cols
# 5 premières lignes du jeu d'entrainement
print(f"Affichage des 5 premières ligne : \n{train_data.head(5)}\n")

# stats de résumé
# print(train_data.describe())

# NETTOYAGE
print("*" * 40)
print("Nettoyage du jeu de donnée")
print("*" * 40 + "\n")

# PRESENCE DE DOUBLONS
print("-" * 10 + "Nettoyage des doublons" + "-" * 10 + "\n")

nb_doublon = train_data.duplicated().sum()  # nombre de doublons
if nb_doublon == 0:
    print("Absence de doublon...\n")
else:
    # supprimer les doublons en modifiant le jeu de données en question
    print(f"{nb_doublon} doublons détectés...")
    train_data.drop_duplicates(keep='first', inplace=True, ignore_index=False)
    print("Doublons supprimés...\n")

# VALEURS MANQUANTES
print("-" * 10 + "Détection de valeurs manquantes" + "-" * 10 + "\n")

# affichage du nombre de valeurs manquantes par colonne
print("Nombre de valeurs manquantes par colonne :")
val_manquantes_par_colonnes = train_data.isna().sum()
print(val_manquantes_par_colonnes)
# affichage du nombre total de valeurs manquantes
nombre_valeur_manquante = train_data.isna().sum().sum()
liste_colonnes_avec_valeurs_manquantes = []
if nombre_valeur_manquante > 0:
    print(f"\n{nombre_valeur_manquante} valeurs manquantes détectées\n")
    print("Suppression des colonnes présentant des valeurs manquantes...\n")
    for i in range(0, len(val_manquantes_par_colonnes)):
        if val_manquantes_par_colonnes[i] > 0:
            liste_colonnes_avec_valeurs_manquantes.append(train_data.columns[i])
    print("Colonnes présentant des valeurs manquantes supprimées\n")

else:
    print("\nPas de valeurs maquantes\n")

# ANALYSE PREDICTIVE
print("*" * 40)
print("Préparation du jeu de donnée pour l'analyse prédictive")
print("*" * 40 + "\n")

print("Séparation de la donnée cible du jeu de donnée...\n")

all_x = train_data.loc[:, ~train_data.columns.isin(liste_colonnes_avec_valeurs_manquantes + ['Perf_niveauEstime'])].copy()

all_y = train_data['Perf_niveauEstime'].copy()  # Cible

print("Création d'un jeu d'entrainement et d'un jeu de test...\n")

X_train, X_test, y_train, y_test = train_test_split(all_x, all_y, test_size=0.2, random_state=42, stratify=all_y)
print(f"X_train et y_train de même taille : {X_train.shape[0] == y_train.shape[0]}")
print(f"X_test et y_test de même taille: {X_test.shape[0] == y_test.shape[0]}")
print(f"Le rapport jeu de donné de test est de {X_test.shape[0] / train_data.shape[0]}% par rapport au jeu initial\n")

# NORMALISATION DES DONNEES
print("Normalisation des données...\n")
scaler = MinMaxScaler()  # create a scaler object
# Fit (calculer le min et max pour le futur scaling) aux données et transformer les données
X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
# transformer les données
X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=X_train.columns)
print("Données normalisées")


# MODELISATION
# ARBRE DE DECISION
print("*" * 40)
print("Création de l'arbre de décision")
print("*" * 40 + "\n")

# Création
print("Création de l'arbre...")
# create a model
clf_tree = tree.DecisionTreeClassifier()
# fit the model
clf_tree.fit(X_train_scaled.values, y_train.values)

plt.figure()
plt.figure(figsize=(10,10))
tree.plot_tree(clf_tree, filled = True, fontsize=6, max_depth=3)
plt.show()

# Entrainement
print("Entrainement de l'arbre...\n")
y_pred_tree = clf_tree.predict(X_test_scaled.values)

# Evaluation
print("Résumé d'évaluation de l'arbre : ")
print(metrics.classification_report(y_test, y_pred_tree))

# matrice de confusion
conf_m = metrics.confusion_matrix(y_test, y_pred_tree)
# display
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix=conf_m,
                                           display_labels=["Jamais touché de piano", "Débutant", "Intermédiaire", "Confirmé", "Expert"])
fig, ax = plt.subplots(figsize=(8,8))
ax.grid(False)
cm_display.plot(ax=ax)
plt.show()

"""
# KNN
print("*" * 40)
print("Création du modèle KNN")
print("*" * 40 + "\n")

print("Création du modèle...")
# create model
knn = KNeighborsClassifier(n_neighbors=8)
# fit to train Data (train the model)
knn.fit(X_train_scaled, y_train)

# Entrainement
print("Entrainement du modèle...\n")
y_pred = knn.predict(X_test_scaled)

# Evaluation
# Accuracy
print(f"La précision de KNN : {metrics.accuracy_score(y_test, y_pred)}")
# matrice de confusion
conf_m = metrics.confusion_matrix(y_test, y_pred)
print("Résumé d'évaluation de l'arbre : ")
print(metrics.classification_report(y_test, y_pred))
"""

perf_to_analyse = cbd.get_perf_to_analyse(connexion_bd, 111)
perf_to_analyse = pd.DataFrame(perf_to_analyse)

scaler = MinMaxScaler()  # create a scaler object
scaler.fit(X_train.values)
perf_to_analyse = pd.DataFrame(scaler.transform(perf_to_analyse))

predicted = clf_tree.predict(perf_to_analyse)
jtdp_count = 0
intermediaire_count = 0
debutant_count = 0
confirme_count = 0
expert_count = 0

dico_results = {}

for result in predicted:
    if result in dico_results.keys():
        dico_results[result] += 1
    else:
        dico_results[result] = 1

print(dico_results)
print(f"Niveau estimé : {max(dico_results.items(), key=operator.itemgetter(1))[0]}")

cbd.fermer_connexion_bd(connexion_bd)
