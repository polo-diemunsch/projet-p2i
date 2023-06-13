import matplotlib.pyplot as plt
import SQL.commandes_bd as cbd
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def graphique_BPM(connexion_bd, id_perf, main):
    """
    Affiche pour une performance donnée (déterminée par id_perf), l'évolution du rythme
    cardiaque du pianiste concernée en fonction du temps passé depuis le début du morceau

    Paramètres :
        int id_perf: Identifiant de la performance
    """
    fig = Figure(figsize=(10, 3), dpi=100)
    ax = fig.add_subplot(111)
    tuples = cbd.get_BPM(connexion_bd, id_perf)
    l_temps, l_BPM = [], []
    for (a,b) in tuples:
        l_BPM.append(a)
        l_temps.append(b)
    ax.plot(l_temps, l_BPM)
    ax.set_title("Evolution du Rythme Cardiaque durant la prestation")
    ax.set_xlabel('Temps depuis le début (s)')
    ax.set_ylabel('BPM')

    canvas = FigureCanvasTkAgg(fig, master=main)
    canvas.draw()
    canvas.get_tk_widget().pack()


def graphique_accelero(connexion_bd, id_perf, main):
    """
    Affiche deux graphiques pour une performance donnée (déterminée par id_perf):
    1. L'évolution de l'accélération de la main du pianiste sur l'axe des x (sur la longueur du 
        piano)
    2. L'évolution de l'accélération de la main du pianiste sur l'axe des y (sur la largeur du 
        piano)
    Les axes x et y sont les deux seuls axes qui nous intéressent car ce sont les seuls qui
    appartiennent au plan horizontal (l'axe z prenant aussi en compte l'action de la gravité)

    Paramètres :
        int id_perf: Identifiant de la performance
    """
    fig = Figure(figsize=(10, 3), dpi=100)
    ax = fig.add_subplot(111)
    tuples = cbd.get_accelero(connexion_bd, id_perf)
    l_temps, l_accX, l_accY = [], [], []
    for (a,b,c) in tuples:
        l_accX.append(a)
        l_accY.append(b)
        l_temps.append(c)
    ax.plot(l_temps, l_accX, 'b', label='Accélération en X')
    ax.plot(l_temps, l_accY, 'r', label='Accélération en Y')
    ax.set_title("Evolution de l'accélération de la main sur les axes x et y")
    ax.set_xlabel('Temps depuis le début (s)')
    ax.set_ylabel("Amplitude de l'accélération")

    canvas = FigureCanvasTkAgg(fig, master=main)
    canvas.draw()
    canvas.get_tk_widget().pack()


def graphique_niveau(connexion_bd, id_musicien, id_morceau, main, possible_levels):
    """
    Affiche pour un musicien donné (déterminé par id_musicien) et pour un morceau donné
    (déterminé par id_morceau) l'évolution de son niveau sur ce morceau en fonction de la date
    de prestation

    Paramètres :
        int id_musicien: Identifiant du musicien
        int id_morceau: Identifiant du morceau
    """
    fig = Figure(figsize=(4, 4), dpi=100)
    ax = fig.add_subplot(111)
    tuples = cbd.get_perf(connexion_bd, id_musicien, id_morceau)
    l_date, l_niveau = [], []
    i = 0
    for (a, b, c, d, e, f, g, h) in tuples:
        l_date.append(i-len(tuples)+1)
        l_niveau.append(h)
        i += 1

    unique_levels = sorted(set(l_niveau), key=lambda x: possible_levels.index(x))
    level_to_index = {level: possible_levels.index(level) for level in unique_levels}
    sorted_data = sorted(zip(l_niveau, l_date), key=lambda x: level_to_index[x[0]])
    sorted_niveau, sorted_date = zip(*sorted_data)

    ax.scatter(sorted_date, sorted_niveau, s=100, c='r', marker='+')
    ax.set_title('Evolution du niveau de ' + tuples[0][0])
    ax.set_xlabel('Prestation')
    ax.set_ylabel('Niveau Estimé')

    ax.set_yticks(range(len(unique_levels)))
    ax.set_yticklabels(unique_levels)
    ax.tick_params(axis='y', rotation=90)



    canvas = FigureCanvasTkAgg(fig, master=main)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0)


def graphique_nb_fausses_notes(connexion_bd, id_musicien, id_morceau,main):
    """
    Affiche pour un musicien donné (déterminé par id_musicien) et pour un morceau donné
    (déterminé par id_morceau) l'évolution du nombre de fausses notes jouées par ce dernier
    sur ce morceau en fonction de la date de la prestation

    Paramètres :
        int id_musicien: Identifiant du musicien
        int id_morceau: Identifiant du morceau
    """
    fig = Figure(figsize=(4, 4), dpi=100)
    ax = fig.add_subplot(111)
    tuples = cbd.get_perf(connexion_bd, id_musicien, id_morceau)
    l_date, l_nombre = [], []
    i=0
    for (a, b, c, d, e, f, g, h) in tuples:
        l_date.append(i-len(tuples)+1)
        l_nombre.append(d)
        i += 1
    ax.plot(l_date, l_nombre,c='brown')
    ax.set_title('Evolution du nombre de fausses notes de ' + tuples[0][0])
    ax.set_xlabel('Prestation')
    ax.set_ylabel('Nombre de fausses notes')

    canvas = FigureCanvasTkAgg(fig, master=main)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=1)


