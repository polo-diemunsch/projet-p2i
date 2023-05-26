import mysql.connector as mysql
from creds import creds_bd


def ouvrir_connexion_bd():
    """
    Ouvre une connexion à la base de données.

    Renvoi :
        connexion_bd: Objet de connexion à la bd
    """
    print("")
    print("***********************")
    print("** Connexion à la BD **")
    print("***********************")
    print("")

    connexion_bd = None
    try:
        connexion_bd = mysql.connect(
                host=creds_bd["host"],
                port=creds_bd["port"],
                user=creds_bd["user"],
                password=creds_bd["password"],
                database=creds_bd["database"]
        )
        print("=> Connexion établie avec la base de donnée")
        print()
    except Exception as e:
        print("MySQL [ERROR]")
        print(e)

    return connexion_bd


def fermer_connexion_bd(connexion_bd):
    """
    Ferme la connexion à la base de données.
    """
    print("")
    print("Fermeture de la connexion à la BD")

    try:
        connexion_bd.close()
        print("=> Connexion à la base de données fermée")
        print()
    except Exception as e:
        print("MySQL [ERROR]")
        print(e)


def insert_accelero(connexion_bd, id_perf, valeur_x, valeur_y, tps_depuis_debut):
    """
    Insère des données d'accéléromètre dans la base de données.

    Paramètres :
        int id_perf: Identifiant de la performance à laquelle est liée la mesure
        int valeur_x: Valeur en X de l'accéléromètre
        int valeur_y: Valeur en Y de l'accéléromètre
        float tps_depuis_debut: Moment de la mesure par rapport au début de la performance (en secondes)
    """
    cursor = connexion_bd.cursor()
    cursor.execute("INSERT INTO MesureAccelero (idPerf, valeurX, valeurY, tpsDepuisDebut) VALUES (%s, %s, %s, %s);",
                   [id_perf, valeur_x, valeur_y, tps_depuis_debut])
    connexion_bd.commit()


def insert_BPM(connexion_bd, id_perf, valeur, tps_depuis_debut):
    """
    Insère une donnée de BPM dans la base de données.

    Paramètres :
        int id_perf: Identifiant de la performance à laquelle est liée la mesure
        int valeur: Valeur du BPM
        float tps_depuis_debut: Moment de la mesure par rapport au début de la performance (en secondes)
    """
    cursor = connexion_bd.cursor()
    cursor.execute("INSERT INTO MesureBPM (idPerf, valeur, tpsDepuisDebut) VALUES (%s, %s, %s);",
                   [id_perf, valeur, tps_depuis_debut])
    connexion_bd.commit()


def insert_touche_mesure(connexion_bd, id_perf, note, doigt, tps_presse, tps_depuis_debut):
    """
    Insère des données de touche pressée dans la base de données.

    Paramètres :
        int id_perf: Identifiant de la performance à laquelle est liée la mesure
        int note: Index de la touche du piano correspondante
        int doigt: Doigt avec lequel la touche est pressée
        float tps_presse: Temps pendant lequel la touche est pressée (en secondes)
        float tps_depuis_debut: Moment de la mesure par rapport au début de la performance (en secondes)
    """
    cursor = connexion_bd.cursor()
    cursor.execute("INSERT INTO MesureTouche (idPerf, note, doigt, tpsPresse, tpsDepuisDebut) VALUES (%s, %s, %s, %s, %s);",
                   [id_perf, note, doigt, tps_presse, tps_depuis_debut])
    connexion_bd.commit()


def insert_touche_ref(connexion_bd, id_morceau, note, tps_presse, tps_depuis_debut):
    """
    Insère des données de touche de référence dans la base de données.

    Paramètres :
        int id_morceau: Identifiant du morceau correspondant
        int note: Index de la touche du piano correspondante
        float tps_presse: Temps pendant lequel la touche doit être pressée (en secondes)
        float tps_depuis_debut: Moment de l'appui par rapport au début du morceau (en secondes)
    """
    cursor = connexion_bd.cursor()
    cursor.execute("INSERT INTO ToucheRef (idMorceau, note, tpsPresse, tpsDepuisDebut) VALUES (%s, %s, %s, %s);",
                   [id_morceau, note, tps_presse, tps_depuis_debut])
    connexion_bd.commit()


def clear_touche_ref(connexion_bd):
    """
    Efface toutes les données de la table ToucheRef et réinitialise la valeur de l'auto increment.
    """
    cursor = connexion_bd.cursor()
    cursor.execute("DELETE FROM ToucheRef;")
    cursor.execute("ALTER TABLE ToucheRef AUTO_INCREMENT = 0;")
    connexion_bd.commit()


def insert_morceau(connexion_bd, titre, bpm_morceau):
    """
    Insère un morceau dans la base de données.

    Paramètres :
        str titre: Titre du morceau
    Renvoi :
        int: id du morceau ajouté
    """
    cursor = connexion_bd.cursor()
    cursor.execute("INSERT INTO Morceau (titre, bpmMorceau) VALUES (%s, %s);", [titre, bpm_morceau])
    connexion_bd.commit()

    cursor.execute("SELECT MAX(idMorceau) FROM Morceau;")
    return cursor.fetchone()[0]


def clear_morceau(connexion_bd):
    """
    Efface toutes les données de la table Morceau et réinitialise la valeur de l'auto increment.
    """
    cursor = connexion_bd.cursor()
    cursor.execute("DELETE FROM Morceau;")
    cursor.execute("ALTER TABLE Morceau AUTO_INCREMENT = 0;")
    connexion_bd.commit()


