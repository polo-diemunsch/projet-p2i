import pandas as pd  # library to work with dataframes
from sklearn.model_selection import train_test_split  # découpage de jeu de données en train et test
from sklearn.preprocessing import MinMaxScaler  # min-max scaler
from sklearn import tree  # decision trees
from sklearn import metrics  # evaluation metrics
from sklearn.neighbors import KNeighborsClassifier  # knn
import matplotlib.pyplot as plt  # Visualization library
import operator

# RECUPERATION DES DONNEES
# Import des données d'entrainement
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

# 5 premières lignes du jeu d'entrainement
# pd.set_option("max_columns", None) # show all cols
print(f"Affichage des 5 premières ligne : \n{train_data.head(5)}\n")

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

# Separation en un jeu de test et un jeu d'entrainement
print("Séparation de la donnée cible du jeu de donnée...\n")
all_x = train_data.loc[:, ~train_data.columns.isin(liste_colonnes_avec_valeurs_manquantes + ['Perf_niveauEstime'])].copy()
all_y = train_data['Perf_niveauEstime'].copy()  # Cible

print("Création d'un jeu d'entrainement et d'un jeu de test...\n")
X_train, X_test, y_train, y_test = train_test_split(all_x, all_y, test_size=0.2, random_state=42, stratify=all_y)

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

# Affichage de l'arbre
plt.figure(figsize=(10, 10))
tree.plot_tree(clf_tree, filled=True, fontsize=6, max_depth=2)  # Modifier ou supprimer max_depth pour modifier la profondeur
# plt.savefig("arbre_de_decision_premières_branches.png")
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
fig, ax = plt.subplots(figsize=(8, 8))
ax.grid(False)
cm_display.plot(ax=ax)
plt.title("Matrice de confusion de l'arbre de classification")
#plt.savefig("matrice_de_confusion_Arbre_Decision.png")
plt.show()


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
y_pred_knn = knn.predict(X_test_scaled)

# Evaluation
# Accuracy
print(f"La précision de KNN : {metrics.accuracy_score(y_test, y_pred_knn)}")

print("Résumé d'évaluation de l'arbre : ")
print(metrics.classification_report(y_test, y_pred_knn))

# matrice de confusion
conf_m = metrics.confusion_matrix(y_test, y_pred_knn)
# display
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix=conf_m,
                                            display_labels=["Jamais touché de piano", "Débutant", "Intermédiaire", "Confirmé", "Expert"])
fig, ax = plt.subplots(figsize=(8, 8))
ax.grid(False)
cm_display.plot(ax=ax)
plt.title("Matrice de confusion de KNN")
#plt.savefig("matrice_de_confusion_KNN.png")
plt.show()


# ANALYSE D'UNE PERFORMANCE
print("*" * 40)
print("Analyse d'une performance")
print("*" * 40 + "\n")


def analyse_performance(path_to_csv_perf_to_analyse):
    perf_to_analyse = pd.read_csv(path_to_csv_perf_to_analyse, sep=";")

    # Normalisation du dataset a analyser
    scaler = MinMaxScaler()
    scaler.fit(X_train.values)  # On définit les valeurs min et max possibles comme celle du dataset d'entrainement
    perf_to_analyse = pd.DataFrame(scaler.transform(perf_to_analyse.values))

    # Prediction
    predicted_tree = clf_tree.predict(perf_to_analyse.values)

    # Recuperation des resultats

    #Resultats de l'arbre de classification
    dico_results = {}
    for result in predicted_tree:
        if result in dico_results.keys():
            dico_results[result] += 1
        else:
            dico_results[result] = 1
    print(dico_results)
    print(f"Niveau estimé par l'arbre de classification: {max(dico_results.items(), key=operator.itemgetter(1))[0]}")

    predicted_knn = clf_tree.predict(perf_to_analyse.values)
    dico_results = {}
    for result in predicted_knn:
        if result in dico_results.keys():
            dico_results[result] += 1
        else:
            dico_results[result] = 1
    print(f"Niveau estimé par KNN: {max(dico_results.items(), key=operator.itemgetter(1))[0]}")
    print("")


analyse = True
while analyse:
    path_to_csv_perf_to_analyse = input("Entrez le chemin vers le fichier csv de la performance à analyser ou appuyer sur q pour quitter : ")
    if path_to_csv_perf_to_analyse != "q":
        analyse_performance(path_to_csv_perf_to_analyse)
    else:
        analyse = False