def graphique_BPM_moyen(connexion_bd, id_musicien, id_morceau, main):
    """
    Affiche pour un musicien donné (déterminé par id_musicien) et pour un morceau donné
    (déterminé par id_morceau) l'évolution de son rythme cardiaque sur ce morceau en fonction
    de la date de prestation

    Paramètres :
        int id_musicien: Identifiant du musicien
        int id_morceau: Identifiant du morceau
    """
    fig = Figure(figsize=(4, 4), dpi=100)
    ax = fig.add_subplot(111)
    tuples = cbd.get_perf(connexion_bd, id_musicien, id_morceau)
    l_date, l_BPMmoy = [], []
    i = 0
    for (a, b, c, d, e, f, g, h) in tuples:
        l_date.append(i-len(tuples)+1)
        l_BPMmoy.append(f)
        i += 1
    ax.plot(l_date, l_BPMmoy)
    ax.set_title('BPM Moyen de ' + tuples[0][0] + ' durant sa prestation')
    ax.set_xlabel('Prestation')
    ax.set_ylabel('BPM Moyen')

    canvas = FigureCanvasTkAgg(fig, master=main)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0)


def graphique_precision(connexion_bd, id_musicien, id_morceau, main):
    """
    Affiche pour un musicien donné (déterminé par id_musicien) et pour un morceau donné
    (déterminé par id_morceau) l'évolution du ratio de précision (nb bonnes notes/nb total)
    de ce dernier sur ce morceau en fonction de la date de la prestation

    Paramètres :
        int id_musicien: Identifiant du musicien
        int id_morceau: Identifiant du morceau
    """
    fig = Figure(figsize=(4, 4), dpi=100)
    ax = fig.add_subplot(111)
    tuples = cbd.get_perf(connexion_bd, id_musicien, id_morceau)
    l_date, l_ratio = [], []
    i=0
    for (a, b, c, d, e, f, g, h) in tuples:
        l_date.append(i-len(tuples)+1)
        l_ratio.append(int(((e - d) / e if e != 0 else 0) * 100))
        i += 1
    ax.plot(l_date, l_ratio, c='g')
    ax.set_title('Evolution du ratio de précision de ' + tuples[0][0])
    ax.set_xlabel('Prestation')
    ax.set_ylabel('Ratio de Précision (en %)')
    ax.set_xlim(l_date[0], l_date[-1])
    ax.set_ylim(0, 100)
    ax.tick_params(axis='y', rotation=90)

    canvas = FigureCanvasTkAgg(fig, master=main)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=1)


def tableau_last(connexion_bd, id_musicien, id_morceau, main, possible_levels):
    """
    Affiche un tableau récapitulatif de la performance avec la précision, le nombre de
    fausses notes, le BPM cardiaque moyen ainsi que le niveau estimé.

    Paramètres :
        int id_musicien: Identifiant du musicien
        int id_morceau: Identifiant du morceau
    """
    data = cbd.get_perf(connexion_bd, id_musicien, id_morceau)[-1]
    date = data[2]
    nb_fausses_notes = data[3]
    precision = (data[4] - nb_fausses_notes) / data[4] if data[4] != 0 else 0
    BPM_moyen = data[5]
    ancien_niv = data[6]
    niv_estime = data[7]
    musicien = cbd.get_nom_musicien(connexion_bd,id_musicien)
    morceau = cbd.get_titre_morceau(connexion_bd,id_morceau)
    info_perf = tk.Label(main, text=f"Performance de {musicien} sur {morceau} réalisée le {date}", font="Arial 16")
    info_perf.pack()

    fenetre = tk.Frame(main)
    fauxlabel = tk.Label(fenetre, text=f"Nombre de fausses notes \n{nb_fausses_notes}", bg="#E72E20", font="Arial 15")
    fauxlabel.grid(row=0, column=0, ipadx=74)
    preclabel = tk.Label(fenetre,text=f"Précision \n {int(precision*100)} %",bg="#FF9900", font="Arial 15")
    preclabel.grid(row=0, column=1, ipadx=172)
    bpmlabel = tk.Label(fenetre,text=f"BPM Moyen \n {BPM_moyen} BPM",bg="#EFF828", font="Arial 15")
    bpmlabel.grid(row=1, column=0, ipadx=150)

    ancien_niv_index = possible_levels.index(ancien_niv)
    niv_estime_index = possible_levels.index(niv_estime)

    if ancien_niv_index < niv_estime_index:
        nivlabel = tk.Label(fenetre, text=f"Evolution du niveau \n {ancien_niv} ↗ {niv_estime}", bg="#50FF00", font="Arial 15")
        nivlabel.grid(row=1, column=1, ipadx=100)
    elif ancien_niv_index == niv_estime_index:
        nivlabel = tk.Label(fenetre,text=f"Evolution du niveau \n {ancien_niv} = {niv_estime}", bg="#FFFFFF", font="Arial 15")
        nivlabel.grid(row=1, column=1, ipadx=100)
    else:
        nivlabel = tk.Label(fenetre,text=f"Evolution du niveau \n {ancien_niv} ↘ {niv_estime}", bg="#DA6262", font="Arial 15")
        nivlabel.grid(row=1, column=1, ipadx=100)

    fenetre.pack()