def insert_musicien(connexion_bd, nom, niveau):
    """
    Insère un musicien dans la base de données.

    Paramètres :
        str nom: Nom du musicien
        str niveau: Niveau estimé du musicien
    Renvoi :
        int: id du morceau ajouté
    """
    cursor = connexion_bd.cursor()
    cursor.execute("INSERT INTO Musicien (nom, niveau) VALUES (%s, %s);", [nom, niveau])
    connexion_bd.commit()

    cursor.execute("SELECT MAX(idMusicien) FROM Musicien;")
    return cursor.fetchone()[0]


def insert_performance(connexion_bd, id_musicien, id_morceau, date_perf):
    """
    Insère une nouvelle performance dans la base de données.

    Paramètres :
        int id_musicien: Identifiant du musicien jouant cette performance
        int id_morceau: Identifiant du morceau joué
        str date_perf: Date (et heure) du début de la performance              # A adapter
    """
    cursor = connexion_bd.cursor()
    cursor.execute("INSERT INTO Performance (idMusicien, idMorceau, datePerf) VALUES (%s, %s, %s);",
                   [id_musicien, id_morceau, date_perf])
    connexion_bd.commit()


def update_lvl_musicien(connexion_bd, id_musicien, niveau):
    """
    Mets à jour le niveau d'un musicien.

    Paramètres :
        int id_musicien: Identifiant du musicien jouant cette performance
        str niveau: Nouveau niveau estimé du musicien
    """
    cursor = connexion_bd.cursor()
    cursor.execute("UPDATE Musicien SET niveau = %s WHERE idMusicien = %s;", [niveau, id_musicien])
    connexion_bd.commit()


def update_performance(connexion_bd, id_perf, nb_fausses_notes, nb_notes_total, bpm_moy, niveau_estime):
    """
    Mets à jour les infos sur une performance (à la fin de celle-ci).

    Paramètres :
        int id_perf: Identifiant de la performance
        int nb_fausses_notes: Nombre de fausses notes durant la performance
        int nb_notes_total: Nombre total de notes jouées durant la performance
        int bpm_moy: BPM moyen le long de la performance
        str niveau_estime: Niveau estimé sur cette performance
    """
    cursor = connexion_bd.cursor()
    cursor.execute("UPDATE Performance SET nbFaussesNotes=%s, nbNotesTotal=%s, bpmMoy=%s, niveauEstime=%s  WHERE idPerf = %s;",
                   [nb_fausses_notes, nb_notes_total, bpm_moy, niveau_estime, id_perf])
    connexion_bd.commit()


def get_morceaux(connexion_bd):
    """
    Récupère les id et titres des morceaux présents dans la base de données.

    Renvoi :
        Liste de tuples composés de l'id et du titre pour chaque morceau
    """
    cursor = connexion_bd.cursor()
    cursor.execute("SELECT idMorceau, titre FROM Morceau")
    return cursor.fetchall()


def get_touches_morceau(connexion_bd, id_morceau):
    """
    Récupère les touches de références ainsi que le temps d'appui et le moment où appuyer pour le morceau d'identifiant id_morceau.

    Renvoi :
        Liste de tuples composés de la note, du temps d'appui et du moment où appuyer pour chaque touche
        La liste est triée par moment où appuyer
    """
    cursor = connexion_bd.cursor()
    cursor.execute("SELECT note, tpsPresse, tpsDepuisDebut FROM ToucheRef WHERE idMorceau=%s ORDER BY tpsDepuisDebut DESC", [id_morceau])
    return cursor.fetchall()


def get_musiciens(connexion_bd):
    """
    Récupère les id, noms et niveaux estimés des musiciens présents dans la base de données.

    Renvoi :
        Liste de tuples composés du titre et de l'id, nom et niveau estimé pour chaque musicien
    """
    cursor = connexion_bd.cursor()
    cursor.execute("SELECT idMusicien, nom, niveau FROM Musicien")
    return cursor.fetchall()

def get_perf(connexion_bd, idMusicien, idMorceau):
    cursor = connexion_bd.cursor()
    cursor.execute("SELECT mo.nom as Nom du Musicien, mu.titre as Titre du Morceau, p.datePerf as Date de la Performance, p.nbFaussesNotes as Nb Fausses Notes, (p.nbNotesTotal-p.nbFaussesNotes)/p.nbNotesTotal as Ratio de Précision, p.bpmMoy as BPM Moyen, mu.niveau as Ancien Niveau, p.niveauEstime as Niveau Estimé"
                   +"FROM Musicien mu, Morceau mo, Performance p"
                   +"WHERE p.idMusicien = %s, p.idMorceau = %s, mu.idMusicien = p.idMusicien, mo.idMorceau = p.idMorceau"
                   +"ORDER BY p.datePerf ASC", [idMusicien, idMorceau])
    return cursor.fetchall()

def get_BPM(connexion_bd):
    cursor = connexion_bd.cursor()
    cursor.execute("SELECT valeur as BPM, tpsDepuisDebut as Temps depuis Début FROM MesureBPM")
    return cursor.fetchall()

def get_accelero(connexion_bd):
    cursor = connexion_bd.cursor()
    cursor.execute("SELECT valeurX, valeurY, tpsDepuisDebut as Temps depuis Début FROM MesureAccelero")
    return cursor.fetchall()