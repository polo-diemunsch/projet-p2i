import SQL.commandes_bd as cbd


connexion_bd = cbd.ouvrir_connexion_bd()
cbd.create_CSV_train_data(connexion_bd)
cbd.create_CSV_test_data(connexion_bd)
cbd.fermer_connexion_bd(connexion_bd)

cbd.lire_fichier_csv("train_data.csv")

import pandas as pd # library to work with dataframes
import numpy as np # numeric calculations


#RECUPERATION DES DONNEES

# Import des données
train_data = pd.read_csv('train_data.csv') # jeu de donnés d'entrainement
test_data = pd.read_csv('test_data.csv') # jeu de données de test

train_data.info()
# 5 premières lignes du jeu d'entrainement
train_data.head(5)

train_data.shape[1]

#PREPARATION DES DONNEES

# merge de train et test
all_data = pd.concat([train_data, test_data])
# stats de résumé
all_data.describe()

# affichage du nombre de lignes et de colonnes
print(f"Nombre de lignes: {all_data.shape[0]:,}\nNombre de colonnes: {all_data.shape[1]:,}")

#NETTOYAGE

#PRESENCE DE DOUBLONS
# affichage du nombre de doublons
nb_doublon = all_data.duplicated().sum()
print(f'Nombre de doublons complets : {nb_doublon}')

#supprimer les doublons en modifiant le jeu de données en question
if nb_doublon > 0:
    all_data.drop_duplicates(keep='first', inplace=True, ignore_index=False)
    print(f'Nombre de doublons après nettoyage : {all_data.duplicated().sum()}')

#VALEURS MANQUANTES
# affichage du nombre de valeurs manquantes par colonne
print(f"nombre de valeurs manquantes par colonne : {all_data.isna().sum()}")
# affichage du nombre total de valeurs manquantes
print(f"nombre total de valeurs manquantes : {all_data.isna().sum().sum()}")


