import SQL.commandes_bd as cbd
import pandas as pd  # library to work with dataframes
from sklearn.preprocessing import MinMaxScaler  # min-max scaler
from sklearn import tree  # decision trees
import operator


class ArbreDecision:
    def __init__(self, path_to_train_csv):
        self.train_data = pd.read_csv(path_to_train_csv, sep=";")
        self.nettoyage_doublons()
        self.nettoyage_val_manquantes()
        self.separation_des_donnees()
        self.normalisation_train_data()
        self.creation_arbre()

    def nettoyage_doublons(self):
        nb_doublon = self.train_data.duplicated().sum()  # nombre de doublons
        if nb_doublon == 0:
            print("Absence de doublon...\n")
        else:
            # supprimer les doublons en modifiant le jeu de données en question
            print(f"{nb_doublon} doublons détectés...")
            self.train_data.drop_duplicates(keep='first', inplace=True, ignore_index=False)
            print("Doublons supprimés...\n")

    def nettoyage_val_manquantes(self):
        val_manquantes_par_colonnes = self.train_data.isna().sum()
        nombre_valeur_manquante = self.train_data.isna().sum().sum()
        self.liste_colonnes_avec_valeurs_manquantes = []
        if nombre_valeur_manquante > 0:
            print(f"\n{nombre_valeur_manquante} valeurs manquantes détectées\n")
            print("Suppression des colonnes présentant des valeurs manquantes...\n")
            for i in range(0, len(val_manquantes_par_colonnes)):
                if val_manquantes_par_colonnes[i] > 0:
                    self.liste_colonnes_avec_valeurs_manquantes.append(self.train_data.columns[i])
            print("Colonnes présentant des valeurs manquantes supprimées\n")

        else:
            print("\nPas de valeurs maquantes\n")

    def separation_des_donnees(self):
        print("Séparation de la donnée cible du jeu de donnée...\n")
        self.all_x = self.train_data.loc[:, ~self.train_data.columns.isin(self.liste_colonnes_avec_valeurs_manquantes + ['Perf_niveauEstime'])].copy()

        self.all_y = self.train_data['Perf_niveauEstime'].copy()  # Cible

    def normalisation_train_data(self):
        print("Normalisation des données...\n")
        scaler = MinMaxScaler()  # create a scaler object
        # Fit (calculer le min et max pour le futur scaling) aux données et transformer les données
        self.all_x_scaled = pd.DataFrame(scaler.fit_transform(self.all_x), columns=self.all_x.columns)
        print("Données normalisées")

    def creation_arbre(self):
        print("Création de l'arbre...")
        # create a model
        self.clf_tree = tree.DecisionTreeClassifier()
        # fit the model
        self.clf_tree.fit(self.all_x_scaled.values, self.all_y.values)

    def analyse_performance(self, connexion_bd, id_perf_to_analyse):
        perf_to_analyse = cbd.get_perf_to_analyse(connexion_bd, id_perf_to_analyse)
        perf_to_analyse = pd.DataFrame(perf_to_analyse)

        scaler = MinMaxScaler()  # create a scaler object
        scaler.fit(self.all_x.values)
        perf_to_analyse = pd.DataFrame(scaler.transform(perf_to_analyse))

        predicted_tree = self.clf_tree.predict(perf_to_analyse)

        dico_results = {}
        for result in predicted_tree:
            if result in dico_results.keys():
                dico_results[result] += 1
            else:
                dico_results[result] = 1

        return max(dico_results.items(), key=operator.itemgetter(1))[0]