import SQL.commandes_bd as cbd
import pandas as pd # library to work with dataframes
from sklearn.model_selection import train_test_split # découpage de jeu de données en train et test
from sklearn.preprocessing import MinMaxScaler # min-max scaler
from sklearn import tree # decision trees
from sklearn import metrics # evaluation metrics
from sklearn.neighbors import KNeighborsClassifier # knn
import matplotlib.pyplot as plt # Visialization library


#Code permettant de recréer les fichier csv si on veut les modifier
"""
connexion_bd = cbd.ouvrir_connexion_bd()
cbd.create_CSV_train_data(connexion_bd)
cbd.create_CSV_test_data(connexion_bd)
cbd.fermer_connexion_bd(connexion_bd)
"""

#RECUPERATION DES DONNEES

# Import des données
train_data = pd.read_csv('train_data.csv', sep = ";") # jeu de donnés d'entrainement

#Informations générales sur le jeu de données
print("*"*40)
print(f"Informations générales sur le jeu de donnée train_data :")
print("*"*40 + "\n")

# affichage du nombre de lignes et de colonnes
print("Taille du jeu de données d'entrainement:")
print(f"Nombre de lignes: {train_data.shape[0]:,}\nNombre de colonnes: {train_data.shape[1]:,}\n")

print("Résumé du dataset :\n")
train_data.info()
print("")

# 5 premières lignes du jeu d'entrainement
print(f"Affichage des 5 premières ligne : \n{train_data.head(5)}\n")

# stats de résumé
#print(train_data.describe())

#NETTOYAGE
print("*"*40)
print("Nettoyage du jeu de donnée")
print("*"*40 + "\n")

#PRESENCE DE DOUBLONS
print("-"*10 + "Nettoyage des doublons" + "-"*10 + "\n")

nb_doublon = train_data.duplicated().sum()              # nombre de doublons
if nb_doublon == 0:
    print("Abscence de doublon...\n")
else:
#supprimer les doublons en modifiant le jeu de données en question
    print(f"{nb_doublon} doublons détectés...")
    train_data.drop_duplicates(keep='first', inplace=True, ignore_index=False)
    print("Doublons supprimés...\n")

#VALEURS MANQUANTES
print("-"*10 + "Détection de valeurs manquantes" + "-"*10 + "\n")

# affichage du nombre de valeurs manquantes par colonne
print("Nombre de valeurs manquantes par colonne :")
val_manquantes_par_colonnes = train_data.isna().sum()
print(val_manquantes_par_colonnes)
# affichage du nombre total de valeurs manquantes
nombre_valeur_manquante = train_data.isna().sum().sum()
if nombre_valeur_manquante > 0:
    print(f"\n{nombre_valeur_manquante} valeurs manquantes détectées\n")
    print("Suppression des colonnes présentant des valeurs manquantes...\n")
    liste_colonnes_avec_valeurs_manquantes = []
    for i in range(0, len(val_manquantes_par_colonnes)):
        if val_manquantes_par_colonnes[i] > 0:
            liste_colonnes_avec_valeurs_manquantes.append(train_data.columns[i])
    print("Colonnes présentant des valeurs manquantes supprimées\n")

#ANALYSE PREDICTIVE
print("*"*40)
print("Préparation du jeu de donnée pour l'analyse prédictive")
print("*"*40 + "\n")

print("Séparation de la donnée cible du jeu de donnée...")
all_x = train_data.loc[:, ~train_data.columns.isin(liste_colonnes_avec_valeurs_manquantes + ['Mu_niveau'])].copy()
all_y = train_data['Mu_niveau'].copy() #Cible

print("Création d'un jeu d'entrainement et d'un jeu de test...\n")
X_train, X_test, y_train, y_test = train_test_split(all_x, all_y, test_size=0.2, random_state=42, stratify=all_y)
print(f"La taille de X_train et y_train est la même : {X_train.shape[0] == y_train.shape[0]}")
print(f"La taille de X_test et y_test est la même : {X_test.shape[0] == y_test.shape[0]}")
print(f"Le rapport jeu de donné de test est de {X_test.shape[0] / train_data.shape[0]}% par rapport au jeu initial\n")

#NORMALISATION DES DONNEES
print("Normalisation des données...\n")
scaler = MinMaxScaler() # create a scaler object
# Fit (calculer le min et max pour le futur scaling) aux données et transformer les données
X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
# transformer les données
X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=X_train.columns)

#MODELISATION
#ARBRE DE DECISION
print("*"*40)
print("Création de l'arbre de décision")
print("*"*40 + "\n")

#Création
print("Création de l'arbre...")
# create a model
clf_tree = tree.DecisionTreeClassifier()
# fit the model
clf_tree.fit(X_train_scaled, y_train)

# Entrainement
print("Entrainement de l'arbre...\n")
y_pred_tree = clf_tree.predict(X_test_scaled)

#Evaluation
print("Résumé d'évaluation de l'arbre : ")
print(metrics.classification_report(y_test, y_pred_tree))

#KNN
print("*"*40)
print("Création du modèle KNN")
print("*"*40 + "\n")

print("Création du modèle...")
# create model
knn = KNeighborsClassifier(n_neighbors=8)
# fit to train data (train the model)
knn.fit(X_train_scaled, y_train)

#Entrainement
print("Entrainement du modèle...\n")
y_pred = knn.predict(X_test_scaled)

#Evaluation
#Accuracy
print(f"La précision de KNN : {metrics.accuracy_score(y_test, y_pred)}")
# matrice de confusion
conf_m = metrics.confusion_matrix(y_test, y_pred)
print("Résumé d'évaluation de l'arbre : ")
print(metrics.classification_report(y_test, y_pred))
